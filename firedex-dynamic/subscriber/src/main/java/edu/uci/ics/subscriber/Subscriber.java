package edu.uci.ics.subscriber;

import java.io.IOException;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import edu.uci.ics.configuration.Configuration;
import edu.uci.ics.configuration.Subscription;
import edu.uci.ics.configuration.Unsubscription;
import edu.uci.ics.exception.FiredexException;
import edu.uci.ics.middleware.FiredexMiddleware;
import edu.uci.ics.model.Event;
import edu.uci.ics.model.middleware.FiredexSubscription;
import edu.uci.ics.model.middleware.ModifiedFiredexSubscription;
import edu.uci.ics.model.middleware.SubscriptionCompletion;
import edu.uci.ics.model.middleware.SubscriptionIntention;
import edu.uci.ics.model.middleware.SubscriptionIntentionInsert;
import edu.uci.ics.model.middleware.SubscriptionIntentionModify;
import edu.uci.ics.model.middleware.SubscriptionIntentionRemove;
import edu.uci.ics.model.middleware.SubscriptionIntentionResponse;
import edu.uci.ics.model.middleware.UnsubscriptionIntention;
import edu.uci.ics.model.result.SubscriberResult;
import edu.uci.ics.model.result.SubscriptionResult;
import edu.uci.ics.model.web.WebEvent;
import edu.uci.ics.model.web.WebRequest;
import edu.uci.ics.mqtt.BrokerConnection;
import edu.uci.ics.subscriber.web.SubscriberEndPoint;
import edu.uci.ics.utility.JsonUtility;
import edu.uci.ics.utility.LoggerUtility;

public class Subscriber {
	private Configuration configuration;
	
	private FiredexMiddleware firedexMiddleware;
	private List<BrokerConnection> brokerConnections;
	private SubscriberEndPoint subscriberEndPoint;
	
	private Map<String, Map<Integer, List<Long>>> subscriptionsLatencies;
	
	public Subscriber(Configuration configuration) throws FiredexException {
		this.configuration = configuration;
		
		this.firedexMiddleware = new FiredexMiddleware(configuration);
		this.brokerConnections = new ArrayList<>();
		this.subscriberEndPoint = null;
		
		this.subscriptionsLatencies = new HashMap<>();
	}
	
	public void connect() throws FiredexException {
		boolean abilitate = configuration.getServer().getWeb().isAbilitate();
		if ( abilitate == true ) {
			int port = configuration.getServer().getWeb().getPort();
			try {
				subscriberEndPoint = new SubscriberEndPoint(port);
				subscriberEndPoint.setOnWebMessage( 
					(message) -> {
						WebRequest webRequest = JsonUtility.fromJson(message, WebRequest.class);
						if ( webRequest.getType().equals("subscribe") ) {
							Subscription subscription = JsonUtility.fromJson(webRequest.getContent(), Subscription.class);
							List<Subscription> subscriptions = new ArrayList<>();
							subscriptions.add(subscription);
							try {
								subscribe(subscriptions);
							} catch (FiredexException exception) {
								System.out.println("Something bad happened.");
							}
						}
						
						if ( webRequest.getType().equals("unsubscribe") ) {
							Unsubscription unsubscription = JsonUtility.fromJson(webRequest.getContent(), Unsubscription.class);
							List<Unsubscription> unsubscriptions = new ArrayList<>();
							unsubscriptions.add(unsubscription);
							try {
								unsubscribe(unsubscriptions);
							} catch (FiredexException exception) {
								System.out.println("Something bad happened.");
							}
						}
					}
				);
				
				subscriberEndPoint.start();
			} catch (UnknownHostException exception) {
				throw ( new FiredexException() );
			}
		}
	}
	
