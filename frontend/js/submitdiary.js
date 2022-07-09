function submitButton() {              

    var currentUser = getCurrentUser();
    var username = currentUser.username;
    
    // TODO CHECK IF USER IS LOGGED IN
    
    console.log(username);
    
    var postData = {
        "username": username,
        "diaryTitle": $("#diaryTitle").val(),
        "text": $("#diaryEntry").val()
    };
    
    // spara brutalmente verso aws
    // TO-DO: fare con post
    let text = $.ajax({
        type: "GET",
        url: "https://blwdljp75pvc5eswhthjx66a4m0hdbyv.lambda-url.us-east-1.on.aws/", //_config.lambda_url,
        data: postData,
        success: function(data) {
            console.log(data);
        },
        error: function(data) {
            console.log(data);
        }
    });
    
    console.log(text);
    
}