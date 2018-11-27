package edu.uci.ics.configuration;

public class Unsubscription {
	private String topic;
	private int time;
	
	public Unsubscription(String topic, int time) {
		this.topic = topic;
		this.time = time;
	}
	
	public String getTopic() {
		return (topic);
	}
	
	public int getTime() {
		return (time);
	}

}
