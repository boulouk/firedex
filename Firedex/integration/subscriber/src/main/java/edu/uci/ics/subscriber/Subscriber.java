package edu.uci.ics.subscriber;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import edu.uci.ics.analytics.SubscriberAnalytics;
import edu.uci.ics.configuration.Configuration;
import edu.uci.ics.configuration.Subscription;
import edu.uci.ics.exception.FiredexException;
import edu.uci.ics.middleware.FiredexMiddleware;
import edu.uci.ics.model.Event;
import edu.uci.ics.model.SubscriptionConfiguration;
import edu.uci.ics.mqtt.BrokerConnection;
import edu.uci.ics.mqtt.BrokerConnectionFactory;
import edu.uci.ics.utility.JsonUtility;
import edu.uci.ics.utility.LoggerUtility;

public class Subscriber {
	private Configuration configuration;
	
	private FiredexMiddleware firedexMiddleware;
	private List<BrokerConnection> brokerConnections;
	
	private SubscriberAnalytics subscriberAnalytics;
	
	public Subscriber(Configuration configuration) throws FiredexException {
		this.configuration = configuration;
		
		this.firedexMiddleware = new FiredexMiddleware(configuration);
		this.brokerConnections = new ArrayList<>();
		
		this.subscriberAnalytics = null;
	}
	
	public SubscriberAnalytics getSubscriberAnalytics() {
		return (subscriberAnalytics);
	}
	
	public void connect() throws FiredexException {
		
	}
	
	public void subscribe(List<Subscription> subscriptions) throws FiredexException {
		List<SubscriptionConfiguration> subscriptionConfigurations = firedexMiddleware.subscriberConfiguration(subscriptions);
		for ( SubscriptionConfiguration subscriptionConfiguration : subscriptionConfigurations )
			subscribe(subscriptionConfiguration);
		
		this.subscriberAnalytics = new SubscriberAnalytics(subscriptionConfigurations);
	}
	
	private void subscribe(SubscriptionConfiguration subscriptionConfiguration) throws FiredexException {
		BrokerConnection byLocalPort = byLocalPort( subscriptionConfiguration.getPort() );
		
		if ( byLocalPort == null ) {
			byLocalPort = createBrokerConnection( subscriptionConfiguration.getPort() );
			byLocalPort.addOnEventListener( (subscription, message) -> onEvent(subscription, message) );
			
			byLocalPort.connect();
			brokerConnections.add(byLocalPort);
		}
		
		byLocalPort.subscribe(subscriptionConfiguration);
	}
	
	private BrokerConnection createBrokerConnection(int localPort) throws FiredexException {
		String type = configuration.getSubscriber().getType();
		BrokerConnection brokerConnection = BrokerConnectionFactory.create(type, configuration, localPort);
		return (brokerConnection);
	}
	
	private BrokerConnection byLocalPort(int localPort) {
		for ( BrokerConnection brokerConnection : brokerConnections )
			if ( brokerConnection.getLocalPort() == localPort )
				return (brokerConnection);
		return (null);
	}
	
	public void disconnect() throws FiredexException {
		for ( BrokerConnection brokerConnection : brokerConnections )
			brokerConnection.disconnect();
	}
	
	private void onEvent(SubscriptionConfiguration subscriptionConfiguration, String message) {
		Event event = JsonUtility.fromJson(message, Event.class);
		
		long timestamp = ( new Date() ).getTime();
		int latency = (int) (timestamp - event.getTimestamp());
		subscriberAnalytics.updateAnalytics(subscriptionConfiguration, message, latency);
		
		StringBuilder log = new StringBuilder();
		
		log.append("---");
		log.append( System.getProperty("line.separator") );
		log.append("event: message on topic");
		log.append( System.getProperty("line.separator") );
		log.append( String.format("topic: %s", subscriptionConfiguration.getTopic()) );
		log.append( System.getProperty("line.separator") );
		log.append( String.format("port: %d", subscriptionConfiguration.getPort()) );
		log.append( System.getProperty("line.separator") );
		log.append("content: ");
		log.append( System.getProperty("line.separator") );
		log.append(event);
		log.append( System.getProperty("line.separator") );
		log.append("---");
		log.append( System.getProperty("line.separator") );
		
		LoggerUtility.log( message.toString() );
	}
	
}
