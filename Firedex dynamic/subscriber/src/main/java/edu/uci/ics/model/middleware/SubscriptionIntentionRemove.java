package edu.uci.ics.model.middleware;

import java.util.List;

public class SubscriptionIntentionRemove {
	private String identifier;
	private String host;
	
	private List<UnsubscriptionIntention> subscriptions;

	public SubscriptionIntentionRemove(String identifier, String host, List<UnsubscriptionIntention> subscriptions) {
		this.identifier = identifier;
		this.host = host;
		this.subscriptions = subscriptions;
	}
	
	public String getIdentifier() {
		return (identifier);
	}
	
	public String getHost() {
		return (host);
	}
	
	public List<UnsubscriptionIntention> getSubscriptions() {
		return (subscriptions);
	}

}
