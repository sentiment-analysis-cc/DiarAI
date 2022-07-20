function submitButton() {              

    var currentUser = getCurrentUser();
    var username = currentUser.username;

    // Await for session token to be available
    var sessionToken = getSessionToken((err, sessionToken) => {
        if (err) {
            alert('Cannot retrieve token!')
        }

        console.log(sessionToken);
        
        var postData = {
            "token": sessionToken,
            "username": username,
            "diaryTitle": $("#diaryTitle").val(),
            "text": $("#diaryEntry").val()
        };
        
        // spara brutalmente verso aws
        // TO-DO: fare con post
        let res = $.ajax({
            type: "GET",
            url: _config.lambda_url, //_config.lambda_url,
            data: postData,
            success: function(data) {
                alert("Succesfully submit entry! Your sentiment value is " + data["compound"])
                console.log(data);
            },
            error: function(data) {
                console.log(data);
            }
        });
        
        console.log(res);
    });

}

