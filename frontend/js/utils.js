// window._config = {
//   cognito: {
//       userPoolId: 'us-east-1_iBJ56HJ3I', // e.g. us-east-2_uXboG5pAb
//       region: 'us-east-1', // e.g. us-east-2
//   clientId: '3peuo13ghjq51jnenhh9svi47u' //is this used anywhere?
//   },
//   lambda_url: "https://blwdljp75pvc5eswhthjx66a4m0hdbyv.lambda-url.us-east-1.on.aws/",
//   lambda_entries_url: "https://uuq3nqiwkutez37nremubegf6i0xqjsz.lambda-url.us-east-1.on.aws/"
// };

function getCurrentUser() {
    var poolData = {
        UserPoolId : _config.cognito.userPoolId, // Your user pool id here
        ClientId : _config.cognito.clientId, // Your client id here
      };
      
      var userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);

      var cognitoUser = userPool.getCurrentUser();
      return cognitoUser;
}

function logout() {
    var cognitoUser = getCurrentUser();
    if (cognitoUser != null) {
        cognitoUser.signOut();
    }

    window.location.href = "login.html";
}