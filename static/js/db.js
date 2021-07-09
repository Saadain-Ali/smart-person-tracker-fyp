
	$('.form-frienddummy').on('submit', function(event) {
		$(".mydata").text('');
		$.ajax({
			data : {
				name : $('#nameInput').val(),
				email : $('#emailInput').val()
			},
			type : 'POST',
			url : '/findFriend'
		})
		.done(function(data) {

			if (data.error) {
				$('#errorAlert').text(data.error).show();
				$('#successAlert').hide();
			}
			else {
				$('#successAlert').text(data.name).show();
				$('#errorAlert').hide();
			}

		});

		event.preventDefault();

	});

	// maximum occurence of a student
	$('.form-max').on('submit', function(event) {
		// $('.findMax').click(function(){
			$(".mydata").text('');
			$("#errorAlert").text('');
			$("#successAlert").text('');
			// $('.mydata').load(location.href + " .mydata");
			var sid = $('#inputUsername').val();
			$.ajax({
				url: '/findMax',
				data: $('.form-max').serialize(),
				type: 'POST'
			})
			.done(function(data) {

				if (data['results'].length <= 0) {
					console.log('not found');
					$('#errorAlert').text("not found").show();
					$('#successAlert').hide();
				}
				else {
					console.log(data);

					let arr = data['results']
					var table = $('<table id="myDataTable"><thead class="thead-dark fs-4"><tr><th>Name</th><th>Location</th><th>Date</th><th>count</th></tr></thead></table>').addClass('display table table-striped table-hover table-light fs-5 table-responsive-sm w-100');
					$('.mydata').append(table);

					$('#myDataTable').DataTable( {
						data: arr
					} );
					$("#myDataTable").removeClass("dataTable ");

					var head = $('<b>'+ sid + ' Max Occurences' + '</b>');
					google.charts.setOnLoadCallback(drawCalendarChart);
					drawCalendarChart();
					$("#successAlert").append(head);
					$('#errorAlert').hide();
				}
	
			});
			event.preventDefault();
		});

	// last scene location of a student 
	$('.form-lastseen').on('submit', function(event) {
			$(".mydata").text('');
			$("#errorAlert").text('');
			$("#successAlert").text('');
			
			
			$.ajax({
				url: '/stdsLastSeen',
				data: $('.form-lastseen').serialize(),
				type: 'POST'
			})
			.done(function(data) {
				if (data['status'] == 'Bad') {
					console.log('not found');
					$('#errorAlert').text("not found").show();
					$('#successAlert').hide();
				}
				else if((data['status'] == 'OK')) {
					// Sameer 62785 Unknown (NULL) 22:20:48 GateOut
					console.log(data);
					data = data['friends']
					let head = $('<p><b>'+ data[0] +'</b> is last seen at ' +data[5] + ' on ' + data[4] + '</p>');
					if(data[3] != null){head.append('<h5> with ' + data[2] + '</h5>')}
					$("#successAlert").append(head).show();		
					$('#errorAlert').hide();
				}
	
			});
			event.preventDefault();
	});
	

	// # most occurence of all students at one place
	// $('.findAllLoc').click(function(){
	$('.form-findAllLoc').on('submit', function(event) {
			event.preventDefault();
			$(".mydata").text('');
			$("#errorAlert").text('');
			$("#successAlert").text('');

			var location = $('#FALlocation').val();
			$(".mydata").text('');
			$.ajax({
				url: '/findAllAtOneLocation',
				data: $('.form-findAllLoc').serialize(),
				type: 'POST'
			})
			.done(function(data) {
				// debugger	
				if (data["status"] != 'OK') {
					console.log(data['status']);
					$('#errorAlert').text('Data not found').show();
					$('#successAlert').hide();
				}
				else {
					// data = [ (Haleem | 62987 | Ayaz | 62424 | 1 |) , () ]
					console.log(data);
					let arr = data['result'];
		
					var table = $('<table id="myDataTable"><thead class="thead-dark fs-4"><tr><th>student1</th><th>sid1</th><th>student2</th><th>sid2</th><th>occurence</th></tr></thead></table>').addClass('display table table-striped table-hover table-light fs-5 table-responsive-sm w-100');
					$('.mydata').append(table);
					
					$('#myDataTable').DataTable( {
						data: arr
					} );
					$("#myDataTable").removeClass("dataTable ");
					$('#successAlert').text('Occurence at ' + location ).show();		
					$('#errorAlert').hide();
				}
	
			});
	
			
	});
	
	// find who's friends with whom
	$('.form-studentFriend').on('submit' , function(event){
			$(".mydata").text('');
			$("#errorAlert").text('');
			$("#successAlert").text('');
			event.preventDefault();
			$.ajax({
				url: '/findAllFreinds',
				data: $('.form-studentFriend').serialize(),
				type: 'POST'
			})
			.done(function(data) {
				if (data['results'].length <= 0) {
					console.log("error : not found ");
					$('#errorAlert').text("Not Found").show();
					$('#successAlert').hide();
				}
				else {
				// Saadain,62445,Arbaz,62647,16
					
				console.log(data);
					var arrr = data['results'];
					
					var table = $('<table id="myDataTable" style="font-size:10px;"><thead class="thead-dark fs-4"><tr><th>Name</th><th>Date</th><th>Ariving</th><th>ALocation</th><th>Leaving</th><th>LDetect</th></tr></thead></table>').addClass('table table-striped table-hover table-light fs-5 table-responsive-sm w-100');
					// var table = $('<table id="myDataTable"><thead><tr><th>student1</th><th>sid1</th><th>student2</th><th>sid2</th><th>occurence</th></tr></thead></table>').addClass('display');
					$('.mydata').append(table);
					
					$('#myDataTable').DataTable( {
						data: arrr
					} );
					$('#successAlert').text('Occurence at ' + location ).show();		
					$('#errorAlert').hide();



				// console.log(data['results']);
				// let values = data['results'];
				// 	var table = $('<table id="myDataTable"><thead><tr><th>Name</th><th>Date</th><th>Ariving</th><th>ALocation</th><th>Leaving</th><th>LDetect</th></tr></thead></table>').addClass('display');
				// 	$('.mydata').append(table);

				// 	$('#myDataTable').DataTable( {
				// 		data: values
				// 	} );

				// 	$('.mydata').append(table);
				// 	$('#successAlert').append('In out Time').show();			
				// 	$('#errorAlert').hide();
				}
				
				});
	
			});


	// find route by date and sid
	$('.form-route').on('submit',function(event){
		$(".mydata").text('');
		$("#errorAlert").text('');
		$("#successAlert").text('');
		event.preventDefault();

		$.ajax({
			url: '/findRoute',
			data: $('.form-route').serialize(),
			type: 'POST',
			success: function(data){
				
			},
			error: function(error){
				
			}
		})
		.done(function(data) {
			// debugger	
			if (data["status"] != 'OK' || data['result'] == [] || data['result'] == null) {
				console.log("error:  no result");
				$('#errorAlert').text("No Result").show();
				$('#successAlert').hide();
			}
			else {
				// Saadain,62445,Arbaz,62647,16
				console.log(data['result']);
				$(".mydata").text('');
				let arr = data['result'];
				var table = $('<table><thead class="thead-dark fs-4"><th>student1</th><th>sid1</th><th>student2</th><th>sid2</th><th>occurence</th></thead></table>').addClass('table table-striped table-hover table-light fs-5 table-responsive-sm w-100');
				for(i=0; i<arr.length; i++){
					var row = $('<tr></tr>');
					for(j=0; j<arr[i].length; j++){
						var row1 = $('<td></td>').addClass('bar').text(arr[i][j]);
						table.append(row);
						row.append(row1);
					}
				}
				myRouteTimeLine(data['result'])
				$('.mydata').append(table);
				$('#successAlert').text('Occurence : ' + arr.length).show();			
				$('#errorAlert').hide();
			}
	});
	});

	// find route of two students by date using sid
	$('.form-friendOccur').on('submit',function(event){
		event.preventDefault();
		
		$(".mydata").text('');
		$("#errorAlert").text('');
		$("#successAlert").text('');
		
		$.ajax({
			url: '/findFriendOccur',
			data: $('.form-friendOccur').serialize(),
			type: 'POST'
		})
		.done(function(data) {
			// debugger	
			if (data["status"] != 'OK' || data['friends'] == [] || data['friends'].length <= 0) {
				console.log("error: no results ");
				$('#errorAlert').text("error: no results ").show();
				$('#successAlert').hide();
			}
			else {
				var dataToSend = []
		
				console.log(data['friends']);
				$(".mydata").text('');
				var arr = data['friends'];
				var head = $('<b>'+arr[0][0]+' found with ' + arr[0][1] +'</b>')
				$('#successAlert').append(head).show();
				for(j=0; j<arr.length; j++){
					var row1 = $('<h5></h5>').addClass('').text(arr[j][2]+' | ' + arr[j][3] );
					dataToSend.push([arr[j][2] , arr[j][3]])
					
					$('.mydata').append(row1);
				}
				
				console.log(dataToSend)
				drawPiChart(dataToSend);
							
				$('#errorAlert').hide();
			}

		});
	});
			

	// find route by date and sid
	$('.form-Clocked').on('submit',function(event){
		
		$(".mydata").text('');
			$("#errorAlert").text('');
			$("#successAlert").text('');
			event.preventDefault();
		$.ajax({
			url: '/findClockedInOut',
			data: $('.form-Clocked').serialize(),
			type: 'POST'
		})
		.done(function(data) {
			// debugger	
			if (data["status"] != 'OK' || data['result'] == [] || data['result'] == null){
				console.log("error:  no result");
				$('#errorAlert').text("No Result").show();
				$('#successAlert').hide();
			}
			else {
				// # 62445 18-12-2020 18:45:57 Corridor1 22:20:41 Corridor1
				console.log(data['result']);
				$(".mydata").text('');
				let arr = data['result'];
				var table = $('<table><thead class="thead-dark fs-4"><th>SID</th><th>Date</th><th>ArrivingTime</th><th>Location</th><th>LeavingDate</th><th>Location</th></thead></table>').addClass('table table-striped table-hover table-light fs-5 table-responsive-sm w-100');
					var row = $('<tr></tr>');
					for(j=0; j<arr.length; j++){
						var row1 = $('<td></td>').addClass('bar').text(arr[j]);
						table.append(row);
						row.append(row1);
					}
				
					response = data['result']
				drawTimeChart(response[0],response[2],response[4],response[1])
				$('.mydata').append(table);
				$('#successAlert').text('Clocked Time').show();			
				$('#errorAlert').hide();
			}
		});
	});


	$('.form-Clocked_multi').on('submit',function(event){
		event.preventDefault();
		$(".mydata").text('');
			$("#errorAlert").text('');
			$("#successAlert").text('');
			
		$.ajax({
			url: '/findClockedmulti',
			data: $('.form-Clocked_multi').serialize(),
			type: 'POST'
		})
		.done(function(data) {
			// debugger	
			if (data["status"] != 'OK' || data['result'] == [] || data['result'] == null){
				console.log("error:  no result");
				$('#errorAlert').text("No Result").show();
				$('#successAlert').hide();
			}
			else {
				// # 62445 18-12-2020 18:45:57 Corridor1 22:20:41 Corridor1
				console.log(data['result']);
				$(".mydata").text('');
				let arr = data['result'];
				var table = $('<table><thead class="thead-dark fs-4"><th>SID</th><th>Date</th><th>ArrivingTime</th><th>Location</th><th>LeavingDate</th><th>Location</th></thead></table>').addClass('table table-striped table-hover table-light fs-5 table-responsive-sm w-100');
					var row = $('<tr></tr>');
					for(j=0; j<arr.length; j++){
						var row1 = $('<td></td>').addClass('bar').text(arr[j]);
						table.append(row);
						row.append(row1);
					}
				
					response = data['result']
				// drawTimeChart(response[0],response[2],response[4],response[1])
				$('.mydata').append(table);
				$('#successAlert').text('Clocked Time').show();			
				$('#errorAlert').hide();
			}
		});
	});




