var username;
var password;
var personalname;
var poolData;
    
function registerButton() {

personalname =  document.getElementById("personalnameRegister").value;	
email = document.getElementById("emailInputRegister").value;


if (document.getElementById("passwordInputRegister").value != document.getElementById("confirmationpassword").value) {
    alert("Passwords Do Not Match!")
    throw "Passwords Do Not Match!"
} else {
    password =  document.getElementById("passwordInputRegister").value;	
}

poolData = {
        UserPoolId : _config.cognito.userPoolId, // Your user pool id here
        ClientId : _config.cognito.clientId // Your client id here
    };		
var userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);

var attributeList = [];

var dataEmail = {
    Name : 'email', 
    Value : email, //get from form field
};

var dataPersonalName = {
    Name : 'name', 
    Value : personalname, //get from form field
};

var attributeEmail = new AmazonCognitoIdentity.CognitoUserAttribute(dataEmail);
var attributePersonalName = new AmazonCognitoIdentity.CognitoUserAttribute(dataPersonalName);


attributeList.push(attributeEmail);
attributeList.push(attributePersonalName);

userPool.signUp(personalname, password, attributeList, null, function(err, result){
    if (err) {
        alert(err.message || JSON.stringify(err));
        return;
    }
    cognitoUser = result.user;
    console.log('user name is ' + cognitoUser.getUsername());
    //change elements of page
    //document.getElementById("titleheader").innerHTML = "Check your email for a verification link";
    window.location.href = "login.html";
    
});
}