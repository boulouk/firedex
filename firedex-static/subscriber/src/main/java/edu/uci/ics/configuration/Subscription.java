package edu.uci.ics.configuration;

public class Subscription {
	private String topic;
	private double utilityFunction;
	private int time;
	
	public Subscription(String topic, double utilityFunction, int time) {
		this.topic = topic;
		this.utilityFunction = utilityFunction;
		this.time = time;
	}
	
	public String getTopic() {
		return (topic);
	}
	
	public double getUtilityFunction() {
		return (utilityFunction);
	}
	
	public int getTime() {
		return (time);
	}

}
