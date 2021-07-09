$(document).ready(function () {

  // to populate dashboard with data
  dashboardData();
  function dashboardData() {
    var Students = $('#noOfStudents');
    var location = $('#noOfLocation');
    var Occurences = $('#totalOccurence');
    var OccurenceToday = $('#totalOccurenceToday');
    $.ajax({
      url: '/getDashboardData',
      data: { 'INFO': 'SAADI' },
      type: 'GET',
      success: function (response) {
        console.log(response);
        var data = response.data;

        console.log('data = ' + data);
        Students.text(data['students'])
        location.text(data['location'])
        Occurences.text(data['occurences'])
        OccurenceToday.text(data['occurencesToday'])
      }
    });
  }

  // var responseData;
  // $.get("getMostVisitedLocation", function(response, status){
  //   responseData = response;
  //   console.log(responseData);
  // });


  google.charts.load('current', { 'packages': ['annotationchart', 'corechart', 'calendar'] });
  google.charts.setOnLoadCallback(drawAnnotChart);

  function drawAnnotChart() {
    var data = new google.visualization.DataTable();
    data.addColumn('date', 'Date');
    data.addColumn('number', 'Kepler-22b mission');
    data.addColumn('string', 'Kepler title');
    data.addColumn('string', 'Kepler text');
    data.addColumn('number', 'Gliese 163 mission');
    data.addColumn('string', 'Gliese title');
    data.addColumn('string', 'Gliese text');
    data.addRows([
      [new Date(2314, 2, 15), 12400, undefined, undefined,
        10645, undefined, undefined],
      [new Date(2314, 2, 16), 24045, 'Lalibertines', 'First encounter',
        12374, undefined, undefined],
      [new Date(2314, 2, 17), 35022, 'Lalibertines', 'They are very tall',
        15766, 'Gallantors', 'First Encounter'],
      [new Date(2314, 2, 18), 12284, 'Lalibertines', 'Attack on our crew!',
        34334, 'Gallantors', 'Statement of shared principles'],
      [new Date(2314, 2, 19), 8476, 'Lalibertines', 'Heavy casualties',
        66467, 'Gallantors', 'Mysteries revealed'],
      [new Date(2314, 2, 20), 0, 'Lalibertines', 'All crew lost',
        79463, 'Gallantors', 'Omniscience achieved']
    ]);

    var chart = new google.visualization.AnnotationChart(document.getElementById('chart_div'));

    var options = {
      displayAnnotations: true
    };

    chart.draw(data, options);
  }


  // scatter chart
  // google.charts.load('current', {'packages':['corechart']});
  google.charts.setOnLoadCallback(drawScatterChart);

  function drawScatterChart() {
    var data = google.visualization.arrayToDataTable([
      ['Age', 'Weight'],
      [8, 12],
      [4, 5.5],
      [11, 14],
      [4, 5],
      [3, 3.5],
      [6.5, 7]
    ]);

    var options = {
      title: 'Age vs. Weight comparison',
      hAxis: { title: 'Age', minValue: 0, maxValue: 15 },
      vAxis: { title: 'Weight', minValue: 0, maxValue: 15 },
      legend: 'none'
    };

    var chart = new google.visualization.ScatterChart(document.getElementById('chart-scatter-activity'));

    chart.draw(data, options);
  }


  // buble chart
  // google.charts.load('current', {'packages':['corechart']});
  google.charts.setOnLoadCallback(drawSeriesChart);

  function drawSeriesChart() {

    var data = google.visualization.arrayToDataTable([
      ['ID', 'Life Expectancy', 'Fertility Rate', 'Region', 'Population'],
      ['CAN', 80.66, 1.67, 'North America', 33739900],
      ['DEU', 79.84, 1.36, 'Europe', 81902307],
      ['DNK', 78.6, 1.84, 'Europe', 5523095],
      ['EGY', 72.73, 2.78, 'Middle East', 79716203],
      ['GBR', 80.05, 2, 'Europe', 61801570],
      ['IRN', 72.49, 1.7, 'Middle East', 73137148],
      ['IRQ', 68.09, 4.77, 'Middle East', 31090763],
      ['ISR', 81.55, 2.96, 'Middle East', 7485600],
      ['RUS', 68.6, 1.54, 'Europe', 141850000],
      ['USA', 78.09, 2.05, 'North America', 307007000]
    ]);

    var options = {
      title: 'Correlation between life expectancy, fertility rate ' +
        'and population of some world countries (2010)',
      hAxis: { title: 'Life Expectancy' },
      vAxis: { title: 'Fertility Rate' },
      bubble: { textStyle: { fontSize: 11 } },
      width: "800",
      height: "250",
      animation: {
        startup: true,
        duration: 800,
        easing: "inAndOut"
      },
    };

    var chart = new google.visualization.BubbleChart(document.getElementById('chart-bubble-activity'));
    chart.draw(data, options);
  }


  //Chart Calendar
  // // google.charts.load("current", {packages:["calendar"]});
  // google.charts.setOnLoadCallback(drawCalendarChart);

  // function drawCalendarChart() {
  //     var dataTable = new google.visualization.DataTable();
  //     dataTable.addColumn({ type: 'date', id: 'Date' });
  //     dataTable.addColumn({ type: 'number', id: 'Won/Loss' });
  //     dataTable.addRows([
  //         [ new Date(2012, 3, 13), 37032 ],
  //         [ new Date(2012, 3, 14), 38024 ],
  //         [ new Date(2012, 3, 15), 38024 ],
  //         [ new Date(2012, 3, 16), 38108 ],
  //         [ new Date(2012, 3, 17), 38229 ],
  //         // Many rows omitted for brevity.
  //         [ new Date(2013, 9, 4), 38177 ],
  //         [ new Date(2013, 9, 5), 38705 ],
  //         [ new Date(2013, 9, 12), 38210 ],
  //         [ new Date(2013, 9, 13), 38029 ],
  //         [ new Date(2013, 9, 19), 38823 ],
  //         [ new Date(2013, 9, 23), 38345 ],
  //         [ new Date(2013, 9, 24), 38436 ],
  //         [ new Date(2013, 9, 30), 38447 ]
  //     ]);

  //     var chart = new google.visualization.Calendar(document.getElementById('chart-calendar'));

  //     var options = {
  //       title: "Todays Attendance",
  //       width: "800",
  //       // height: "600",
  //       animation: {
  //         startup: true,
  //         duration: 800,
  //         easing: "inAndOut"
  //       },
  //     };

  //     chart.draw(dataTable, options);



  //     }   

  //calendar chart
  google.charts.setOnLoadCallback(drawCalendarChart);
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

      var chart = new google.visualization.Calendar(document.getElementById('chart-calendar'));

      var options = {
        title: "Annual Attendance",
        width: "800",
        height: "250",
        animation: {
          startup: true,
          duration: 2000,
          easing: "inAndOut"
        },
      };
      chart.draw(dataTable, options);
    });
  }

  //most visited location
  google.charts.setOnLoadCallback(drawPiChart);
  function drawPiChart() {

    var responseData = [];
    $.get("getMostVisitedLocation", function (response, status) {
      // alert("Data: " + response + "\nStatus: " + status);
      // responseData = response;

      responseData.push(['Location', 'Counts']);
      response.data.forEach(element => {
        console.log(element)
        responseData.push(element);
      });
      console.log('responsedata')
      console.log(responseData);

      var data = google.visualization.arrayToDataTable(responseData);

      var options = {
        title: 'Most Visited Locations',
        width: "800",
        height: "250",
        animation: {
          startup: true,
          duration: 800,
          easing: "inAndOut"
        },
      };

      var chart = new google.visualization.PieChart(document.getElementById('chart-bar-location-most-visit'));

      chart.draw(data, options);
    });
  }


  // link : https://developers.google.com/chart/interactive/docs/datesandtimes
  // time line chart for each day . month
  google.charts.load('current', { 'packages': ['timeline'] });
  google.charts.setOnLoadCallback(drawChart);
  function drawChart() {

    var responseData = [];
    responseData.push(['Location', 'Start Time', 'End Time'])
    $.get("getTimeLineByLocation", function (response, status) {

      response.data.forEach(element => {
        console.log('timeline')
        console.log(element) //[('01-01-2021', '02:36:01', '03:39:10', 'Corridor1')...]
        responseData.push([
          element[3],
          new Date(
            element[0].split('-')[2], element[0].split('-')[1], element[0].split('-')[0],
            element[1].split(':')[0], element[1].split(':')[1], element[1].split(':')[2]
          ),
          new Date(
            element[0].split('-')[2], element[0].split('-')[1], element[0].split('-')[0],
            element[2].split(':')[0], element[2].split(':')[1], element[2].split(':')[2]
          ),
        ]);
        // responseData.push([element]);
      });

      console.log('responsedata');
      console.log(responseData);

      var data = google.visualization.arrayToDataTable(responseData);

      var options = {
        height: 450,
        width: 900,
      };

      var chart = new google.visualization.Timeline(document.getElementById('timeline-chart_div'));

      chart.draw(data, options);


    });
  }


  // BAR CHART //
  google.charts.load('current', { packages: ['corechart', 'bar'] });
  google.charts.setOnLoadCallback(drawBasic);

  function drawBasic() {

    var data = google.visualization.arrayToDataTable([
      ['Locations', 'Occurences',],
      ['Lab1', 1],
      ['Lab2', 2],
      ['Corridor1', 3],
      ['GateIn', 5],
      ['GateOut', 8],
    ]);

    var options = {
      orientation: 'horizontal',
      title: '62445 occurences overall',
      // chartArea: { width: '100%' },
      hAxis: {
        title: 'Locations',
        minValue: 0
      },
      legend: { position: 'top' },
      
      vAxis: {
        title: 'Occurences'
      }
    };

    var chart = new google.visualization.BarChart(document.getElementById('occurence-bar-chart_div'));

    chart.draw(data, options);
  }

  // ================ Stepped Area Chart for location occurences with date
  google.charts.load('current', {'packages':['corechart']});
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {

    $.get("getTimeLineByLocation", function (response, status) {
      
    var data = google.visualization.arrayToDataTable([
      ['Date',  'Corridor1', 'Corridor2','Lab1','Lab6'],
      ['12-1-2021', 8.4,         7.9	,		6.7		,		8.9],
      ['13-1-2021',     6.9,         6.5	,		6		,		8],
      ['14-1-2021',        6.5,         6.4	,		5.2		,		9],
      ['15-1-2021',      4.4,         6.2	,		5		,		2]
    ]);

    var options = {
      title: 'The decline of \'The 39 Steps\'',
      vAxis: {title: 'Accumulated Rating'},
      chartArea: { width: '100%' },
      isStacked: true,
      legend: { position: 'bottom' },

      connectSteps: false
    };

    var chart = new google.visualization.SteppedAreaChart(document.getElementById('location-stepped-chart_div'));

    chart.draw(data, options);
  });
}
});