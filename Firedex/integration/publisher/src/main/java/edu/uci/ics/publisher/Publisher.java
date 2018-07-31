package edu.uci.ics.publisher;

import edu.uci.ics.configuration.Configuration;
import edu.uci.ics.exception.FiredexException;
import edu.uci.ics.model.Event;
import edu.uci.ics.mqtt.BrokerConnection;
import edu.uci.ics.utility.JsonUtility;
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
		String content = JsonUtility.toJson(event);
		brokerConnection.publish(topic, content, qualityOfService, retained);
		
		StringBuilder message = new StringBuilder();
		message.append("---");
		message.append( System.getProperty("line.separator") );
		message.append("event: publish");
		message.append( System.getProperty("line.separator") );
		message.append( String.format("topic: %s", topic) );
		message.append( System.getProperty("line.separator") );
		message.append( String.format("quality of service: %d", qualityOfService) );
		message.append( System.getProperty("line.separator") );
		message.append( String.format("retained: %b", retained) );
		message.append( System.getProperty("line.separator") );
		message.append("content: ");
		message.append( System.getProperty("line.separator") );
		message.append(content);
		message.append( System.getProperty("line.separator") );
		message.append("---");
		message.append( System.getProperty("line.separator") );
		
		LoggerUtility.log( message.toString() );
	}
	
	public void disconnect() throws FiredexException {
		brokerConnection.disconnect();
	}

}
