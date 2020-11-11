import datetime
class timeStatistician:
    def __init__(self, facebase, leaveThreshold = 60):
        self.timebase = {}
        self.leaveThreshold = leaveThreshold #unit seconds
        for identity in facebase:
            beginTime = datetime.datetime(2020, 1, 1, 0, 0, 0, 0)
            lastTime = datetime.datetime(2020, 1, 1, 0, 0, 0, 0)
            status = 'dormant'
            info = {'beginTime':beginTime, 'lastTime':lastTime, 'status':status}
            self.timebase[identity] = info
    
    def insert(self, identity, imgTime):
        if identity in self.timebase:
            print(identity, 'is in database, can not insert!')
            return
        print('new person, identity', identity)
        beginTime = imgTime
        lastTime = imgTime
        status = 'activated'
        info = {'beginTime':beginTime, 'lastTime':lastTime, 'status':status}
        self.timebase[identity] = info

    def delete(self, identity):
        if not identity in self.timebase:
            print(identity, 'is not in database, can not delete!')
            return
        del self.timebase[identity]

    def reset(self, identity, imgTime):
        if not identity in self.timebase:
            print(identity, 'is not in database, can not reset!')
            return
        print('reset time, identity', identity)
        self.timebase[identity]['status'] = 'activated'
        self.timebase[identity]['beginTime'] = imgTime
        self.timebase[identity]['lastTime'] = imgTime

    def update(self, identity, imgTime):
        '''
        threshold is the period between now and last seen, unit is second
        '''
        if not identity in self.timebase:
            print(identity, 'is not in database, insert new!')
            self.insert(identity, imgTime)
            return
        if (imgTime - self.timebase[identity]['lastTime']).seconds > self.leaveThreshold:
            # new
            print('delta time：', (imgTime - self.timebase[identity]['lastTime']).seconds)
            self.reset(identity, imgTime)
        else:
            print('update time, identity', identity)
            self.timebase[identity]['lastTime'] = imgTime

    def getStayTime(self, identity):
        if not identity in self.timebase:
            print(identity, 'is not in database!')
            return 0
        print('identity,', identity, 'begin time', self.timebase[identity]['beginTime'])
        stayTime = (self.timebase[identity]['lastTime'] - self.timebase[identity]['beginTime']).seconds
        # unit is second
        return stayTime

    def getFinalStayTime(self, imgTime):
        # if not identity in self.timebase:
        #     print('error, ', identity, 'is not in database!')
        #     return 0
        finalStayTimes = {}
        for identity in self.timebase:
            if self.timebase[identity]['status'] == 'dormant':
                continue
            elif (imgTime - self.timebase[identity]['lastTime']).seconds > self.leaveThreshold:
                finalStayTime = (self.timebase[identity]['lastTime'] - self.timebase[identity]['beginTime']).seconds
                finalStayTimes[identity] = finalStayTime #unit second
                self.timebase[identity]['status'] = 'dormant'
                print('identity', identity, 
                      'go out, begin time:',self.timebase[identity]['beginTime'],
                       'end time:', imgTime)
        return finalStayTimes

    def getStayTimebyIdentities(self, identities, imgTime):
        stayTimes = []
        print('imgTime:', imgTime)
        for identity in identities:
            self.update(identity, imgTime)
            stayTime = self.getStayTime(identity)
            print('identity', identity, 'stayTime', stayTime, ' second')
            stayTimes.append(stayTime) # unit is second
        return stayTimes
