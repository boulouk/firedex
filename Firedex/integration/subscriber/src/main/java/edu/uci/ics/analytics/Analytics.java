package edu.uci.ics.analytics;

import java.util.ArrayList;
import java.util.List;

import edu.uci.ics.model.SubscriptionConfiguration;

public class Analytics {
	private SubscriptionConfiguration subscriptionConfiguration;
	private List<String> events;
	private List<Integer> latencies;
	
	public Analytics(SubscriptionConfiguration subscriptionConfiguration) {
		this.subscriptionConfiguration = subscriptionConfiguration;
		events = new ArrayList<>();
		latencies = new ArrayList<>();
	}
	
	public SubscriptionConfiguration getSubscriptionConfiguration() {
		return (subscriptionConfiguration);
	}
	
	public void updateAnalytics(String event, int latency) {
		events.add(event);
		latencies.add(latency);
	}
	
	public int receivedMessages() {
		return ( events.size() );
	}
	
	public double getLatency() {
		if ( latencies.size() == 0 )
			return ( Double.NaN );
		
		int sum = 0;
		for ( int latency : latencies )
			sum = sum + latency;
		
		double average = (double) sum / (double) latencies.size();
		return (average);
	}

}