$('.nav-link').on('click',function(event) {
		console.log('clear chart')
		$('#chart-area').html('')
	});

	$(document).ready(function() {
		$("table").addClass('table table-striped table-hover table-light fs-5 table-responsive-sm w-100');
		$.ajax({
			url: '/getFinds',
			data : {
				status : 'OK',
			},
			type: 'POST'
		})
		.done(function(data)
		{
			if (data["status"] != 'OK' || data['result'] == [] || data['result'] == null){
				console.log("error:  no result");
				$('#errorAlert').text("No Result").show();
				$('#successAlert').hide();
			}
			else{
			var arr = data['result']
			$('#example').DataTable( {
				data: arr
			} );
			$("#example").removeClass("dataTable ");
			$("#example .thead").addClass('thead-dark fs-4')
			$(".dataTables_info").css("color","#fffbfb");
			$(".dataTables_wrapper .dataTables_paginate .paginate_button").attr('style', 'color: gray');
			$("  .dataTables_length,.dataTables_filter, .dataTables_wrapper .dataTables_info, .dataTables_wrapper .dataTables_processing, .dataTables_wrapper .dataTables_paginate ").attr('style', 'color: gray');
		}
		});

		$("select.location").change(function(){
			var selectedLocation = $(this).children("option:selected").val();
			// alert("You have selected the country - " + selectedLocation);
		});

		$(".date_picker").append(
			`
			<label>Select Date: </label>
			<div class="datepick input-group date dabba" data-date-format="dd-mm-yyyy">
			    <input class="form-control" type="text" class="form-control" name="date" placeholder="Date" autofocus readonly />
			    <span class="input-group-addon"><i class="glyphicon glyphicon-calendar p-3"></i></span>
			</div>
			`
		).css(
			`.date_picker label{margin-left: 20px;}
			.datepick{width:180px; margin: 0 20px 20px 20px;}
			.datepick > span:hover{cursor: pointer;}
			`
		);

		$(function () {
			$(".datepick").datepicker({ 
				  autoclose: true, 
				  todayHighlight: true
			}).datepicker('update', new Date());
		  });
	} );

	