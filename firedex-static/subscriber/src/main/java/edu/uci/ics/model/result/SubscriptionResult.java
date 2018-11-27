package edu.uci.ics.model.result;

public class SubscriptionResult {
	private String topic;
	private int port;
	
	private int messages;
	private double latency;
	
	public SubscriptionResult(String topic, int port, int messages, double latency) {
		this.topic = topic;
		this.port = port;
		
		this.messages = messages;
		this.latency = latency;
	}

	public String getTopic() {
		return (topic);
	}

	public int getPort() {
		return (port);
	}

	public int getMessages() {
		return (messages);
	}

	public double getLatency() {
		return (latency);
	}

}
