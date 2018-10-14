package edu.uci.ics.model;

import java.util.List;

import edu.uci.ics.configuration.Subscription;

public class SubscriptionRequest {
	private String identifier;
	private List<Subscription> subscriptions;
	
	public SubscriptionRequest(String identifier, List<Subscription> subscriptions) {
		this.identifier = identifier;
		this.subscriptions = subscriptions;
	}
	
	public String getIdentifier() {
		return (identifier);
	}
	
	public List<Subscription> getSubscriptions() {
		return (subscriptions);
	}
	
}
