package ics.uci.edu.firedex.subscriber.mqtt;

import java.util.ArrayList;
import java.util.List;

import org.eclipse.paho.client.mqttv3.MqttException;

import ics.uci.edu.firedex.subscriber.model.MessageQueue;

public class Subscriber {
	private String broker;
	private String identifier;
	private MessageQueue messageQueue;
	
	private List<BrokerConnection> brokerConnections;
	
	public Subscriber(String broker, String identifier, MessageQueue messageQueue) throws MqttException {
		this.broker = broker;
		this.identifier = identifier;
		this.messageQueue = messageQueue;
		
		this.brokerConnections = new ArrayList<BrokerConnection>();
	}
	
	public String getBroker() {
		return (broker);
	}
	
	public String getIdentifier() {
		return (identifier);
	}
	
	public void subscribe(String topic, int priority) throws MqttException {
		for ( BrokerConnection brokerConnection : brokerConnections )
			if ( brokerConnection.getPriority() == priority ) {
				brokerConnection.subscribe(topic);
				return;
			}
		
		BrokerConnection brokerConnection = new BrokerConnection( getBroker(), getIdentifier(), priority, messageQueue );
		brokerConnection.connect();
		brokerConnection.subscribe(topic);
		
		brokerConnections.add(brokerConnection);
	}
	
	public void unsubscribe(String topic, int priority) throws MqttException {
		for ( BrokerConnection brokerConnection : brokerConnections )
			if ( brokerConnection.getPriority() == priority )
				brokerConnection.unsubscribe(topic);
	}
	
	public void unsubscribeAll() throws MqttException {
		for ( BrokerConnection brokerConnection : brokerConnections )
			brokerConnection.unsubscribeAll();
	}

}
