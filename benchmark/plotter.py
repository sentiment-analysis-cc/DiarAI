from tracemalloc import start
import matplotlib.pyplot as plt


def createPlot(xAxis, yAxis):
    plt.plot(xAxis, yAxis)
    plt.ylabel('some numbers')
    plt.show()

def extractAxes(lst):
    firstExec = lst[0]['start_time']
    xAxis = list(map(lambda x: x['start_time'] - firstExec, lst))
    yAxis = list(map(lambda y: y['execution_time'], lst))
    return (xAxis, yAxis)

def benchmarkPlot(lst):
    xAxis, yAxis = extractAxes(lst)
    createPlot(xAxis, yAxis)