from tracemalloc import start
import requests
from essential_generators import DocumentGenerator
import threading
import random
import string
import time
from autoLogin import *
import argparse

basepathWrite = "https://blwdljp75pvc5eswhthjx66a4m0hdbyv.lambda-url.us-east-1.on.aws/"
basepathRead = "https://uuq3nqiwkutez37nremubegf6i0xqjsz.lambda-url.us-east-1.on.aws/"
numThreads = 16
sizeText = 5
deltaTime = 600  # sec

parser = argparse.ArgumentParser(description='Optional app description')

parser.add_argument('--threads', '-t', type=int,
                    help='Number of threads', default=numThreads)

parser.add_argument('--text-len', '--num-req', type=int, 
                    help='Length of text array, or number of request per thread', default=sizeText)

parser.add_argument('--stop-mode' , '-sm', type=str, choices=['time', 'num'],
                    help='The stopping mode', default='time')

parser.add_argument('--execution-time' , '-et', type=int,
                    help='Execution time on a single thread', default=deltaTime)

parser.add_argument('--create-users', '-c',action='store_true',
                    help='Sign up new users')

parser.add_argument('--mode', '-m', type=str, required=True, choices=['write', 'read'],
                    help='Target of the lambda function')

args = parser.parse_args()

numThreads, sizeText, stopMode, deltaTime, reSignUp, mode = vars(args).values()

### Functions ###

def initTexts(num):
    lst = []
    main = DocumentGenerator()
    
    for _ in range(num):
        lst.append(main.sentence() + " " + main.sentence())
    return lst

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

def doWriteRequest(result, token, i):
    texts = initTexts(sizeText)
    index = 0
    print("[DEBUG] Text list created! Thread number " + str(i))
    start_time = time.time()
    localEndTime = start_time + deltaTime
    # Print current time in humanly readable format
    if stopMode == "time":
        s= time.strftime("%H:%M:%S", time.localtime(start_time))
        e= time.strftime("%H:%M:%S", time.localtime(localEndTime))
        print(f"[DEBUG] Start time for thread {i}: {s} - End time: {e}")
    while time.time() <= localEndTime or stopMode == 'num':
        params = ({"diaryTitle": getRandomString(20), "text": texts[index], "token": token})
        res = requests.get(basepathWrite, params=params)
        print("[DEBUG] Status Code: " + str(res.status_code) + "; Thread number " + str(i))
        index = (index + 1) % len(texts)
        if index == 0:
            if stopMode == "time":
                random.shuffle(texts)
            elif stopMode == "num":
                break
    print("--- Thread number " + str(i) + " finished! ---")
    result.append(time.time() - start_time)

def doReadRequest(result, token, i):
    index = 0
    start_time = time.time()
    localEndTime = start_time + deltaTime
    if stopMode == "time":
        s= time.strftime("%H:%M:%S", time.localtime(start_time))
        e= time.strftime("%H:%M:%S", time.localtime(localEndTime))
        print(f"[DEBUG] Start time for thread {i}: {s} - End time: {e}")
    while time.time() <= localEndTime or stopMode == 'num':
        params = ({"type": "all", "token": token})
        res = requests.get(basepathRead, params=params)
        print("[DEBUG] Status Code: " + str(res.status_code) + "; Thread number " + str(i))
        index += 1
        if stopMode == "num" and index >= sizeText:
            break
    print("--- Thread number " + str(i) + " finished! ---")
    result.append(time.time() - start_time)


def getRandomString(num):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k = num))


print(f'Current mode: {mode}')
print(f'Number of thread: {numThreads}')
if stopMode == 'time':
    print(f'Text list size: {sizeText}')
    print(f'Execution time: {deltaTime}s')
else:
    print(f'Number of request per thread: {sizeText}')
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
res = []

print("--- Starting to fill texts ---")
for i in range(numThreads):
    if mode == "write":
        t = threading.Thread(target=doWriteRequest, args=[res, tokens[i], i])
    elif mode == "read":
        t = threading.Thread(target=doReadRequest, args=[res, tokens[i], i])
    t.daemon=True
    threads.append(t)

for t in threads: 
    t.start()

for t in threads: 
    t.join()

print(res)
min = min(res)
max = max(res)
avg = sum(res) / len(res)

print("Minimum: "+str(min)+"; Maximum: "+str(max)+"; Average: "+str(avg))