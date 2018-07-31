package edu.uci.ics.configuration;

public class Subscription {
	private String topic;
	private int utilityFunction;
	
	public Subscription(String topic, int utilityFunction) {
		this.topic = topic;
		this.utilityFunction = utilityFunction;
	}
	
	public String getTopic() {
		return (topic);
	}
	
	public int getUtilityFunction() {
		return (utilityFunction);
	}

}