	public void subscribe(List<Subscription> subscriptions) throws FiredexException {
		String identifier = configuration.getSubscriber().getIdentifier();
		String host = configuration.getSubscriber().getHost();
		
		List<SubscriptionIntention> subscriptionsIntention = new ArrayList<>();
		for ( Subscription subscription : subscriptions ) {
			String topic = subscription.getTopic();
			double utilityFunction = subscription.getUtilityFunction();
			SubscriptionIntention subscriptionIntention = new SubscriptionIntention(topic, utilityFunction);
			subscriptionsIntention.add(subscriptionIntention);
		}
		
		SubscriptionIntentionInsert subscriptionIntentionInsert = new SubscriptionIntentionInsert(identifier, host, subscriptionsIntention);
		SubscriptionIntentionResponse subscriptionIntentionResponse = firedexMiddleware.subscriptionIntentionInsert(subscriptionIntentionInsert);
		
		manageSubscriptionIntentionResponse(subscriptionIntentionResponse);
		
		SubscriptionCompletion subscriptionCompletion = new SubscriptionCompletion(identifier, host);
		firedexMiddleware.subscriptionCompletion(subscriptionCompletion);
	}

	public void modify(List<Subscription> modifications) throws FiredexException {
		String identifier = configuration.getSubscriber().getIdentifier();
		String host = configuration.getSubscriber().getHost();
		
		List<SubscriptionIntention> subscriptionsIntention = new ArrayList<>();
		for ( Subscription modification : modifications ) {
			String topic = modification.getTopic();
			double utilityFunction = modification.getUtilityFunction();
			SubscriptionIntention subscriptionIntention = new SubscriptionIntention(topic, utilityFunction);
			subscriptionsIntention.add(subscriptionIntention);
		}
		
		SubscriptionIntentionModify subscriptionIntentionModify = new SubscriptionIntentionModify(identifier, host, subscriptionsIntention);
		SubscriptionIntentionResponse subscriptionIntentionResponse = firedexMiddleware.subscriptionIntentionModify(subscriptionIntentionModify);
		
		manageSubscriptionIntentionResponse(subscriptionIntentionResponse);
		
		SubscriptionCompletion subscriptionCompletion = new SubscriptionCompletion(identifier, host);
		firedexMiddleware.subscriptionCompletion(subscriptionCompletion);
	}
	
	public void unsubscribe(List<Unsubscription> unsubscriptions) throws FiredexException {
		String identifier = configuration.getSubscriber().getIdentifier();
		String host = configuration.getSubscriber().getHost();
		
		List<UnsubscriptionIntention> unsubscriptionsIntention = new ArrayList<>();
		for ( Unsubscription unsubscription : unsubscriptions ) {
			String topic = unsubscription.getTopic();
			UnsubscriptionIntention unsubscriptionIntention = new UnsubscriptionIntention(topic);
			unsubscriptionsIntention.add(unsubscriptionIntention);
		}
		
		SubscriptionIntentionRemove subscriptionIntentionRemove = new SubscriptionIntentionRemove(identifier, host, unsubscriptionsIntention);
		SubscriptionIntentionResponse subscriptionIntentionResponse = firedexMiddleware.subscriptionIntentionRemove(subscriptionIntentionRemove);
		
		manageSubscriptionIntentionResponse(subscriptionIntentionResponse);
		
		SubscriptionCompletion subscriptionCompletion = new SubscriptionCompletion(identifier, host);
		firedexMiddleware.subscriptionCompletion(subscriptionCompletion);
	}
	
	private void manageSubscriptionIntentionResponse(SubscriptionIntentionResponse subscriptionIntentionResponse) throws FiredexException {
		List<ModifiedFiredexSubscription> modifiedFiredexSubscriptions = subscriptionIntentionResponse.getModifiedSubscriptions();
		List<FiredexSubscription> insertedFiredexSubscriptions = subscriptionIntentionResponse.getInsertedSubscriptions();
		List<FiredexSubscription> removedFiredexSubscriptions = subscriptionIntentionResponse.getRemovedSubscriptions();
		
		manageModifiedFiredexSubscriptions(modifiedFiredexSubscriptions);
		manageInsertedFiredexSubscriptions(insertedFiredexSubscriptions);
		manageRemovedFiredexSubscriptions(removedFiredexSubscriptions);
	}
	
