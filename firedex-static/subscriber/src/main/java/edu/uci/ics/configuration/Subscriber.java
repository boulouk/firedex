package edu.uci.ics.configuration;

import java.util.List;

public class Subscriber {
	private String identifier;
	private String host;
	private int runningTime;
	
	private List<Subscription> subscriptions;
	
	public Subscriber(String identifier, String host, int runningTime, List<Subscription> subscriptions) {
		this.identifier = identifier;
		this.host = host;
		this.runningTime = runningTime;
		
		this.subscriptions = subscriptions;
	}

	public String getIdentifier() {
		return (identifier);
	}
	
	public String getHost() {
		return (host);
	}
	
	public int getRunningTime() {
		return (runningTime);
	}
	
	public List<Subscription> getSubscriptions() {
		return (subscriptions);
	}
	
}
