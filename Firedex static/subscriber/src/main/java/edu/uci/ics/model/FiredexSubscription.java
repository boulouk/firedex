package edu.uci.ics.model;

public class FiredexSubscription {
	private String topic;
	private int port;
	
	public FiredexSubscription(String topic, int port) {
		this.topic = topic;
		this.port = port;
	}
	
	public String getTopic() {
		return (topic);
	}
	
	public int getPort() {
		return (port);
	}
	
}
