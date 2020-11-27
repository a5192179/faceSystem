import matplotlib.pyplot as plt
import sys
sys.path.append('.')
from common.myColor import getColor

# def myColor(num, resultFormat = 'str'):
#     if resultFormat == 'str':
#         baseColors = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple', 'pink', 'gray', 'black', 'aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'blanchedalmond', 'blueviolet']
#         if num > len(baseColors):
#             Exception('Too more colors!')
#         return baseColors[0:num]
    
# bins : integer or array_like, optional

# 这个参数指定bin(箱子)的个数,也就是总共有几条条状图

# normed : boolean, optional

# If True, the first element of the return tuple will be the counts normalized to form a probability density, i.e.,n/(len(x)`dbin)

# 这个参数指定密度,也就是每个条状图的占比例比,默认为1

# color : color or array_like of colors or None, optional "skyblue" 'green'
# lw=0 线宽
# alpha=0.5 设置透明度，0为完全透明
# range The lower and upper range of the bins. Lower and upper outliers are ignored. If not provided, range is (x.min(), x.max()). Range has no effect if bins is a sequence.

def myBar(xs, ys, elementLabels = None, xlabel = None, ylabel = None, title = None, xlim = None, ylim = None, xAxislabels = None):
    """
    绘制条形图
    left:长条形中点横坐标
    height:长条形高度
    width:长条形宽度，默认值0.8
    label:为后面设置legend准备
    """
    xNum = len(xs)
    colors = getColor(xNum)
    width = (max(xs) - min(xs)) / (xNum - 1) * 0.618
    for i in range(xNum):
        x = xs[i]
        y = ys[i]
        if elementLabels != None:
            label = elementLabels[i]
            plt.bar(x=x, height=y, width=width, alpha=0.8, color=colors[i], label=label)
        else:
            plt.bar(x=x, height=y, width=width, alpha=0.8, color=colors[i])
    """
    设置x轴刻度显示值
    参数一：中点坐标
    参数二：显示值
    """
    if ylim == None:
        plt.ylim(0.95 * min(ys), 1.05 * max(ys))
    elif len(ylim) == 1:
        plt.ylim(ylim[0], 1.05 * max(ys))
    else:
        plt.ylim(ylim[0], ylim[1])
        
    if xlim != None:
        plt.xlim(xlim[0], xlim[1])
    else:
        plt.xlim(min(xs) - 3 * width / 4, max(xs) + 3 * width / 4)
        
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
    # xs = [1, 2]
    # ys = [692, 633]
    # elementLabels = ['male', 'female']
    # ylabel = 'counting'
    # xlabel = 'gender ID'
    # title = 'gender of test data'
    # ylim = [0]
    # xAxislabels = ['male', 'female']
    # myBar(xs, ys, elementLabels = elementLabels, ylabel = ylabel, xlabel = xlabel, title = title, ylim = ylim)
    # xs = [1, 2, 3, 4]
    # ys = [227, 739, 316, 43]
    # elementLabels = ['0-20', '21-40', '41-60', '61+']
    # ylabel = 'counting'
    # xlabel = 'age group ID'
    # title = 'age of test data'
    # ylim = [0]
    # myBar(xs, ys, elementLabels = elementLabels, ylabel = ylabel, xlabel = xlabel, title = title, ylim = ylim)
    xs = [0, 1, 2, 3, 4, 5]
    ys = [292, 791, 329, 182, 34, 0]
    elementLabels = ['0', '1', '2', '3', '4', '5+']
    ylabel = 'number of images'
    xlabel = 'number of faces in each image'
    title = 'number of face'
    ylim = [0]
    xAxislabels = ['male', 'female']
    myBar(xs, ys, elementLabels = elementLabels, ylabel = ylabel, xlabel = xlabel, title = title, ylim = ylim)
