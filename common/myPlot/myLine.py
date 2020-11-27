import matplotlib.pyplot as plt
import sys
sys.path.append('.')
from common.myColor import getColor
import numpy as np
import random
from scipy import interpolate 
    
# bins : integer or array_like, optional

# 这个参数指定bin(箱子)的个数,也就是总共有几条条状图

# normed : boolean, optional

# If True, the first element of the return tuple will be the counts normalized to form a probability density, i.e.,n/(len(x)`dbin)

# 这个参数指定密度,也就是每个条状图的占比例比,默认为1

# color : color or array_like of colors or None, optional "skyblue" 'green'
# lw=0 线宽
# alpha=0.5 设置透明度，0为完全透明
# range The lower and upper range of the bins. Lower and upper outliers are ignored. If not provided, range is (x.min(), x.max()). Range has no effect if bins is a sequence.

# plt.plot(x, y1, color='red', linewidth=10.0, linestyle='--')

def myLine(xs, ys, elementLabels = None, xlabel = None, ylabel = None, title = None, xlim = None, ylim = None, xAxislabels = None):
    fig = plt.figure(1)
    color = getColor(1)
    plt.plot(xs, ys, color = 'm', linewidth = 1, alpha = 1, linestyle = '-')
    

    if ylim == None:
        plt.ylim(0.95 * min(ys), 1.05 * max(ys))
    elif len(ylim) == 1:
        plt.ylim(ylim[0], 1.05 * max(ys))
    else:
        plt.ylim(ylim[0], ylim[1])
        
    if xlim != None:
        plt.xlim(xlim[0], xlim[1])
    else:
        width = max(xs) - min(xs)
        plt.xlim(min(xs) - 0.05 * width, max(xs) + 0.05 * width)
        
    if ylabel != None:
        plt.ylabel(ylabel)
    if xlabel != None:
        plt.xlabel(xlabel)

    if xAxislabels != None:
        x = range(xNum)
        plt.xticks([index + 0.2 for index in xs], xAxislabels)

    if title != None:
        plt.title(title)
    if elementLabels != None:
        plt.legend(loc = 1)
    plt.grid()
    plt.show()

# def myHist(weights, bins):
#     plt.hist(bins[:-1], weights = weights, bins = bins), color = myColor(len(weights)))

if __name__ == "__main__":
    xs = np.array([0, 100, 250, 500, 1000])/2
    ys = np.array([0.7, 0.9, 0.925, 0.93, 0.94])
    tck = interpolate.splrep(xs, ys)
    x_new = np.linspace(0, 500, 50)
    y_bspline = interpolate.splev(x_new, tck)   
    # f1 = np.polyfit(xl, yl, 10)
    # p1 = np.poly1d(f1)
    # xs = np.linspace(0, 500, 50)
    # ys=np.polyval(f1, xs)
    elementLabels = ['male', 'female']
    ylabel = 'true positive rate'
    xlabel = 'false positive'
    title = 'ROC of mtcnn'
    # ylim = [0]
    # xAxislabels = ['male', 'female']
    myLine(x_new, y_bspline, ylabel = ylabel, xlabel = xlabel, title = title)

