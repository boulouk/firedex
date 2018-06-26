package ics.uci.edu.firedex.subscriber.mqtt;

import java.util.ArrayList;
import java.util.List;

import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;

import ics.uci.edu.firedex.subscriber.message.EventMessage;
import ics.uci.edu.firedex.subscriber.model.Event;
import ics.uci.edu.firedex.subscriber.model.MessageQueue;
import ics.uci.edu.firedex.subscriber.utilities.JsonUtility;

public class BrokerConnection {
	private String broker;
	private String identifier;
	private int priority;
	private List<String> topics;
	
	private MessageQueue messageQueue;
	
	private MqttClient client;
	
	public BrokerConnection(String broker, String baseIdentifier, int priority, MessageQueue messageQueue) throws MqttException {
		this.broker = broker;
		this.identifier = baseIdentifier + String.format("-%d", priority);
		this.priority = priority;
		this.topics = new ArrayList<>();
		
		this.messageQueue = messageQueue;
		
		this.client = new MqttClient(broker, identifier, null);
		MessageHandler messageHandler = new MessageHandler( (topic, message) -> handleMessage(topic, message) );
		this.client.setCallback(messageHandler);
	}
	
	public String getBroker() {
		return (broker);
	}
	
	public String getIdentifier() {
		return (identifier);
	}
	
	public int getPriority() {
		return (priority);
	}
	
	public void connect() throws MqttException {
		PriorityService priorityService = PriorityService.getInstance();
		int port = priorityService.getPort( getPriority() );
		
		MqttConnectOptions options = new MqttConnectOptions();
		options.setSocketFactory( new CustomSocketFactory(port) );
		this.client.connect(options);
	}
	
	private void handleMessage(String topic, String message) {
		EventMessage eventMessage = JsonUtility.fromJson(message, EventMessage.class);
		Event event = eventMessage.getEvent();
		event.setPriority( getPriority() );
		messageQueue.blockingPut(event);
	}
	
	public void subscribe(String topic) throws MqttException {
		client.subscribe(topic);
		topics.add(topic);
	}
	
	public void unsubscribe(String topic) throws MqttException {
		client.unsubscribe(topic);
		topics.remove(topic);
	}
	
	public void unsubscribeAll() throws MqttException {
		for ( String topic : topics )
			client.unsubscribe(topic);
		topics.clear();
	}

}
