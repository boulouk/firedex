package edu.uci.ics.analytics;

import java.util.ArrayList;
import java.util.List;

import edu.uci.ics.model.SubscriptionConfiguration;
import edu.uci.ics.utility.LoggerUtility;

public class SubscriberAnalytics {
	private List<Analytics> analyticsList;
	
	public SubscriberAnalytics(List<SubscriptionConfiguration> subscriptionConfigurations) {
		analyticsList = new ArrayList<>();
		
		for ( SubscriptionConfiguration subscriptionConfiguration : subscriptionConfigurations )
			analyticsList.add( new Analytics(subscriptionConfiguration) );
	}
	
	public List<Analytics> getAnalyticsList() {
		return (analyticsList);
	}
	
	public void updateAnalytics(SubscriptionConfiguration subscriptionConfiguration, String event, int latency) {
		Analytics analytics = bySubscriptionConfiguration(subscriptionConfiguration);
		analytics.updateAnalytics(event, latency);
	}
	
	private Analytics bySubscriptionConfiguration(SubscriptionConfiguration subscriptionConfiguration) {
		for ( Analytics analytics : analyticsList ) {
			SubscriptionConfiguration currentSubscriptionConfiguration = analytics.getSubscriptionConfiguration();
			if ( currentSubscriptionConfiguration.getTopic().equals(subscriptionConfiguration.getTopic()) &&
				 currentSubscriptionConfiguration.getUtilityFunction() == subscriptionConfiguration.getUtilityFunction() && 
				 currentSubscriptionConfiguration.getPort() == subscriptionConfiguration.getPort() )
				
				return ( analytics );
		}
		
		return (null);
	}
	
	public void print() {
		StringBuilder message = new StringBuilder();
		
		message.append("---");
		message.append( System.getProperty("line.separator") );
		for ( Analytics analytics : analyticsList ) {
			String topic = analytics.getSubscriptionConfiguration().getTopic();
			int utilityFunction = analytics.getSubscriptionConfiguration().getUtilityFunction();
			int port = analytics.getSubscriptionConfiguration().getPort();
			message.append( String.format("topic: %s", topic) );
			message.append( System.getProperty("line.separator") );
			message.append( String.format("priority: %d", utilityFunction) );
			message.append( System.getProperty("line.separator") );
			message.append( String.format("priority: %d", port) );
			message.append( System.getProperty("line.separator") );
			message.append( String.format("messages: %d", analytics.receivedMessages()) );
			message.append( System.getProperty("line.separator") );
			message.append( String.format("latency: %1$,.2f", analytics.getLatency()) );
			message.append( System.getProperty("line.separator") );
			message.append( System.getProperty("line.separator") );
		}
		message.append("---");
		
		LoggerUtility.log( message.toString() );
	}

}
