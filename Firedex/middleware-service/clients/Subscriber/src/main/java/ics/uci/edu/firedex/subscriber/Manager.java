package ics.uci.edu.firedex.subscriber;

import java.util.ArrayList;
import java.util.List;

import org.eclipse.paho.client.mqttv3.MqttException;
import org.java_websocket.WebSocket;

import ics.uci.edu.firedex.subscriber.message.PriorityMessage;
import ics.uci.edu.firedex.subscriber.message.RequestMessage;
import ics.uci.edu.firedex.subscriber.message.SubscribeMessage;
import ics.uci.edu.firedex.subscriber.message.UnsubscribeMessage;
import ics.uci.edu.firedex.subscriber.model.MessageQueue;
import ics.uci.edu.firedex.subscriber.model.Priority;
import ics.uci.edu.firedex.subscriber.mqtt.PriorityService;
import ics.uci.edu.firedex.subscriber.mqtt.Subscriber;
import ics.uci.edu.firedex.subscriber.utilities.Global;
import ics.uci.edu.firedex.subscriber.utilities.JsonUtility;
import ics.uci.edu.firedex.subscriber.websocket.FiredexWebSocketServer;
import ics.uci.edu.firedex.subscriber.websocket.MessageForwarder;

public class Manager {
	private FiredexWebSocketServer firedexWebSocketServer;
	private PriorityService priorityService;
	private MessageQueue messageQueue;
	private MessageForwarder messageForwarder;
	private Subscriber subscriber;

	public Manager() { }

	public void start() throws MqttException {
		int port = Global.WEB_SOCKET_SERVER;
		
		String broker = Global.BROKER;
		String priorityIdentifier = Global.PRIORITY_CLIENT;
		String clientIdentifier = Global.CLIENT;
		
		// Creating FiredexWebSocketServer.
		firedexWebSocketServer = new FiredexWebSocketServer(port) {
			@Override
			public void onMessage(WebSocket webSocket, String message) {
				handleMessage(webSocket, message);
			}
		};
		firedexWebSocketServer.start();
		// ---

		// Initializing PriorityService
		priorityService = PriorityService.getInstance();		
		priorityService.initialize(broker, priorityIdentifier);
		// ---

		// Creating MessageQueue
		messageQueue = new MessageQueue();
		// ---

		// Creating MessageForwarder
		messageForwarder = new MessageForwarder(messageQueue, firedexWebSocketServer);
		messageForwarder.start();
		// ---
				
		// Creating Subscriber
		subscriber = new Subscriber(broker, clientIdentifier, messageQueue);
		// ---
	}

	private void handleMessage(WebSocket webSocket, String message) {
		RequestMessage requestMessage = JsonUtility.fromJson(message, RequestMessage.class);
		String type = requestMessage.getRequest().getType();
		String content = requestMessage.getRequest().getContent();
		
		if ( type.equals("priorityService") ) {
			while ( !priorityService.isInitialized() ) {
				try {
					Thread.sleep(100);
				} catch (InterruptedException exception) { }
			}
			
			List<Integer> priorityLevels = priorityService.getPriorities();
			List<Priority> priorities = new ArrayList<>();
			for (int priorityLevel : priorityLevels) {
				int priorityPort = priorityService.getPort(priorityLevel);
				Priority priority = new Priority(priorityLevel, priorityPort);
				priorities.add(priority);
			}
			
			PriorityMessage priorityMessage = new PriorityMessage(priorities);
			String response = JsonUtility.toJson(priorityMessage);
			webSocket.send(response);
		} else if ( type.equals("subscribe") ) {
			SubscribeMessage subscribeMessage = JsonUtility.fromJson(content, SubscribeMessage.class);
			String topic = subscribeMessage.getSubscription().getTopic();
			int priority = subscribeMessage.getSubscription().getPriority();
			
			try {
				subscriber.subscribe(topic, priority);
			} catch (MqttException exception) { }
		} else if ( type.equals("unsubscribe") ) {
			UnsubscribeMessage unsubscribeMessage = JsonUtility.fromJson(content, UnsubscribeMessage.class);
			String topic = unsubscribeMessage.getUnsubscription().getTopic();
			int priority = unsubscribeMessage.getUnsubscription().getPriority();
			
			try {
				subscriber.unsubscribe(topic, priority);
			} catch (MqttException exception) { }
		} else if ( type.equals("disconnect") ) {
			try {
				subscriber.unsubscribeAll();
				System.out.println("Unsubscribed from all topics");
			} catch (MqttException exception) { }
			messageQueue.clear();
		}
	}

}
