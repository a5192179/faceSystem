from multiprocessing import Process
import multiprocessing
import time
def func1(d, name, age):
    if name in d:
        print('func1 begin, name:', name, 'age', age, 'd[name]', d[name])
    else:
        print('func1 begin, name:', name, 'age', age)
    d[name] = age + 0.1
    print('func1 over, name:', name, 'age', age, 'd[name]', d[name])

def func2(d, name, age):
    if name in d:
        print('func2 begin, name:', name, 'age', age, 'd[name]', d[name])
    else:
        print('func2 begin, name:', name, 'age', age)
    d[name] = age + 0.2
    print('func2 over, name:', name, 'age', age, 'd[name]', d[name])

def func3(d, name, age):
    if name in d:
        print('func3 begin, name:', name, 'age', age, 'd[name]', d[name])
    else:
        print('func3 begin, name:', name, 'age', age)
    d[name] = age + 0.3
    print('func3 over, name:', name, 'age', age, 'd[name]', d[name])

class myADD(Process):
    def __init__(self, dictOri, index):
        Process.__init__(self)
        self.dictOri = dictOri
        self.index = index

    def run(self):
        print('i:', self.index)
        for key in self.dictOri.keys():
            self.dictOri[key] += 1
            print('key', key, 'value', self.dictOri[key])
            a = {'index':self.index}
            self.dictOri['index'] = a
            print(self.dictOri['index'])
            self.dictOri['index']['index'] = 100
            print(self.dictOri['index'])

            b={'indexb':1000}
            self.dictOri['index'] = b
            print(self.dictOri['index'])
            
            print('index' in self.dictOri)
            del self.dictOri['index']
            print('index' in self.dictOri)
            a=1

if __name__ == '__main__':
    processors = []
    mgr = multiprocessing.Manager()
    myDict = mgr.dict()
    myDict['a'] = 3

    for i in range(1):
        processors.append(myADD(myDict, i))

    for oneWork in processors:
        oneWork.start()

    while True:
        for index, oneWork in enumerate(processors):
            if not oneWork.is_alive():
                processors[index] = myADD(myDict, index)
                processors[index].start()
            time.sleep(1)

    # =================================
#     mgr = multiprocessing.Manager()
#     d = mgr.dict()
#     p1 = Process(target=func1, args=(d, 'A', 1))
#     p2 = Process(target=func2, args=(d, 'A', 2))
#     p3 = Process(target=func3, args=(d, 'C', 3))
#     start_time = time.time()
#     p1.start()
#     p2.start()
#     p3.start()
#     p2.join()
#     p1.join()
#     p3.join()
#     print('主进程')
#     print(time.time() - start_time)
#     '''
#     B 进程 running (this order is random)
#     A 进程 running (this order is random)
#     C 进程 running (this order is random)
#     A 进程 over
#     B 进程 over
#     C 进程 over
#     主进程
#     3.1728098392486572
# ​
#     '''
    # =================================