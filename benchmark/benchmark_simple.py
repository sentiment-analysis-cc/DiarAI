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
from tqdm import tqdm
from plotter import benchmarkPlot

# Variables
numThreads = 200
scalingPercentages = [10, 20, 50, 100, 100, 100, 50, 20, 10]
scalingSteps = len(scalingPercentages)
scalingTime = 400
totalExecutionTime = scalingTime * scalingSteps

tokens = []
basepathWrite = "https://blwdljp75pvc5eswhthjx66a4m0hdbyv.lambda-url.us-east-1.on.aws/"
p_diaryTitle = "Test Diary Title"
p_text = "I am very happy. Or sad. Either way, this is a test diary entry that has been sent to the server."

def loginUsers(lst):
    return list(map(lambda user : login(user, "ciaociao"), lst))

def createUsers(num):
    lst = []
    for i in range(num):
        user = f"test{i}"
        signUp(user, f"test{i}@test.com", "ciaociao")
        lst.append(user)
    return lst

def numberedLogin(num):
    tempList = []
    for i in tqdm(range(num)):
        temp_token = login(f"test{i}", "ciaociao")
        tempList.append(temp_token)
    return tempList
    #return loginUsers(list(map(lambda x: f"test{x}", range(num))))

def createRequest(token, i):
    threadStartingTime = time.time()
    shouldSleep(i, threadStartingTime)
    while True:
        params = ({"diaryTitle": p_diaryTitle, "text": p_text, "token": token, "type": "benchmark"})
        res = requests.get(basepathWrite, params=params)
        print("[DEBUG] Status Code: " + str(res.status_code) + "; Thread number " + str(i))
        #
        shouldSleep(i, threadStartingTime)
        
def shouldSleep(i, threadStartingTime):
    currentTime = time.time()
    deltaTime = currentTime - threadStartingTime
    if deltaTime >= totalExecutionTime:
        exit(0)

    a = scalingPercentages[int(deltaTime // scalingTime)]
    #print(a)
    if a < (i)/numThreads*100:
        print(f"Thread {i} will now sleep")
        time.sleep(scalingTime)
        shouldSleep(i, threadStartingTime)
        return
    else:
        #print(f"Thread {i} will now start or will keep on running")
        return



# # # # # # MAIN OPERATIONS

print(f"Number of threads: {numThreads}")
print(f"ETA: {totalExecutionTime}")

# Log in numThread users
print(f"--- Logging in {numThreads} users... ---")
tokens = numberedLogin(numThreads)
print("--- Done! Starting threads... ---")

threads = []
# Start numThread threads
for i in range(numThreads):
    t = threading.Thread(target=createRequest, args=[tokens[i], i])
    t.daemon=True
    threads.append(t)

for t in threads: 
    t.start()

for t in threads: 
    t.join()