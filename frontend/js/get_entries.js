function generateTable(data) {
    // Generate table from json entries, stored in req, with the following structure:
    // title of entry, date of entry, compound sentiment, id of entry
    
    var table = document.getElementById("table");
    var row = table.insertRow(0);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);
    cell1.innerHTML = "Title";
    cell2.innerHTML = "Date";
    cell3.innerHTML = "Sentiment";
    cell4.innerHTML = "ID";
    cell1.setAttribute("class", "table-title");
    cell2.setAttribute("class", "table-title");
    cell3.setAttribute("class", "table-title");
    cell4.setAttribute("class", "table-title");
    
    for (var i = 0; i < data.length; i++) {

        var date = getDateFromTimestamp(data[i].id);

        console.log(data[i]);
        var row = table.insertRow(i+1);
        row.id = data[i].id;
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        var cell3 = row.insertCell(2);
        var cell4 = row.insertCell(3);
        cell1.innerHTML = "<a href=\"#"+ i + "\">" + data[i].title + "</a>";
        cell2.innerText = date;
        cell3.innerText = data[i].sentiment.compound;
        cell4.innerText = data[i].id;
    }
    
    $('tr').click((e) => {
        var id = e.currentTarget.id;
        console.log(id);
        var postData = {
            "username": username,
            "type" : "single",
            "id" : id,
        };
        
        let data = $.ajax({
            type: "GET",
            url: _config.lambda_entries_url,
            data: postData,
            success: function(data) {
                console.log(data);
            },
            error: function(data) {
                console.log(data);
                alert("Some error occurred :(\n" + data);
            }
        });
    });
}


// A function that extracts the current date from a timestamp. id is formatted as [name]/[date].txt, only [date] will be returned
function getDateFromTimestamp(id) {

    const zeroPad = (num, places) => String(num).padStart(places, '0')

    var d = id.split("/")[1].split(".")[0];
    // convert epoch date to readable date
    var date = new Date(parseInt(d) * 1000);
    console.log(d);
    var day = zeroPad(date.getDate(), 2);
    var month = zeroPad(date.getMonth() + 1, 2);
    var year = date.getFullYear();
    var hours = zeroPad(date.getHours(), 2);
    var minutes = zeroPad(date.getMinutes(), 2);
    var readableDate = day + "/" + month + "/" + year + " " + hours + ":" + minutes;
    return readableDate;
}
