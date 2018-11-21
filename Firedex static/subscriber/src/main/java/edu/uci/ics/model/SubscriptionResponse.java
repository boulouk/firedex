package edu.uci.ics.model;

import java.util.List;

public class SubscriptionResponse {
	private String identifier;
	private List<FiredexSubscription> firedexSubscriptions;
	
	public SubscriptionResponse(String identifier, List<FiredexSubscription> firedexSubscriptions) {
		this.identifier = identifier;
		this.firedexSubscriptions = firedexSubscriptions;
	}
	
	public String getIdentifier() {
		return (identifier);
	}
	
	public List<FiredexSubscription> getFiredexSubscriptions() {
		return (firedexSubscriptions);
	}
	
}
