google.charts.load('current', {'packages':['corechart']});
// google.charts.setOnLoadCallback(createChart);

function createChart(data) {
        data = data.reverse();

        // Iterate through data and create a new array with the data we want
        var chartData = [];
        for (var i = 0; i < data.length; i++) {
            var date = getDateFromTimestamp(data[i].id);
            chartData.push([date, data[i].sentiment['compound']]);
        }

        // Create the data table.
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'X');
        data.addColumn('number', 'Sentiment');
        data.addRows(chartData);

        // Set chart options
        var options = {
            'title': 'Sentiment over time',
            'width': 900,
            'height': 500,
            'hAxis': {
                'title': 'Date'
            },
            'vAxis': {
                'title': 'Sentiment'
            },
            'legend': 'none',
            'curveType': 'function',
        };

        // Instantiate and draw our chart, passing in some options.
        var chart = new google.visualization.LineChart(document.getElementById('chart'));
        chart.draw(data, options);
}

// A function that extracts the current date from a timestamp. id is formatted as [name]/[date].txt, only [date] will be returned
function getDateFromTimestamp(id) {

    const zeroPad = (num, places) => String(num).padStart(places, '0')

    var d = id.split("/")[1].split(".")[0];
    // convert epoch date to readable date
    var date = new Date(parseInt(d) * 1000);
    var day = zeroPad(date.getDate(), 2);

    // Parse month in readable format (Jan, Feb, etc.)
    var month = date.toLocaleString('en-us', { month: 'short' });

    //var month = zeroPad(date.getMonth() + 1, 2);
    var year = date.getFullYear();
    var hours = zeroPad(date.getHours(), 2);
    var minutes = zeroPad(date.getMinutes(), 2);
    var readableDate = day + " " + month + " " +  hours + ":" + minutes;
    return readableDate;
}