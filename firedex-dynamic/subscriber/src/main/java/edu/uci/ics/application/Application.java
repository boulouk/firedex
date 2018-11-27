package edu.uci.ics.application;

import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ScheduledThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

import edu.uci.ics.configuration.Configuration;
import edu.uci.ics.configuration.Subscription;
import edu.uci.ics.configuration.Unsubscription;
import edu.uci.ics.exception.FiredexException;
import edu.uci.ics.model.result.SubscriberResult;
import edu.uci.ics.subscriber.Subscriber;
import edu.uci.ics.utility.JsonUtility;
import edu.uci.ics.utility.LoggerUtility;

public class Application {

	public static void main(String[] args) {
		try {
			String configurationFile = args[0];
			Configuration configuration = configuration(configurationFile);
			
			initializeApplication(configuration);
			
			Subscriber subscriber = new Subscriber(configuration);
			subscriber.connect();
			
			int startAfter = configuration.getSubscriber().getStartAfter() * 1000;
			Thread.sleep(startAfter);
			
			Map<Integer, List<Subscription>> mapSubscriptions = new HashMap<>();
			List<Subscription> subscriptions = configuration.getSubscriber().getSubscriptions();

			for ( Subscription subscription : subscriptions ) {
				int time = subscription.getTime();
				if ( !mapSubscriptions.containsKey(time) )
					mapSubscriptions.put( time, new ArrayList<>() );
				
				List<Subscription> subscriptionsByTime = mapSubscriptions.get(time);
				subscriptionsByTime.add(subscription);
			}
			
			Map<Integer, List<Subscription>> mapModifications = new HashMap<>();
			List<Subscription> modifications = configuration.getSubscriber().getModifications();

			for ( Subscription modification : modifications ) {
				int time = modification.getTime();
				if ( !mapModifications.containsKey(time) )
					mapModifications.put( time, new ArrayList<>() );
				
				List<Subscription> modificationsByTime = mapModifications.get(time);
				modificationsByTime.add(modification);
			}
			
			Map<Integer, List<Unsubscription>> mapUnsubscriptions = new HashMap<>();
			List<Unsubscription> unsubscriptions = configuration.getSubscriber().getUnsubscriptions();

			for ( Unsubscription unsubscription : unsubscriptions ) {
				int time = unsubscription.getTime();
				if ( !mapUnsubscriptions.containsKey(time) )
					mapUnsubscriptions.put( time, new ArrayList<>() );
				
				List<Unsubscription> unsubscriptionsByTime = mapUnsubscriptions.get(time);
				unsubscriptionsByTime.add(unsubscription);
			}
			
			ScheduledThreadPoolExecutor scheduler = new ScheduledThreadPoolExecutor(1);
			
			for ( int time : mapSubscriptions.keySet() ) {
				List<Subscription> subscriptionsByTime = mapSubscriptions.get(time);
				scheduler.schedule( () -> subscribe(subscriber, subscriptionsByTime), time, TimeUnit.SECONDS);
			}
			
			for ( int time : mapModifications.keySet() ) {
				List<Subscription> modificationsByTime = mapModifications.get(time);
				scheduler.schedule( () -> modify(subscriber, modificationsByTime), time, TimeUnit.SECONDS);
			}
			
			for ( int time : mapUnsubscriptions.keySet() ) {
				List<Unsubscription> unsubscriptionsByTime = mapUnsubscriptions.get(time);
				scheduler.schedule( () -> unsubscribe(subscriber, unsubscriptionsByTime), time, TimeUnit.SECONDS);
			}
						
			int runningTime = configuration.getSubscriber().getRunningTime() * 1000;
			Thread.sleep(runningTime);

			subscriber.disconnect();
			
			String outputFile = configuration.getOutput().getOutputFile();
			PrintWriter output = new PrintWriter(outputFile);
			
			SubscriberResult subscriberResult = subscriber.subscriberResult();
			String result = JsonUtility.toJson(subscriberResult);
			output.println(result);
			
			output.close();
			
			terminateApplication();

			System.exit(0);
		} catch (Exception exception) {
			System.out.println("Something bad happened.");
		}
	}
	
	private static Configuration configuration(String configurationFile) throws FiredexException {
		Configuration configuration = Configuration.initialize(configurationFile);
		return (configuration);
	}
	
	private static void initializeApplication(Configuration configuration) {
		LoggerUtility.initialize(configuration);
	}
	
	private static void subscribe(Subscriber subscriber, List<Subscription> subscriptions) {
		try {
			subscriber.subscribe(subscriptions);
		} catch (FiredexException exception) {
			System.out.println("Something bad happened.");
		}
	}
	
	private static void modify(Subscriber subscriber, List<Subscription> modifications) {
		try {
			subscriber.modify(modifications);
		} catch (FiredexException exception) {
			System.out.println("Something bad happened.");
		}
	}
	
	private static void unsubscribe(Subscriber subscriber, List<Unsubscription> unsubscriptions) {
		try {
			subscriber.unsubscribe(unsubscriptions);
		} catch (FiredexException exception) {
			System.out.println("Something bad happened.");
		}
	}
	
	private static void terminateApplication() {
		LoggerUtility.terminate();
	}

}
