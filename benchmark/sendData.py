import json
import requests
from essential_generators import DocumentGenerator
import threading
import random
import string
import time
import sys
from autoLogin import *


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
    while time.time() <= endTime:
        params = ({"diaryTitle": getRandomString(20), "text": texts[index], "token": token})
        res = requests.get(basepath, params=params)
        print("[DEBUG] Status Code: " + str(res.status_code) + "; Thread number " + str(i))
        index = (index + 1) % len(texts)
        if index == 0:
            random.shuffle(texts)
    result.append(time.time() - start_time)

def getRandomString(num):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k = num))


basepath = "https://blwdljp75pvc5eswhthjx66a4m0hdbyv.lambda-url.us-east-1.on.aws/"
numThreads = 16
sizeText = 5
startGlobalTime = time.time()
deltaTime = 120  # sec
endTime = startGlobalTime + deltaTime

args = sys.argv
argsLen = len(args)

if argsLen > 1:
    numThreads = int(args[1])
if argsLen > 2:
    sizeText = int(args[2])

users = createUsers(numThreads)
tokens = loginUsers(users)

#tokens = numberedLogin(numThreads)

# f = open('misc.json')
# misc = json.load(f)
# f.close()

threads = []
res = []

print("--- Starting to fill texts... ---")
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
