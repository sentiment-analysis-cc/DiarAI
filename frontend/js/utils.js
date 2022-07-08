function getCurrentUser() {
    var poolData = {
        UserPoolId : _config.cognito.userPoolId, // Your user pool id here
        ClientId : _config.cognito.clientId, // Your client id here
      };
      
      var userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);

      var cognitoUser = userPool.getCurrentUser();
      return cognitoUser;
}