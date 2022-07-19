import json
import boto3
from boto3.dynamodb.types import TypeDeserializer
from boto3.dynamodb.conditions import Key
import time 


def lambda_handler(event, context):
    startTime = time.time()
    queryStr = event["queryStringParameters"]
    type = queryStr["type"]
    token = queryStr["token"]
    cognito = boto3.client('cognito-idp')
    username = cognito.get_user(AccessToken = token)
    username = username['Username']
    
    if type  == "all":
        entries = getEntries(username)
        return {
            'statusCode': 200,
            'body': json.dumps(entries)
        }
    elif type == "single":
        id = event["queryStringParameters"]["id"]
        return {
            'statusCode': 200,
            'body': json.dumps(getEntry(username, id))
        }
    elif type == "benchmark":
        entries = getEntries(username)
        endTime = time.time() - startTime
        return {
            'statusCode': 200,
            'body': json.dumps({"execution_time":endTime, "start_time": startTime, "count": len(entries)})
        }


def getEntries(username):
    client = boto3.resource('dynamodb')
    table = client.Table('diary-associations')
    
    response = table.query(
        IndexName='username-index',
        KeyConditionExpression=Key('username').eq(username)
    )
    
    lst = list(map(lambda x : decimalToFloat(x), response['Items']))
    lst.sort(key=lambda x : getTimestamp(x['id']), reverse=True)
    return lst


def getEntry(username, id):
    s3 = boto3.client('s3')
    res = s3.get_object(Bucket = 'diary-entries', Key = id)
    resDict = {}
    resDict['text'] = res['Body'].read().decode('utf-8')
    return resDict
    
    
def decimalToFloat(item):
    item['sentiment'] = dict(map(lambda kv: (kv[0], float(kv[1])), item['sentiment'].items()))
    return item

def getTimestamp(id):
    timestamp = id.split('/')[-1].replace('.txt', '')
    return float(timestamp)