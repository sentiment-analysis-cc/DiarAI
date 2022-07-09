function signInButton() {
      
    console.log(localStorage.getItem("CognitoIdentityServiceProvider.3peuo13ghjq51jnenhh9svi47u.LastAuthUser"));
    console.log(cognitoUser);
    var authenticationData = {
      Username : document.getElementById("inputUsername").value,
      Password : document.getElementById("inputPassword").value,
    };
    
    var authenticationDetails = new AmazonCognitoIdentity.AuthenticationDetails(authenticationData);
    
    var poolData = {
      UserPoolId : _config.cognito.userPoolId, // Your user pool id here
      ClientId : _config.cognito.clientId, // Your client id here
    };
    
    var userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);
    
    var userData = {
      Username : document.getElementById("inputUsername").value,
      Pool : userPool,
    };
    
    var cognitoUser = new AmazonCognitoIdentity.CognitoUser(userData);
    
    cognitoUser.authenticateUser(authenticationDetails, {
      onSuccess: function (result) {
        var accessToken = result.getAccessToken().getJwtToken();
        console.log(result);
        // console.log(accessToken);	
        // Redirect to get_entries
        window.location.href = "get_entries.html";
      },
      
      onFailure: function(err) {
        alert(err.message || JSON.stringify(err));
      },
    });
  }