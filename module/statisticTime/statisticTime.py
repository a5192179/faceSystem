import datetime
class timeStatistician:
    def __init__(self, facebase):
        self.timebase = {}
        for identity in facebase:
            beginTime = 0
            lastTime = 0
            info = {'beginTime':beginTime, 'lastTime':lastTime}
            self.timebase[identity] = info
    
    def insert(identity, imgTime):
        if self.timebase.haskey(identity):
            print(identity, 'is in database, can not insert!')
            return
        beginTime = imgTime
        lastTime = imgTime
        info = {'beginTime':beginTime, 'lastTime':lastTime}
        self.timebase[identity] = info

    def delete(identity):
        if not self.timebase.haskey(identity):
            print(identity, 'is not in database, can not delete!')
            return
        del self.timebase[identity]

    def reset(identity, imgTime):
        if not self.timebase.haskey(identity):
            print(identity, 'is not in database, can not reset!')
            return
        self.timebase[identity]['beginTime'] = imgTime
        self.timebase[identity]['lastTime'] = imgTime

    def update(identity, imgTime, threshold = 600):
        '''
        threshold is the period between now and last seen, unit is second
        '''
        if not self.timebase.haskey(identity):
            print(identity, 'is not in database, insert new!')
            self.insert(identity, imgTime)
        if (self.timebase[identity]['lastTime'] - imgTime).seconds > threshold:
            # new
            self.reset(identity, imgTime)
        else:
            self.timebase[identity]['lastTime'] = imgTime

    def getStayTime(identity):
        if not self.timebase.haskey(identity):
            print(identity, 'is not in database!')
            return 0
        stayTime = (self.timebase[identity]['lastTime'] - self.timebase[identity]['beginTime']).seconds
        # unit is second
        return stayTime

    def getStayTimebyIdentities(identities, imgTime):
        stayTimes = []
        for identity in identities:
            self.update(identity, imgTime)
            stayTime = self.getStayTime(identity)
            stayTimes.append(stayTime / 60) # unit is minutes
        return stayTimes
