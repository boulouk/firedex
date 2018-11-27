package edu.uci.ics.publisher;

import java.util.List;

import edu.uci.ics.configuration.Configuration;
import edu.uci.ics.configuration.Publication;
import edu.uci.ics.exception.FiredexException;
import edu.uci.ics.middleware.FiredexMiddleware;
import edu.uci.ics.model.Event;
import edu.uci.ics.model.middleware.PublicationCompletion;
import edu.uci.ics.model.middleware.PublicationIntention;
import edu.uci.ics.mqtt.BrokerConnection;
import edu.uci.ics.utility.LoggerUtility;

public class Publisher {
	private Configuration configuration;
	
	private FiredexMiddleware firedexMiddleware;
	private BrokerConnection brokerConnection;
	
	public Publisher(Configuration configuration) {
		this.configuration = configuration;
		
		this.firedexMiddleware = new FiredexMiddleware(configuration);
		this.brokerConnection = new BrokerConnection(configuration);
	}
	
	public Configuration getConfiguration() {
		return (configuration);
	}
	
	public void connect() throws FiredexException {
		String identifier = configuration.getPublisher().getIdentifier();
		List<Publication> publications = configuration.getPublisher().getPublications();
		PublicationIntention publicationIntention = new PublicationIntention(identifier, publications);
		firedexMiddleware.publicationIntention(publicationIntention);
		
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
		String identifier = configuration.getPublisher().getIdentifier();
		List<Publication> publications = configuration.getPublisher().getPublications();
		PublicationCompletion publicationCompletion = new PublicationCompletion(identifier, publications);
		firedexMiddleware.publicationCompleted(publicationCompletion);
		
		brokerConnection.disconnect();
	}

}
