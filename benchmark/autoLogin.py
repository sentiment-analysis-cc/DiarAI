from cmath import log
import boto3

CLIENT_ID = "2iujemsjc32fgm5vj2sb5b7s77"
cognito = boto3.client('cognito-idp', region_name = 'us-east-1')

def signUp(username, email, password):
    try:
        sign_up_response = cognito.sign_up(
                    ClientId=CLIENT_ID,
                    Username=username,
                    Password=password,
                    UserAttributes=[{'Name': 'email',
                                    'Value': email}])
    except Exception as e:
        # Probably user already exists
        return False
    return True
    


def login(username, password):
    response = cognito.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password},
            ClientId=CLIENT_ID)

    return response['AuthenticationResult']['AccessToken']
