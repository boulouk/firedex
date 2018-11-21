package edu.uci.ics.model.middleware;

public class SubscriptionIntention {
	private String topic;
	private double utilityFunction;
	
	public SubscriptionIntention(String topic, double utilityFunction) {
		this.topic = topic;
		this.utilityFunction = utilityFunction;
	}
	
	public String getTopic() {
		return (topic);
	}
	
	public double getUtilityFunction() {
		return (utilityFunction);
	}

}
