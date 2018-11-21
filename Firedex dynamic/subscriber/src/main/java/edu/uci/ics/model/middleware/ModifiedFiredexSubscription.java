package edu.uci.ics.model.middleware;

public class ModifiedFiredexSubscription {
	private String topic;
	private int oldPort;
	private int newPort;
	
	public ModifiedFiredexSubscription(String topic, int oldPort, int newPort) {
		this.topic = topic;
		this.oldPort = oldPort;
		this.newPort = newPort;
	}
	
	public String getTopic() {
		return (topic);
	}
	
	public int getOldPort() {
		return (oldPort);
	}
	
	public int getNewPort() {
		return (newPort);
	}
	
}
