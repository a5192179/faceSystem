import datetime
class timeStatistician:
    def __init__(self, facebase, leaveThreshold = 60, leaveErrorThreshold = 1.0):
        self.timebase = {}
        self.leaveThreshold = leaveThreshold #unit seconds
        self.leaveErrorThreshold = leaveErrorThreshold #unit seconds
        for identity in facebase:
            beginFrame = -1
            lastFrame = -1
            status = 'dormant'
            info = {'beginFrame':beginFrame, 'lastFrame':lastFrame, 'status':status}
            self.timebase[identity] = info
    
    def insert(self, identity, frameID):
        if identity in self.timebase:
            print(identity, 'is in database, can not insert!')
            return
        # print('new person, identity', identity)
        beginFrame = frameID
        lastFrame = frameID
        status = 'activated'
        info = {'beginFrame':beginFrame, 'lastFrame':lastFrame, 'status':status}
        self.timebase[identity] = info

    def delete(self, identity):
        if not identity in self.timebase:
            print(identity, 'is not in database, can not delete!')
            return
        del self.timebase[identity]

    def reset(self, identity, frameID):
        if not identity in self.timebase:
            print(identity, 'is not in database, can not reset!')
            return
        # print('reset time, identity', identity)
        self.timebase[identity]['status'] = 'activated'
        self.timebase[identity]['beginFrame'] = frameID
        self.timebase[identity]['lastFrame'] = frameID

    def update(self, identity, frameID, fps):
        '''
        threshold is the period between now and last seen, unit is second
        '''
        if not identity in self.timebase:
            # print(identity, 'is not in database, insert new!')
            self.insert(identity, frameID)
            return
        if (frameID - self.timebase[identity]['lastFrame']) / fps > self.leaveThreshold:
            # new
            # print('reset, delta frame:', frameID - self.timebase[identity]['lastFrame'])
            self.reset(identity, frameID)
        else:
            # print('update time, identity', identity)
            self.timebase[identity]['lastFrame'] = frameID

    def getStayTime(self, identity, fps):
        if not identity in self.timebase:
            print(identity, 'is not in database!')
            return 0
        # print('identity,', identity, 'begin frame:', self.timebase[identity]['beginFrame'])
        stayTime = (self.timebase[identity]['lastFrame'] - self.timebase[identity]['beginFrame']) / fps
        # unit is second
        return stayTime

    def getFinalStayTime(self, frameID, fps):
        # if not identity in self.timebase:
        #     # print('error, ', identity, 'is not in database!')
        #     return 0
        finalStayTimes = {}
        for identity in self.timebase:
            if self.timebase[identity]['status'] == 'dormant':
                continue
            elif (frameID - self.timebase[identity]['lastFrame']) / fps > self.leaveThreshold:
                self.timebase[identity]['status'] = 'dormant'
                finalStayTime = (self.timebase[identity]['lastFrame'] - self.timebase[identity]['beginFrame']) / fps
                if finalStayTime > self.leaveErrorThreshold:
                    finalStayTimes[identity] = finalStayTime #unit second
                    print('------')
                    print('identity', identity, 
                        'finalStayTime', finalStayTime,
                        'go out, begin frame:',self.timebase[identity]['beginFrame'],
                        'end frame:', self.timebase[identity]['lastFrame'])
                    print('------')
                else:
                    print('------')
                    print('identity', identity, 
                        'finalStayTime', finalStayTime,
                        'go out, more like a mistake, begin frame:',self.timebase[identity]['beginFrame'],
                        'end frame:', self.timebase[identity]['lastFrame'])
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
