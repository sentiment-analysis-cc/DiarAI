window._config = {
    cognito: {
        userPoolId: 'us-east-1_Q1wDry2Wr', // e.g. us-east-2_uXboG5pAb
        region: 'us-east-1', // e.g. us-east-2
		clientId: '2iujemsjc32fgm5vj2sb5b7s77' //is this used anywhere?
    },
    lambda_url: "https://blwdljp75pvc5eswhthjx66a4m0hdbyv.lambda-url.us-east-1.on.aws/",
    lambda_entries_url: "https://uuq3nqiwkutez37nremubegf6i0xqjsz.lambda-url.us-east-1.on.aws/"
};

function getCurrentUser() {
    var poolData = {
        UserPoolId : _config.cognito.userPoolId, // Your user pool id here
        ClientId : _config.cognito.clientId, // Your client id here
      };
      
      var userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);

      var cognitoUser = userPool.getCurrentUser();
      return cognitoUser;
}

// Function to get aws session token
function getSessionToken() {
    var cognitoUser = getCurrentUser();
    if (cognitoUser != null) {
        cognitoUser.getSession(function(err, session) {
            if (err) {
                console.log(err);
                return null;
            }
            window.session = session;
            return session.accessToken.jwtToken;
        });
    }
}

function logout() {
    var cognitoUser = getCurrentUser();
    if (cognitoUser != null) {
        cognitoUser.signOut();
    }

    window.location.href = "login.html";
}