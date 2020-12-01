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
    
if __name__ == '__main__':
    mgr = multiprocessing.Manager()
    d = mgr.dict()
    p1 = Process(target=func1, args=(d, 'A', 1))
    p2 = Process(target=func2, args=(d, 'A', 2))
    p3 = Process(target=func3, args=(d, 'C', 3))
    start_time = time.time()
    p1.start()
    p2.start()
    p3.start()
    p2.join()
    p1.join()
    p3.join()
    print('主进程')
    print(time.time() - start_time)
    '''
    B 进程 running (this order is random)
    A 进程 running (this order is random)
    C 进程 running (this order is random)
    A 进程 over
    B 进程 over
    C 进程 over
    主进程
    3.1728098392486572
​
    '''