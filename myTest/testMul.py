from multiprocessing import Process
import time
def func(name, i):
    print('%s 进程 running'%name)
    time.sleep(i)
    print('%s 进程 over'%name)
    
if __name__ == '__main__':
    p1 = Process(target=func, args=('A',1))
    p2 = Process(target=func, args=('B',2))
    p3 = Process(target=func, args=('C',3))
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