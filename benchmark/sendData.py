import requests
from essential_generators import DocumentGenerator
import threading
import random
import string
import time
import sys
from autoLogin import *
import argparse

basepath = "https://blwdljp75pvc5eswhthjx66a4m0hdbyv.lambda-url.us-east-1.on.aws/"
numThreads = 16
sizeText = 5
deltaTime = 600  # sec

parser = argparse.ArgumentParser(description='Optional app description')

parser.add_argument('--threads', type=int,
                    help='Number of threads', default=numThreads)

parser.add_argument('--text-len', type=int,
                    help='Length of text array', default=sizeText)

parser.add_argument('--executioin-time', type=int,
                    help='Execution time on a single thread', default=deltaTime)

parser.add_argument('--create-users', action='store_true',
                    help='Sign up new users')

args = parser.parse_args()

numThreads, sizeText, deltaTime, reSignUp = vars(args).values()


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

def doRequest(result, token, i):
    texts = initTexts(sizeText)
    index = 0
    print("[DEBUG] Text list created! Thread number " + str(i))
    start_time = time.time()
    localEndTime = time.time() + deltaTime
    # Print current time in humanly readable format
    s= time.strftime("%H:%M:%S", time.localtime(start_time))
    e= time.strftime("%H:%M:%S", time.localtime(localEndTime))
    print(f"[DEBUG] Start time for thread {i}: {s} - End time: {e}")
    while time.time() <= localEndTime:
        params = ({"diaryTitle": getRandomString(20), "text": texts[index], "token": token})
        res = requests.get(basepath, params=params)
        print("[DEBUG] Status Code: " + str(res.status_code) + "; Thread number " + str(i))
        index = (index + 1) % len(texts)
        if index == 0:
            random.shuffle(texts)
    print("--- Thread number " + str(i) + " finished! ---")
    result.append(time.time() - start_time)

def getRandomString(num):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k = num))

print('Starting script with')
print(f'Number of thread: {numThreads}')
print(f'Text list size: {sizeText}')
print(f'Execution time: {deltaTime}s')
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
	t = threading.Thread(target=doRequest, args=[res, tokens[i], i])
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


