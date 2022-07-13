import json
import requests
from essential_generators import DocumentGenerator
import threading
import random
import string
import time

def initTexts(num):
    lst = []
    main = DocumentGenerator()
    
    for _ in range(num):
        lst.append(main.sentence() + " " + main.sentence())
    return lst

def doRequest(result, i):
    texts = initTexts(sizeText)
    print("[DEBUG] Text list created! Thread number " + str(i))
    start_time = time.time()
    for text in texts:
        params = misc.copy()
        params.update({"diaryTitle": getRandomString(20), "text": text})
        res = requests.get(basepath, params=params)
        print("[DEBUG] Status Code: " + str(res.status_code) + "; Thread number " + str(i))
    result.append(time.time() - start_time)

def getRandomString(num):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k = num))

basepath = "https://blwdljp75pvc5eswhthjx66a4m0hdbyv.lambda-url.us-east-1.on.aws/"
numThreads = 16
sizeText = 5

f = open('misc.json')
misc = json.load(f)
f.close()

threads = []
res = []

for i in range(numThreads): 
	t = threading.Thread(target=doRequest, args=[res, i])
	t.daemon=True
	threads.append(t)

for t in threads: 
	t.start()

for t in threads: 
	t.join()

print(res)
