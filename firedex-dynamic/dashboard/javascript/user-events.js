
var server = "10.0.0.6"; // 10.0.0.x
var port = 5000;
var webSocket;

var subscriptions = [];

$(document).ready(
	function() {
    connectToSubscriber();
    // simulateMessages();
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
	subscriptions.push(topic);
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
	subscriptions = subscriptions.filter(subscription => subscription != topic);
}

var disconnectFromSubscriber = function() {
	webSocket.close();
}

var handleMessage = function(strMessage) {
	var object = JSON.parse(strMessage);
	var topic = object.topic;
	var latency = object.latency;

	if ( !mapCurrentLatency.has(topic) )
		mapCurrentLatency.set(topic, 0);

	if ( !mapCurrentMessages.has(topic) )
		mapCurrentMessages.set(topic, 0);

	if (topic == "topic3")
		console.log("ricevuto");

	var currentLatency = mapCurrentLatency.get(topic);
	var currentMessages = mapCurrentMessages.get(topic);

	mapCurrentLatency.set(topic, currentLatency + latency);
	mapCurrentMessages.set(topic, currentMessages + 1);
}

var simulateMessages = function() {
	simulateTemperature();
	simulateSmoke();
	simulateWater();
}

var simulateTemperature = function() {
	var message = new Object();
	message.latency = 30;
	message.topic = "temperature"
	var strMessage = JSON.stringify(message);
	handleMessage(strMessage);

	setTimeout( function() { simulateTemperature(); }, 300);
}

var simulateSmoke = function() {
	var message = new Object();
	message.latency = 20;
	message.topic = "smoke"
	var strMessage = JSON.stringify(message);
	handleMessage(strMessage);

	setTimeout( function() { simulateSmoke(); }, 200);
}

var simulateWater = function() {
	var message = new Object();
	message.latency = 20;
	message.topic = "water"
	var strMessage = JSON.stringify(message);
	handleMessage(strMessage);

	setTimeout( function() { simulateWater(); }, 200);
}

var intervals = 60;
var interval = 1000;

var labels = [];
var colors = ["blue", "red", "green", "yellow", "orange", "purple", "brown"];

var mapCurrentLatency = new Map();
var mapCurrentMessages = new Map();

var mapLatencies = new Map();
var mapMessages = new Map();

function timeSeries() {
  for ( var i = 1; i < (intervals + 1); i++ )
    labels.push(i);

  analyze();
}

function analyze() {
	for ( const [topic, currentLatency] of mapCurrentLatency.entries() ) {
		var existsTopic = mapLatencies.has(topic);
		if ( !existsTopic ) {
			var topicLatencies = [];
			for ( var i = 1; i < (intervals + 1); i++ ) {
		    topicLatencies.push(0);
		  }
			mapLatencies.set(topic, topicLatencies);
		}

		var topicLatencies = mapLatencies.get(topic);
		for ( var i = 1; i < intervals; i++ )
			topicLatencies[i - 1] = topicLatencies[i];
		topicLatencies[intervals - 1] = currentLatency;
	}

	for ( const [topic, currentLatency] of mapCurrentMessages.entries() ) {
		var existsTopic = mapMessages.has(topic);
		if ( !existsTopic ) {
			var topicLatencies = [];
			for ( var i = 1; i < (intervals + 1); i++ ) {
		    topicLatencies.push(0);
		  }
			mapMessages.set(topic, topicLatencies);
		}

		var topicLatencies = mapMessages.get(topic);
		for ( var i = 1; i < intervals; i++ )
			topicLatencies[i - 1] = topicLatencies[i];
		topicLatencies[intervals - 1] = currentLatency;
	}

	for ( const topic of mapLatencies.keys() ) // same for mapMessages
		if ( subscriptions.indexOf(topic) == -1 ) {
			mapLatencies.delete(topic);
			mapMessages.delete(topic);
		}

	datasets = [];
	averageLatencyMessage = "";
	averageMessagesMessage = "";

	var index = 0;

	for ( const [topic, messages] of mapMessages.entries() ) {
		var sumMessages = 0;
		for ( const currentMessages of messages )
			sumMessages += currentMessages;
		var averageMessages = sumMessages / intervals;

		var topicLatencies = mapLatencies.get(topic);

		var averageLatency = 0;
		for ( const topicLatency of topicLatencies )
			averageLatency += topicLatency;

		if ( sumMessages != 0 )
			averageLatency /= sumMessages;

		averageLatency = Number(averageLatency).toFixed(2);
		averageMessages = Number(averageMessages).toFixed(2);

		var colorName = colors[index];
		averageLatencyMessage += topic + " (" + colorName + ")" + ": " + averageLatency + ", ";
		averageMessagesMessage += topic + " (" + colorName + ")" + ": " + averageMessages + ", ";
		index++;

		datasets.push(messages);
	}

	drawChart(labels, datasets);

	$("#averageLatency").text("Average latency: [" + averageLatencyMessage + "]")
	$("#averageMessages").text("Average messages: [" + averageMessagesMessage + "]");

	mapCurrentLatency = new Map();
	mapCurrentMessages = new Map();

  setTimeout( function() { analyze(); }, interval);
}
