package edu.uci.ics.model.result;

import java.util.List;

import edu.uci.ics.configuration.Configuration;

public class SubscriberResult {
	private Configuration configuration;
	private List<SubscriptionResult> subscriptionsResult;
	
	public SubscriberResult(Configuration configuration, List<SubscriptionResult> subscriptionsResult) {
		this.configuration = configuration;
		this.subscriptionsResult = subscriptionsResult;
	}
	
	public Configuration getConfiguration() {
		return (configuration);
	}
	
	public List<SubscriptionResult> getSubscriptionsResult() {
		return (subscriptionsResult);
	}

}
