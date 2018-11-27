
var server = "10.0.0.6"; // 10.0.0.x
var port = 5000;
var webSocket;

$(document).ready(
	function() {
    connectToSubscriber();
    timeSeries();
	}
);

var connectToSubscriber = function() {
  webSocket = new WebSocket("ws://" + server + ":" + port + "/");

  webSocket.onerror = function() {
    setTimeout( function() { connectToSubscriber(); } , 3000);
  };

  webSocket.onopen = function() {
    initialize();
  };
}

var initialize = function() {
  $(window).on("beforeunload", function() {
      disconnectFromSubscriber();
  });

  $(".subscribe").click(
    function() {
      var topic = $("#text-topic").val();
      var utilityFunction = $("#text-utility-function").val();
      if ( topic == null || utilityFunction == null )
        alert("Insert topic and priority!");
      else {
        subscribe(topic, utilityFunction);
      }
    }
  );

  webSocket.onmessage = function(event) {
    handleMessage( event.data );
  };

}

var subscribe = function(topic, utilityFunction) {
	var request = new Object();
	request.type = "subscribe";
	var content = new Object();
	content.topic = topic;
	content.utilityFunction = utilityFunction;
	var strContent = JSON.stringify(content);
	request.content = strContent;
	var strMessage = JSON.stringify(request);
	webSocket.send(strMessage);
	var html = "<tr>"
		+ "<td class='topicColumn'>" + topic + "</td>"
		+ "<td class='utilityFunctionColumn'>" + utilityFunction + "</td>"
		+ "<td>" + "<input class='delete' type='button' value='Unsubscribe'>" + "</td>"
		+ "</tr>";
	$('#topics > tbody:last-child').append(html);
	$('.delete').click(
		function() {
			var item = $(this).closest("tr");
			var topic = item.find(".topicColumn").html();
			var utilityFunction = item.find(".utilityFunction").html();
			unsubscribe(topic, utilityFunction);
			item.remove();
		}
	);
}

var unsubscribe = function(topic, priority) {
	var request = new Object();
	request.type = "unsubscribe";
	var content = new Object();
	content.topic = topic;
	var strContent = JSON.stringify(content);
	request.content = strContent;
	var strMessage = JSON.stringify(request);
	webSocket.send(strMessage);
}

var disconnectFromSubscriber = function() {
	webSocket.close();
}

var handleMessage = function(strMessage) {
	var object = JSON.parse(strMessage);
	var latency = object.latency;
	sumLatency += latency;
  count = count + 1;
	console.log(latency);
}

var intervals = 20;
var interval = 3000;

var labels = [];

var sumLatencies = [];
var messages = [];
var sumLatency = 0;
var count = 0;

function timeSeries() {
  for ( var i = 1; i < (intervals + 1); i++ ) {
    labels.push(i);

		sumLatencies.push(0);
    messages.push(0);
  }

  analyze();
}

function analyze() {
	for ( var i = 1; i < intervals; i++ )
		sumLatencies[i - 1] = sumLatencies[i];
	sumLatencies[intervals - 1] = sumLatency;

  for ( var i = 1; i < intervals; i++ )
    messages[i - 1] = messages[i];
  messages[intervals - 1] = count;

	averageLatency = 0;
	totalMessages = 0;

  averageMessages = 0;

  maximumMessages = -1;

  for ( var i = 0; i < intervals; i++ ) {
		currentSumLatency = sumLatencies[i];
		currentMessages = messages[i]

		averageLatency += currentSumLatency;
		totalMessages += currentMessages;

    averageMessages += currentMessages;

    if ( currentMessages > maximumMessages )
      maximumMessages = currentMessages;
  }

	if ( totalMessages != 0 )
		averageLatency /= totalMessages;

	if ( intervals != 0 )
  	averageMessages /= intervals;

	$("#averageLatency").text("Average latency: " + Number(averageLatency).toFixed(2))
  $("#averageMessages").text("Average messages: " + Number(averageMessages).toFixed(2));
  $("#maximumMessages").text("Maximum messages: " + maximumMessages);
  drawChart(labels, messages);

	sumLatency = 0;
  count = 0;

  setTimeout( function() { analyze(); }, interval);
}
