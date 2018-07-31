package edu.uci.ics.application;

import java.io.PrintWriter;
import java.util.List;

import edu.uci.ics.analytics.Analytics;
import edu.uci.ics.configuration.Configuration;
import edu.uci.ics.configuration.Subscription;
import edu.uci.ics.subscriber.Subscriber;

public class Application {

	public static void main(String[] args) throws Exception {
		String configurationFile = args[0];
		String outputFile = args[1];

		Configuration configuration = Configuration.initialize(configurationFile);

		Subscriber subscriber = new Subscriber(configuration);

		subscriber.connect();

		List<Subscription> subscriptions = configuration.getSubscriber().getSubscriptions();
		subscriber.subscribe(subscriptions);

		int runningTime = (configuration.getSubscriber().getRunningTime() + 10) * 1000;
		Thread.sleep(runningTime);

		subscriber.disconnect();

		PrintWriter output = new PrintWriter(outputFile);

		output.println("[");
		List<Analytics> analyticsList = subscriber.getSubscriberAnalytics().getAnalyticsList();
		for ( int i = 0; i < analyticsList.size(); i++ ) {
			Analytics analytics = analyticsList.get(i);
			
			String topic = analytics.getSubscriptionConfiguration().getTopic();
			int utilityFunction = analytics.getSubscriptionConfiguration().getUtilityFunction();
			int messages = analytics.receivedMessages();
			int latency = (int) analytics.getLatency();
			
			if ( i != (analyticsList.size() - 1) )
				output.print( String.format("   { \"topic\": \"%s\", \"utility_function\": \"%d\", \"messages\": \"%d\", \"latency\": \"%d\" }, ", topic, utilityFunction, messages, latency) );
			else
				output.print( String.format("   { \"topic\": \"%s\", \"utility_function\": \"%d\", \"messages\": \"%d\", \"latency\": \"%d\" } ", topic, utilityFunction, messages, latency) );
			output.println();
		}
		
		output.println("]");

		output.close();

		System.exit(0);
	}

}
