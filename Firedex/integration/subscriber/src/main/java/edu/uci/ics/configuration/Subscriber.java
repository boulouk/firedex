package edu.uci.ics.configuration;

import java.util.List;

public class Subscriber {
	private String identifier;
	private int runningTime;
	private String type;
	private List<Subscription> subscriptions;
	
	public Subscriber(String identifier, int runningTime, String type, List<Subscription> subscriptions) {
		this.identifier = identifier;
		this.runningTime = runningTime;
		this.type = type;
		this.subscriptions = subscriptions;
	}
	
	public String getIdentifier() {
		return (identifier);
	}
	
	public int getRunningTime() {
		return (runningTime);
	}
	
	public String getType() {
		return (type);
	}
	
	public List<Subscription> getSubscriptions() {
		return (subscriptions);
	}

}