	private void manageModifiedFiredexSubscriptions(List<ModifiedFiredexSubscription> modifiedFiredexSubscriptions) throws FiredexException {
		if ( modifiedFiredexSubscriptions != null ) {
			for ( ModifiedFiredexSubscription modifiedFiredexSubscription : modifiedFiredexSubscriptions ) {
				String topic = modifiedFiredexSubscription.getTopic();
				int oldPort = modifiedFiredexSubscription.getOldPort();
				int newPort = modifiedFiredexSubscription.getNewPort();
				
				if ( !subscriptionsLatencies.containsKey(topic) )
					subscriptionsLatencies.put( topic, new HashMap<>() );
				
				if ( !subscriptionsLatencies.get(topic).containsKey(newPort) )
					subscriptionsLatencies.get(topic).put( newPort, new ArrayList<>() );
				
				BrokerConnection byLocalPort = byPort(oldPort);
				byLocalPort.unsubscribe(topic);
				
				byLocalPort = byPort(newPort);
				
				if ( byLocalPort == null ) {
					byLocalPort = new BrokerConnection(configuration, newPort);
					byLocalPort.addOnEventListener( (eventTopic, eventPort, eventContent) -> onEvent(eventTopic, eventPort, eventContent) );
					
					byLocalPort.connect();
					brokerConnections.add(byLocalPort);
				}
				
				byLocalPort.subscribe(topic);
			}
		}
	}
	
	private void manageInsertedFiredexSubscriptions(List<FiredexSubscription> insertedFiredexSubscriptions) throws FiredexException {
		if ( insertedFiredexSubscriptions != null ) {
			for ( FiredexSubscription insertedFiredexSubscription : insertedFiredexSubscriptions ) {
				String topic = insertedFiredexSubscription.getTopic();
				int port = insertedFiredexSubscription.getPort();
				
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
	}
	
	private void manageRemovedFiredexSubscriptions(List<FiredexSubscription> removedFiredexSubscriptions) throws FiredexException {
		if ( removedFiredexSubscriptions != null ) {
			for ( FiredexSubscription removedFiredexSubscription : removedFiredexSubscriptions ) {
				String topic = removedFiredexSubscription.getTopic();
				int port = removedFiredexSubscription.getPort();
				
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
				
				byLocalPort.unsubscribe(topic);
			}
		}
	}
	
	private BrokerConnection byPort(int port) {
		for ( BrokerConnection brokerConnection : brokerConnections )
			if ( brokerConnection.getPort() == port )
				return (brokerConnection);
		
		return (null);
	}

	public void disconnect() throws FiredexException {
		List<Unsubscription> unsubscriptions = new ArrayList<>();
		for ( BrokerConnection brokerConnection : brokerConnections ) {
			List<String> subscriptions = brokerConnection.getSubscriptions();
			for ( String subscription : subscriptions ) {
				String topic = subscription;
				int dummyTime = -1;
				Unsubscription unsubscription = new Unsubscription(topic, dummyTime);
				unsubscriptions.add(unsubscription);
			}
		}
		unsubscribe(unsubscriptions);
		
		for ( BrokerConnection brokerConnection : brokerConnections )
			brokerConnection.disconnect();
		
		brokerConnections.clear();
		
		boolean abilitate = configuration.getServer().getWeb().isAbilitate();
		if ( abilitate == true )
			try {
				subscriberEndPoint.stop();
			} catch (IOException | InterruptedException exception) {
				throw ( new FiredexException() );
			}
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
		
		boolean abilitate = configuration.getServer().getWeb().isAbilitate();
		if ( abilitate == true ) {
			WebEvent webEvent = new WebEvent(publisher, identifier, topic, port, sent, received, latency);
			String strWebEvent = JsonUtility.toJson(webEvent);
			subscriberEndPoint.sendMessage(strWebEvent);
		}
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
