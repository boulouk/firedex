package edu.uci.ics.subscriber;

import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import edu.uci.ics.configuration.Configuration;
import edu.uci.ics.configuration.Subscription;
import edu.uci.ics.exception.FiredexException;
import edu.uci.ics.middleware.FiredexMiddleware;
import edu.uci.ics.model.Event;
import edu.uci.ics.model.FiredexSubscription;
import edu.uci.ics.model.SubscriptionRequest;
import edu.uci.ics.model.SubscriptionResponse;
import edu.uci.ics.model.result.SubscriberResult;
import edu.uci.ics.model.result.SubscriptionResult;
import edu.uci.ics.mqtt.BrokerConnection;
import edu.uci.ics.utility.LoggerUtility;

public class Subscriber {
	private Configuration configuration;
	
	private FiredexMiddleware firedexMiddleware;
	private List<BrokerConnection> brokerConnections;
	
	private Map<String, Map<Integer, List<Long>>> subscriptionsLatencies;
	
	public Subscriber(Configuration configuration) throws FiredexException {
		this.configuration = configuration;
		
		this.firedexMiddleware = new FiredexMiddleware(configuration);
		this.brokerConnections = new ArrayList<>();
		
		this.subscriptionsLatencies = new HashMap<>();
	}
	
	public void connect() throws FiredexException {
		
	}
	
	public void subscribe(List<Subscription> subscriptions) throws FiredexException {
		String identifier = configuration.getSubscriber().getIdentifier();
		SubscriptionRequest subscriptionRequest = new SubscriptionRequest(identifier, subscriptions);
		SubscriptionResponse subscriptionResponse = firedexMiddleware.subscriptionRequest(subscriptionRequest);
		
		List<FiredexSubscription> firedexSubscriptions = subscriptionResponse.getFiredexSubscriptions();
		manageFiredexSubscriptions(firedexSubscriptions);
	}
	
	private void manageFiredexSubscriptions(List<FiredexSubscription> firedexSubscriptions) throws FiredexException {
		for ( FiredexSubscription firedexSubscription : firedexSubscriptions ) {
			String topic = firedexSubscription.getTopic();
			int port = firedexSubscription.getPort();
			
			if ( !subscriptionsLatencies.containsKey(topic) )
				subscriptionsLatencies.put( topic, new HashMap<>() );
			
			if ( !subscriptionsLatencies.get(topic).containsKey(port) )
				subscriptionsLatencies.get(topic).put( port, new ArrayList<>() );
			
			BrokerConnection byLocalPort = byPort(port);
			
			if ( byLocalPort == null ) {
				byLocalPort = new BrokerConnection(configuration, port);
				byLocalPort.addOnEventListener( (eventTopic, eventPort, eventContent) -> onEvent(eventTopic, eventPort, eventContent) );
				
				byLocalPort.connect();
				brokerConnections.add(byLocalPort);
			}
			
			byLocalPort.subscribe(topic);
		}
	}
	
	private BrokerConnection byPort(int port) {
		for ( BrokerConnection brokerConnection : brokerConnections )
			if ( brokerConnection.getPort() == port )
				return (brokerConnection);
		
		return (null);
	}

	public void disconnect() throws FiredexException {
		for ( BrokerConnection brokerConnection : brokerConnections )
			brokerConnection.disconnect();
		
		brokerConnections.clear();
	}
	
	private void onEvent(String topic, int port, Event event) {
		String publisher = event.getPublisher();
		long identifier = event.getIdentifier();
		long sent = event.getTimestamp();
		long received = ( new Date() ).getTime();
		long latency = ( received - sent );
		
		List<Long> subscriptionLatencies = subscriptionsLatencies.get(topic).get(port);
		subscriptionLatencies.add(latency);
		
		String message = String.format("%s, %d, %s, %d, %d, %d", topic, port, publisher, identifier, sent, received);
		LoggerUtility.log(message);
	}
	
	public SubscriberResult subscriberResult() {
		List<SubscriptionResult> subscriptionsResult = new ArrayList<>();
		
		for ( String topic : subscriptionsLatencies.keySet() )
			for ( int port : subscriptionsLatencies.get(topic).keySet() ) {
				List<Long> latencies = subscriptionsLatencies.get(topic).get(port);
				
				int messages = latencies.size();
				
				double averageLatency = 0;
				for ( long latency : latencies )
					averageLatency = averageLatency + latency;
				
				if ( messages != 0 )
					averageLatency = averageLatency / messages;
				
				SubscriptionResult subscriptionResult = new SubscriptionResult(topic, port, messages, averageLatency);
				subscriptionsResult.add(subscriptionResult);
			}
		
		SubscriberResult subscriberResult = new SubscriberResult(configuration, subscriptionsResult);
		return (subscriberResult);
	}
	
}
