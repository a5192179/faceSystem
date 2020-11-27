def getColor(num, resultFormat = 'str'):
    if resultFormat == 'str':
        baseColors = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple', 'pink', 'gray', 'black', 'aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'blanchedalmond', 'blueviolet']
        if num > len(baseColors):
            Exception('Too more colors!')
        return baseColors[0:num]