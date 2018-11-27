package edu.uci.ics.application;

import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ScheduledThreadPoolExecutor;

import edu.uci.ics.configuration.Configuration;
import edu.uci.ics.configuration.Subscription;
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
			
			Map<Integer, List<Subscription>> mapSubscriptions = new HashMap<>();
			List<Subscription> subscriptions = configuration.getSubscriber().getSubscriptions();

			for ( Subscription subscription : subscriptions ) {
				int time = subscription.getTime();
				if ( !mapSubscriptions.containsKey(time) )
					mapSubscriptions.put( time, new ArrayList<>() );
				
				List<Subscription> subscriptionsByTime = mapSubscriptions.get(time);
				subscriptionsByTime.add(subscription);
			}
			
			@SuppressWarnings("unused")
			ScheduledThreadPoolExecutor scheduler = new ScheduledThreadPoolExecutor(1);
			
			for ( int time : mapSubscriptions.keySet() ) {
				List<Subscription> subscriptionsByTime = mapSubscriptions.get(time);
				// scheduler.schedule( () -> subscribe(subscriber, subscriptionsByTime), time, TimeUnit.SECONDS);
				subscribe(subscriber, subscriptionsByTime);
			}
			
			System.out.println("SUBSCRIBER: connected.");
			
			int runningTime = configuration.getSubscriber().getRunningTime() * 1000;
			Thread.sleep(runningTime);

			subscriber.disconnect();
			
			System.out.println("SUBSCRIBER: end subscriptions.");
			System.out.println("SUBSCRIBER: disconnected.");
			
			String outputFile = configuration.getOutput().getOutputFile();
			PrintWriter output = new PrintWriter(outputFile);
			
			SubscriberResult subscriberResult = subscriber.subscriberResult();
			String result = JsonUtility.toJson(subscriberResult);
			output.println(result);
			
			output.close();
			
			System.out.println("SUBSCRIBER: completed.");
			
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
	
	private static void terminateApplication() {
		LoggerUtility.terminate();
	}

}
