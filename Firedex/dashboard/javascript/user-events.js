$( document ).ready(function() {

  $("#section-graph").hide();

  $("#button-events").click(function() {
    $("#section-table").show();
    $("#section-graph").hide();
  });

  $("#button-bandwidth").click(function() {
    $("#section-table").hide();
    $("#section-graph").show();
  });

})

var server = "127.0.0.1";
var port = 8888;
var webSocket;

$(document).ready(
	function() {
		var topics = [ {text: "Smoke", value: "smoke"}, {text: "Fire", value: "fire"}, {text: "Temperature", value: "temperature"} ];
		$.each( topics, function(i, element) {
			$("#select-topic").append( new Option(element.text, element.value) );
		});
		$("#select-topic").prop("selectedIndex", 0);

		webSocket = new WebSocket("ws://" + server + ":" + port + "/");
		webSocket.onerror = function() {
			updateSelect();
		}
		webSocket.onopen = function() {
			initialize();
			$(window).on("beforeunload", function() {
		    	disconnect();
			});
      startAnalysis();
		}
		webSocket.onmessage = function(event) {
			handleMessage( event.data );
		}
		$(".subscribe").click(
			function() {
				var topic = $("#select-topic").val();
				var priority = $("#select-priority").val();
				if ( topic == null || priority == null )
					alert("Insert topic and priority!");
				else {
					subscribe(topic, priority);
				}
			}
		);

	}
);
var initialize = function() {
	priorityService();
}
var priorityService = function() {
	var request = new Object();
	request.type = "priorityService";
	var priorityMessage = new Object();
	priorityMessage.message = "Get all priorities";
	var strPriorityMessage = JSON.stringify(priorityMessage);
	request.content = strPriorityMessage;
	var requestMessage = new Object();
	requestMessage.request = request;
	var strMessage = JSON.stringify(requestMessage);
	webSocket.send(strMessage);
}
var subscribe = function(topic, priority) {
	var request = new Object();
	request.type = "subscribe";
	var subscribeMessage = new Object();
	var subscription = new Object();
	subscription.topic = topic;
	subscription.priority = priority;
	subscribeMessage.subscription = subscription;
	var strSubscribeMessage = JSON.stringify(subscribeMessage);
	request.content = strSubscribeMessage;
	var requestMessage = new Object();
	requestMessage.request = request;
	var strMessage = JSON.stringify(requestMessage);
	webSocket.send(strMessage);
	var html = "<tr>"
		+ "<td class='topicColumn'>" + topic + "</td>"
		+ "<td class='priorityColumn'>" + priority + "</td>"
		+ "<td>" + "<input class='delete' type='button' value='Unsubscribe'>" + "</td>"
		+ "</tr>";
	$('#topics > tbody:last-child').append(html);
	$('.delete').click(
		function() {
			var item = $(this).closest("tr");
			var topic = item.find(".topicColumn").html();
			var priority = item.find(".priorityColumn").html();
			unsubscribe(topic, priority);
			item.remove();
		}
	);
}
var unsubscribe = function(topic, priority) {
	var request = new Object();
	request.type = "unsubscribe";
	var unsubscribeMessage = new Object();
	var unsubscription = new Object();
	unsubscription.topic = topic;
	unsubscription.priority = priority;
	unsubscribeMessage.unsubscription = unsubscription;
	var strUnsubscribeMessage = JSON.stringify(unsubscribeMessage);
	request.content = strUnsubscribeMessage;
	var requestMessage = new Object();
	requestMessage.request = request;
	var strMessage = JSON.stringify(requestMessage);
	webSocket.send(strMessage);
}
var disconnect = function() {
	var request = new Object();
	request.type = "disconnect";
	var disconnectMessage = new Object();
	disconnectMessage.message = "Disconnect from all connections.";
	var strDisconnectMessage = JSON.stringify(disconnectMessage);
	request.content = strDisconnectMessage;
	var requestMessage = new Object();
	requestMessage.request = request;
	var strMessage = JSON.stringify(requestMessage);
	webSocket.send(strMessage);
}
var handleMessage = function(strMessage) {
	var object = JSON.parse(strMessage);
	if ( "priorities" in object ) {
		var priorities = object.priorities;
		priorityMessage(priorities);
	} else if ( "event" in object ) {
    count = count + 1;
		var event = object.event;
		eventMessage(event);
	}
}
var priorityMessage = function(priorities) {
	$.each( priorities, function(i, element) {
		$("#select-priority").append( new Option(element.priorityLevel, element.priorityLevel) );
	});
	$("#select-priority").prop("selectedIndex", 0);
	updateSelect();
}

var eventMessage = function(event) {
	var topic = event.topic;
	var priority = event.priority;
	var value = event.value;
	var status = event.status;
	var time = event.time;
	var device = event.device;
	var source = event.source;
	var type = "";
	if ( priority == 0 )
		type = "red";
	else if ( priority == 1 || priority == 2 )
		type = "yellow";
	else if ( priority == 3 )
		type = "green";
	var html = "<tr class='" + type + "''>"
		+ "<td>" + topic + "</td>"
		+ "<td>" + priority + "</td>"
		+ "<td>" + value + "</td>"
		+ "<td>" + status + "</td>"
		+ "<td>" + time + "</td>"
		+ "<td>" + device + "</td>"
		+ "<td>" + source + "</td>"
		+ "</tr>";
	$('#events > tbody:last-child').append(html);
}

var labels = ["t-9", "t-8", "t-7", "t-6", "t-5", "t-4", "t-3", "t-2", "t-1", "t"];
var data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
var count = 0;
var interval = 1000;

function startAnalysis() {
  for ( var i = 1; i < 10; i++ )
    data[i - 1] = data[i];
  data[9] = count;
  count = 0;
  drawChart(labels, data);
  console.log("refresh");
  setTimeout(function(){ startAnalysis(); }, interval);
}
