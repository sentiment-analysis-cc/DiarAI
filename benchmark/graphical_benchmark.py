from tracemalloc import start, stop
import requests
from essential_generators import DocumentGenerator
import threading
import random
import string
import time
from autoLogin import *
import argparse
import json
from plotter import benchmarkPlot

basepathWrite = "https://blwdljp75pvc5eswhthjx66a4m0hdbyv.lambda-url.us-east-1.on.aws/"
basepathRead = "https://uuq3nqiwkutez37nremubegf6i0xqjsz.lambda-url.us-east-1.on.aws/"
numThreads = 16
sizeText = 5
executionTime = 600  # sec

parser = argparse.ArgumentParser(description='Optional app description')

parser.add_argument('--threads', '-t', type=int,
                    help='Number of threads', default=numThreads)

parser.add_argument('--text-len', '--num-req', type=int, 
                    help='Length of text array, or number of request per thread', default=sizeText)

parser.add_argument('--stop-mode' , '-sm', type=str, choices=['time', 'num', 'incremental'],
                    help='The stopping mode', default='time')

parser.add_argument('--execution-time' , '-et', type=int,
                    help='Execution time on a single thread', default=executionTime)

parser.add_argument('--create-users', '-c', action='store_true',
                    help='Sign up new users')

parser.add_argument('--mode', '-m', type=str, required=True, choices=['write', 'read'],
                    help='Target of the lambda function')

args = parser.parse_args()

numThreads, sizeText, stopMode, executionTime, reSignUp, mode = vars(args).values()

lst = [10, 20, 50, 100, 100, 100, 70, 50, 20, 10]
stepLen = executionTime / len(lst)

### Functions ###

def initTexts(num, res):
    main = DocumentGenerator()
    for _ in range(num):
        res.append(main.sentence() + " " + main.sentence())

def createUsers(num):
    lst = []
    for i in range(num):
        user = f"test{i}"
        signUp(user, f"test{i}@test.com", "ciaociao")
        lst.append(user)
    return lst

def loginUsers(lst):
    return list(map(lambda user : login(user, "ciaociao"), lst))

def numberedLogin(num):
    return loginUsers(list(map(lambda x: f"test{x}", range(num))))

def doWriteRequest(result, token, i, textList):
    texts = textList
    index = 0
    start_time = time.time()
    localEndTime = start_time + executionTime
    bodies = []
    # Print current time in humanly readable format
    if stopMode == "time":
        s= time.strftime("%H:%M:%S", time.localtime(start_time))
        e= time.strftime("%H:%M:%S", time.localtime(localEndTime))
        print(f"[DEBUG] Start time for thread {i}: {s} - End time: {e}")
    while time.time() <= localEndTime or stopMode == 'num' or stopMode == "incremental":
        params = ({"diaryTitle": getRandomString(20), "text": texts[index], "token": token, "type": "benchmark"})
        active = True
        if stopMode == "incremental":
            active = canIRun(i)
            print(f"Thread: {i}; canIRun: {active}")
        if active:
            startRequest = time.time()
            res = requests.get(basepathWrite, params=params)
            print("[DEBUG] Status Code: " + str(res.status_code) + "; Thread number " + str(i))
            if res.status_code == 200:
                try: 
                    jsonBody = json.loads(res.content)
                    jsonBody.update({"start_client_request": startRequest})
                    bodies.append(jsonBody)
                except AttributeError:
                    print("ERROR OCCURRED IN PARSING RESULT: " + jsonBody)
                    continue
        else:
            time.sleep(stepLen - 0.01)
        index = (index + 1) % len(texts)
        if index == 0:
            if stopMode == "time" or stopMode == "incremental":
                random.shuffle(texts)
            elif stopMode == "num":
                break
        if stopMode == "incremental" and time.time() > globalTime + executionTime:
            break
    print("--- Thread number " + str(i) + " finished! ---")
    obj = {"bodies": bodies, "thread_time": time.time() - start_time}
    result.append(obj)

