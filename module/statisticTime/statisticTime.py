import datetime
class timeStatistician:
    def __init__(self, identityBase, cameraID, leaveThreshold = 60, leaveErrorThreshold = 1.0):
        self.identityBase = identityBase
        self.leaveThreshold = leaveThreshold #unit seconds
        self.leaveErrorThreshold = leaveErrorThreshold #unit seconds
        self.cameraID = cameraID
        # for identity in facebase:
        #     beginFrame = -1
        #     lastFrame = -1
        #     status = 'dormant'
        #     info = {'beginFrame':beginFrame, 'lastFrame':lastFrame, 'status':status}
        #     self.timebase[identity] = info
    
    def setTime(self, identity, frameID):
        # print('new person, identity', identity)
        age = self.identityBase[identity]['age']
        gender = self.identityBase[identity]['gender']
        img = self.identityBase[identity]['img']
        vec = self.identityBase[identity]['vec']
        timeInfo = self.identityBase[identity]['timeInfo']
        beginFrame = frameID
        lastFrame = frameID
        status = 'activated'
        timeInfo[self.cameraID] = {'beginFrame':beginFrame, 'lastFrame':lastFrame, 'status':status}
        person = {'age':age, 'gender':gender, 'img':img, 'vec':vec, 'timeInfo':timeInfo}
        self.identityBase[identity] = person

    def delete(self, identity):
        if not identity in self.identityBase:
            print(identity, 'is not in database, can not delete!')
            return
        del self.identityBase[identity]

    def reset(self, identity, frameID):
        # print('reset time, identity', identity)
        age = self.identityBase[identity]['age']
        gender = self.identityBase[identity]['gender']
        img = self.identityBase[identity]['img']
        vec = self.identityBase[identity]['vec']
        timeInfo = self.identityBase[identity]['timeInfo']
        beginFrame = frameID
        lastFrame = frameID
        status = 'activated'
        timeInfo[self.cameraID] = {'beginFrame':beginFrame, 'lastFrame':lastFrame, 'status':status}
        person = {'age':age, 'gender':gender, 'img':img, 'vec':vec, 'timeInfo':timeInfo}
        self.identityBase[identity] = person

    def update(self, identity, frameID, fps):
        '''
        threshold is the period between now and last seen, unit is second
        '''
        if len(self.identityBase[identity]['timeInfo']) == 0:
            self.setTime(identity, frameID)
            return
        elif not self.cameraID in self.identityBase[identity]['timeInfo']:
            self.setTime(identity, frameID)
            return
        if (frameID - self.identityBase[identity]['timeInfo'][self.cameraID]['lastFrame']) / fps > self.leaveThreshold:
            # print('reset, delta frame:', frameID - self.timebase[identity]['lastFrame'])
            self.reset(identity, frameID)
        else:
            # print('update time, identity', identity)
            age = self.identityBase[identity]['age']
            gender = self.identityBase[identity]['gender']
            img = self.identityBase[identity]['img']
            vec = self.identityBase[identity]['vec']
            timeInfo = self.identityBase[identity]['timeInfo']
            beginFrame = self.identityBase[identity]['timeInfo'][self.cameraID]['beginFrame']
            lastFrame = frameID
            status = self.identityBase[identity]['timeInfo'][self.cameraID]['status']
            timeInfo[self.cameraID] = {'beginFrame':beginFrame, 'lastFrame':lastFrame, 'status':status}
            person = {'age':age, 'gender':gender, 'img':img, 'vec':vec, 'timeInfo':timeInfo}
            self.identityBase[identity] = person

    def getStayTime(self, identity, fps):
        if not identity in self.identityBase.keys():
            print(identity, 'is not in identityBase!')
            return 0
        # print('identity,', identity, 'begin frame:', self.timebase[identity]['beginFrame'])
        stayTime = (self.identityBase[identity]['timeInfo'][self.cameraID]['lastFrame'] - self.identityBase[identity]['timeInfo'][self.cameraID]['beginFrame']) / fps
        # unit is second
        return stayTime

    def getFinalStayTime(self, frameID, fps):
        # if not identity in self.timebase:
        #     # print('error, ', identity, 'is not in database!')
        #     return 0
        finalStayTimes = {}
        for identity in self.identityBase.keys():
            if identity == 'nextId':
                continue
            if not self.cameraID in self.identityBase[identity]['timeInfo']:
                continue
            if self.identityBase[identity]['timeInfo'][self.cameraID]['status'] == 'dormant':
                continue
            elif (frameID - self.identityBase[identity]['timeInfo'][self.cameraID]['lastFrame']) / fps > self.leaveThreshold:
                age = self.identityBase[identity]['age']
                gender = self.identityBase[identity]['gender']
                img = self.identityBase[identity]['img']
                vec = self.identityBase[identity]['vec']
                timeInfo = self.identityBase[identity]['timeInfo']
                beginFrame = self.identityBase[identity]['timeInfo'][self.cameraID]['beginFrame']
                lastFrame = self.identityBase[identity]['timeInfo'][self.cameraID]['lastFrame']
                status = 'dormant'
                timeInfo[self.cameraID] = {'beginFrame':beginFrame, 'lastFrame':lastFrame, 'status':status}
                person = {'age':age, 'gender':gender, 'img':img, 'vec':vec, 'timeInfo':timeInfo}
                self.identityBase[identity] = person

                finalStayTime = (self.identityBase[identity]['timeInfo'][self.cameraID]['lastFrame'] - self.identityBase[identity]['timeInfo'][self.cameraID]['beginFrame']) / fps
                if finalStayTime > self.leaveErrorThreshold:
                    finalStayTimes[identity] = finalStayTime #unit second
                    print('------')
                    print('identity', identity, 
                        'finalStayTime', finalStayTime,
                        'go out, begin frame:',self.identityBase[identity]['timeInfo'][self.cameraID]['beginFrame'],
                        'end frame:', self.identityBase[identity]['timeInfo'][self.cameraID]['lastFrame'])
                    print('------')
                else:
                    print('------')
                    print('identity', identity, 
                        'finalStayTime', finalStayTime,
                        'go out, more like a mistake, begin frame:',self.identityBase[identity]['timeInfo'][self.cameraID]['beginFrame'],
                        'end frame:', self.identityBase[identity]['timeInfo'][self.cameraID]['lastFrame'])
                    print('------')
        return finalStayTimes

    def getStayTimebyIdentities(self, identities, frameID, fps):
        stayTimes = []
        # print('frameID:', frameID)
        for identity in identities:
            self.update(identity, frameID, fps)
            stayTime = self.getStayTime(identity, fps)
            # print('identity', identity, 'stayTime', stayTime, ' second')
            stayTimes.append(stayTime) # unit is second
        return stayTimes
