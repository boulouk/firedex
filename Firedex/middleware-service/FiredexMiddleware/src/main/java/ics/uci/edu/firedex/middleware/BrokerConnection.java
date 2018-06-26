package ics.uci.edu.firedex.middleware;

import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import ics.uci.edu.firedex.utilities.MessageUtility;

public class BrokerConnection {
	private String broker;
	private String identifier;
	
	private MqttClient client;
	
	public BrokerConnection(String broker, String identifier) throws MqttException {
		this.broker = broker;
		this.identifier = identifier;
		
		this.client = new MqttClient(broker, identifier, null);
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
	
	public void publish(String topic, String content, int qualityOfService, boolean retained) throws MqttException {
		MqttMessage message = new MqttMessage();
		message.setPayload( MessageUtility.toBytes(content) );
		message.setQos(qualityOfService);
		message.setRetained(retained);
		client.publish(topic, message);
	}
	
	public void disconnect() throws MqttException {
		client.disconnect();
	}

}
