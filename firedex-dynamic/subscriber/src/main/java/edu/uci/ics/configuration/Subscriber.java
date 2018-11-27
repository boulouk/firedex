package edu.uci.ics.configuration;

import java.util.List;

public class Subscriber {
	private String identifier;
	private String host;
	
	private int startAfter;
	private int runningTime;
	
	private List<Subscription> subscriptions;
	private List<Subscription> modifications;
	private List<Unsubscription> unsubscriptions;
	
	public Subscriber(
					  String identifier, String host, int startAfter, int runningTime,
					  List<Subscription> subscriptions, List<Subscription> modifications, List<Unsubscription> unsubscriptions
					 )
	{
		this.identifier = identifier;
		this.host = host;
		
		this.startAfter = startAfter;
		this.runningTime = runningTime;
		
		this.subscriptions = subscriptions;
		this.modifications = modifications;
		this.unsubscriptions = unsubscriptions;
	}

	public String getIdentifier() {
		return (identifier);
	}
	
	public String getHost() {
		return (host);
	}
	
	public int getStartAfter() {
		return (startAfter);
	}
	
	public int getRunningTime() {
		return (runningTime);
	}
	
	public List<Subscription> getSubscriptions() {
		return (subscriptions);
	}
	
	public List<Subscription> getModifications() {
		return (modifications);
	}
	
	public List<Unsubscription> getUnsubscriptions() {
		return (unsubscriptions);
	}
	
}
