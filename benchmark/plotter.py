from tracemalloc import start
import matplotlib.pyplot as plt
import time
import json


def createPlot(xAxis, yAxis):
    plt.plot(xAxis, yAxis)
    plt.ylabel('some numbers')
    #plt.show()
    plt.savefig(f'benchmark_{time.time()}.png')

def extractAxes(lst):
    firstExec = lst[0]['start_time']
    xAxis = list(map(lambda x: x['start_time'] - firstExec, lst))
    yAxis = list(map(lambda y: y['execution_time'], lst))
    return (xAxis, yAxis)

def benchmarkPlot(lst):
    xAxis, yAxis = extractAxes(lst)
    createPlot(xAxis, yAxis)

def benchmarkPlotFromFile(file):
    with open(file, 'r') as f:
        obj = json.loads(f.read())
        f.close()
    benchmarkPlot(obj)