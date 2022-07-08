import json
import boto3

def lambda_handler(event, context):
    print (getEntries("test@test.it"))
   
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


def getEntries(username, limit):
    client = boto3.client('dynamodb')
    
    response = client.scan(
        TableName='diary-associations',
        FilterExpression='username = :username',
        ExpressionAttributeValues={
            ':username': {'S': username}
        }
    )
    return response['Items']