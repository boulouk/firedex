package edu.uci.ics.model.middleware;

import java.util.List;

public class SubscriptionIntentionResponse {
	private String identifier;
	private String host;
	
	private List<FiredexSubscription> insertedSubscriptions;
	private List<ModifiedFiredexSubscription> modifiedSubscriptions;
	private List<FiredexSubscription> removedSubscriptions;
	
	public SubscriptionIntentionResponse(
										 String identifier, String host,
										 List<FiredexSubscription> insertedSubscriptions,
										 List<ModifiedFiredexSubscription> modifiedSubscriptions,
										 List<FiredexSubscription> removedSubscriptions
										)
	{
		this.identifier = identifier;
		this.host = host;
		
		this.insertedSubscriptions = insertedSubscriptions;
		this.modifiedSubscriptions = modifiedSubscriptions;
		this.removedSubscriptions = removedSubscriptions;
	}

	public String getIdentifier() {
		return (identifier);
	}
	
	public String getHost() {
		return (host);
	}
	
	public List<FiredexSubscription> getInsertedSubscriptions() {
		return (insertedSubscriptions);
	}
	
	public List<ModifiedFiredexSubscription> getModifiedSubscriptions() {
		return (modifiedSubscriptions);
	}
	
	public List<FiredexSubscription> getRemovedSubscriptions() {
		return (removedSubscriptions);
	}
	
}
