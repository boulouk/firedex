package edu.uci.ics.model.web;

public class WebEvent {
	private String publisher;
	private long identifier;
	private String topic;
	private int port;
	private long sent;
	private long received;
	private long latency;
	
	public WebEvent(String publisher, long identifier, String topic, int port, long sent, long received, long latency) {
		this.publisher = publisher;
		this.identifier = identifier;
		this.topic = topic;
		this.port = port;
		this.sent = sent;
		this.received = received;
		this.latency = latency;
	}

	public String getPublisher() {
		return (publisher);
	}

	public long getIdentifier() {
		return (identifier);
	}

	public String getTopic() {
		return (topic);
	}

	public int getPort() {
		return (port);
	}

	public long getSent() {
		return (sent);
	}

	public long getReceived() {
		return (received);
	}

	public long getLatency() {
		return (latency);
	}

}
