
    google.charts.load('current', { 'packages': ['annotationchart', 'corechart', 'calendar'] });

    google.charts.setOnLoadCallback(drawPiChart);

    function drawPiChart(response) {

    var responseData = []
    responseData.push(['Location', 'Counts']);
    response.forEach(element => {
        console.log(element)
        responseData.push([element[0] , element[1]]);
      });

        console.log('from db-chart.js')
        console.log(responseData);

        var data = google.visualization.arrayToDataTable(responseData);

        var options = {
        title: 'Pie Chart',
        // width: "800",
        // height: "400",
        animation: {
            startup: true,
            duration: 800,
            easing: "inAndOut"
        },
        };

        var chart = new google.visualization.PieChart(document.getElementById('chart-area'));

        chart.draw(data, options);
    }



    //calendar chart
  
  function drawCalendarChart() {

    var responseData = [];
    $.get("getHeatMapofOccurences", function (response, status) {

      response.data.forEach(element => {
        console.log('calendar chart')
        console.log(element)
        responseData.push([new Date(element[0].split('-')[2], element[0].split('-')[1], element[0].split('-')[0]), element[1]]);
        // responseData.push([element]);
      });

      // console.log('responsedata')
      // console.log(responseData);

      var dataTable = new google.visualization.DataTable();
      dataTable.addColumn({ type: 'date', id: 'Date' });
      dataTable.addColumn({ type: 'number', id: 'Won/Loss' });
      dataTable.addRows(responseData);

      var chart = new google.visualization.Calendar(document.getElementById('chart-area'));

      var options = {
        title: "Annual Attendance",
        width: "800",
        // height: "600",
        animation: {
          startup: true,
          duration: 2000,
          easing: "inAndOut"
        },
      };
      chart.draw(dataTable, options);
    });
  }


  google.charts.load("current", {packages:["timeline"]});
  google.charts.setOnLoadCallback(drawTimeChart);
  function drawTimeChart(sid, arrive , leave , date  ) {

    var container = document.getElementById('chart-area');
    var chart = new google.visualization.Timeline(container);

    

    var dataTable = new google.visualization.DataTable();
    dataTable.addColumn({ type: 'string', id: 'SID' });
    dataTable.addColumn({ type: 'date', id: 'Start' });
    dataTable.addColumn({ type: 'date', id: 'End' });
    dataTable.addRows([
      [ sid.toString(),
        new Date(
        date.split('-')[2], date.split('-')[1], date.split('-')[0],
        arrive.split(':')[0], arrive.split(':')[1], arrive.split(':')[2]
        ),
        new Date(
          date.split('-')[2], date.split('-')[1], date.split('-')[0],
          leave.split(':')[0], leave.split(':')[1], leave.split(':')[2]
          )]]);

    var options = {
      timeline: { colorByRowLabel: true }
    };

    chart.draw(dataTable, options);
  }


  google.charts.load("current", {packages:["timeline"]});
  google.charts.setOnLoadCallback(myRouteTimeLine);
  function myRouteTimeLine (response){

    
        var container = document.getElementById('chart-area');
        var chart = new google.visualization.Timeline(container);

        // sid = response[0][1]
        // name = response[0][0]
        responseData = []

        for (let index = 0; index < response.length; index++) {
          if (index == response.length-1){break;}
          const element = response[index];
          const nextElement = response[index+1];
          console.log(element)
          responseData.push([
            element[1].toString() , element[3]+' to '+nextElement[3] ,  
            new Date(
                element[2].split('-')[2], element[2].split('-')[1], element[2].split('-')[0],
                element[4].split(':')[0], element[4].split(':')[1], element[4].split(':')[2]
              ),
            new Date(
              nextElement[2].split('-')[2], nextElement[2].split('-')[1], nextElement[2].split('-')[0],
              nextElement[4].split(':')[0], nextElement[4].split(':')[1], nextElement[4].split(':')[2]
            )
          ]);
        }

        // response.forEach(element => {
        //   console.log(element)
        //   responseData.push([
        //     element[1].toString() , element[3] ,  
        //     new Date(
        //         element[2].split('-')[2], element[2].split('-')[1], element[2].split('-')[0],
        //         element[4].split(':')[0], element[4].split(':')[1], element[4].split(':')[2]
        //       ),
        //   ]);
        // });

        console.log('responseData')
        console.log(responseData)

        var dataTable = new google.visualization.DataTable();
        dataTable.addColumn({ type: 'string', id: 'SID' });
        dataTable.addColumn({ type: 'string', id: 'Location' });
        dataTable.addColumn({ type: 'date', id: 'Start' });
        dataTable.addColumn({ type: 'date', id: 'End' });
        dataTable.addRows(responseData);
    
        var options = {
          timeline: { colorByRowLabel: false }
        };
  
      chart.draw(dataTable, options);
    }