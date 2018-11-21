package edu.uci.ics.model.middleware;

public class SubscriptionCompletion {
	private String identifier;
	private String host;
	
	public SubscriptionCompletion(String identifier, String host) {
		this.identifier = identifier;
		this.host = host;
	}
	
	public String getIdentifier() {
		return (identifier);
	}
	
	public String getHost() {
		return (host);
	}
	
}
