package edu.uci.ics.publisher;

import edu.uci.ics.configuration.Configuration;
import edu.uci.ics.exception.FiredexException;
import edu.uci.ics.model.Event;
import edu.uci.ics.mqtt.BrokerConnection;
import edu.uci.ics.utility.LoggerUtility;

public class Publisher {
	private BrokerConnection brokerConnection;
	
	public Publisher(Configuration configuration) {
		this.brokerConnection = new BrokerConnection(configuration);
	}
	
	public void connect() throws FiredexException {
		brokerConnection.connect();
	}
	
	public void publish(String topic, Event event, int qualityOfService, boolean retained) throws FiredexException {
		byte[] content = Event.serialize(event);
		brokerConnection.publish(topic, content, qualityOfService, retained);
		
		String publisher = event.getPublisher();
		long identifier = event.getIdentifier();
		long timestamp = event.getTimestamp();
		String message = String.format("%s, %s, %d, %d", publisher, topic, identifier, timestamp);
		LoggerUtility.log(message);
	}
	
	public void disconnect() throws FiredexException {
		brokerConnection.disconnect();
	}

}
