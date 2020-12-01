import datetime
import cv2
ts1 = datetime.datetime(2014, 10, 27, 21, 46, 16, 657523)
ts2 = datetime.datetime(2014, 10, 27, 21, 56, 16, 757523)
# ts1 = datetime.datetime.now()
# cv2.waitKey(2000)
# ts2 = datetime.datetime.now()
a = (ts2-ts1)
# print((ts2-ts1).minute>500)
# a=['a', 'b', 'c']
# for i, word in a:
#     print('i:', i, 'word:', word)
import time
# time.sleep(0.01)
# time.sleep(0.01)
for i in range(3):
    a=1
    b=3
    for j in range(10):
        t1 = time.time()
        # cv2.waitKey(10)
        time.sleep(0.01)
        t2 = time.time()
        print(t2 - t1)