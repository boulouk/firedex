package ics.uci.edu.firedex.subscriber.mqtt;

import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;

public class PriorityConnection {
	private String broker;
	private String identifier;
	
	private MqttClient client;
	
	public PriorityConnection(String broker, String identifier, MessageHandler messageHandler) throws MqttException {
		this.broker = broker;
		this.identifier = identifier;
		
		this.client = new MqttClient(broker, identifier, null);
		this.client.setCallback(messageHandler);
	}
	
	public String getBroker() {
		return (broker);
	}
	
	public String getIdentifier() {
		return (identifier);
	}
	
	public void connect() throws MqttException {
		client.connect();
	}
	
	public void subscribe(String topic) throws MqttException {
		client.subscribe(topic);
	}
	
	public void disconnect() throws MqttException {
		client.disconnect();
	}

}