def doReadRequest(result, token, i):
    index = 0
    start_time = time.time()
    localEndTime = start_time + executionTime
    bodies = []
    if stopMode == "time":
        s= time.strftime("%H:%M:%S", time.localtime(start_time))
        e= time.strftime("%H:%M:%S", time.localtime(localEndTime))
        print(f"[DEBUG] Start time for thread {i}: {s} - End time: {e}")
    while time.time() <= localEndTime or stopMode == 'num' or stopMode == "incremental":
        params = ({"type": "benchmark", "token": token})
        active = True
        if stopMode == "incremental":
            active = canIRun(i)
        if active:
            startRequest = time.time()
            res = requests.get(basepathRead, params=params)
            print("[DEBUG] Status Code: " + str(res.status_code) + "; Thread number " + str(i))
            if res.status_code == 200:
                try: 
                    jsonBody = json.loads(res.content)
                    jsonBody.update({"start_client_request": startRequest})
                    bodies.append(jsonBody)
                except AttributeError:
                    print("ERROR OCCURRED IN PARSING RESULT: " + jsonBody)
                    continue
        else:
            time.sleep(stepLen - 0.01)
        index += 1
        if stopMode == "num" and index >= sizeText:
            break
        elif stopMode == "incremental" and time.time() > globalTime + executionTime:
            break
    print("--- Thread number " + str(i) + " finished! ---")
    obj = {"bodies": bodies, "thread_time": time.time() - start_time}
    result.append(obj)


def getRandomString(num):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k = num))

def canIRun(index):
    currentTime = time.time() - globalTime
    ind = int(currentTime // stepLen)
    return index < numThreads * (lst[(ind - 1) % len(lst)] / 100)


print(f'Current mode: {mode}')
print(f'Number of thread: {numThreads}')
if stopMode == 'time':
    print(f'Text list size: {sizeText}')
    print(f'Execution time: {executionTime}s')
elif stopMode == 'num':
    print(f'Number of request per thread: {sizeText}')
elif stopMode == 'incremental':
    print(f'Text list size: {sizeText}')
    print(f'Incremental time: {executionTime}s')
    print(f'Step time: {stepLen}')
print()


if reSignUp:
    print("--- Creating users... ---")
    users = createUsers(numThreads)
    print("--- Logging in users ---")
    tokens = loginUsers(users)
else:
    print("--- Logging in users ---")
    tokens = numberedLogin(numThreads)


threads = []
textMatrix = [[] for _ in range(numThreads)]

if mode == 'write':
    print("--- Starting to fill texts ---")
    for i in range(numThreads):
        t = threading.Thread(target=initTexts, args=[numThreads, textMatrix[i]])
        t.daemon=True
        threads.append(t)

    for t in threads: 
        t.start()

    for t in threads: 
        t.join()

    print("[DEBUG] Text list created!")

threads = []
res = []
globalTime = time.time()
for i in range(numThreads):
    if mode == "write":
        t = threading.Thread(target=doWriteRequest, args=[res, tokens[i], i, textMatrix[i]])
    elif mode == "read":
        t = threading.Thread(target=doReadRequest, args=[res, tokens[i], i])
    t.daemon=True
    threads.append(t)

for t in threads: 
    t.start()

for t in threads: 
    t.join()

threadsTime = list(map(lambda x: x["thread_time"], res))
min = min(threadsTime)
max = max(threadsTime)
avg = sum(threadsTime) / len(threadsTime)
print("Minimum: "+str(min)+"; Maximum: "+str(max)+"; Average: "+str(avg))

bodies = list(map(lambda x: x['bodies'], res))

# Flat list
flatBodies = []
for x in bodies:
    flatBodies += x
bodies = flatBodies

# Plot results

flatBodies.sort(key=lambda x: x['start_time'])
print(flatBodies)

with open(f'benchmark_{time.time()}.txt', 'w') as f:
    f.write(json.dumps(flatBodies))
    f.close()

benchmarkPlot(flatBodies)