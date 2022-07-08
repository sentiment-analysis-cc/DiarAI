import json
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import boto3
import time

def lambda_handler(event, context):
    queryStr = event["queryStringParameters"]
    text = queryStr["text"]
    res = computeSentiment(text)
    title = queryStr["diaryTitle"]
    user = queryStr["username"]
    filename = f'{user}/{time.time()}.txt'
    
    upload2Bucket(text, filename)
    
    putInDynamoDB(filename, title, user, res)
    
    return {
        'statusCode': 200,
        'body': json.dumps(res)
    }


def computeSentiment(text):
    sia = SentimentIntensityAnalyzer()
    res = sia.polarity_scores(text)
    return res
    
def upload2Bucket(text, filename):
    s3 = boto3.resource('s3')
    object = s3.Object('diary-entries', filename)
    object.put(Body=text)

def putInDynamoDB(filename, title, username, sentimentOut):
    client = boto3.client('dynamodb')
    mapping = list(map(lambda x : {x[0] : {'N': str(x[1])}}, zip(sentimentOut.keys(), sentimentOut.values())))
    
    sentimentItem = {}
    for x in range(len(mapping)):
        sentimentItem.update(mapping[x])
    
    client.put_item(TableName='diary-associations', Item={'id': {'S' : filename}, 'title': {'S': title}, 'username': {'S': username}, 'sentiment': {'M': sentimentItem}})