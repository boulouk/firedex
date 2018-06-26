package ics.uci.edu.firedex.publisher.model;

public class Event {
	private String topic;
	private int value;
	private String status;
	private String time;
	private String device;
	private String source;
	
	public Event() { }
	
	public Event(String topic, int value, String status, String time, String device, String source) {
		this.topic = topic;
		this.value = value;
		this.status = status;
		this.time = time;
		this.device = device;
		this.source = source;
	}

	public String getTopic() {
		return (topic);
	}

	public int getValue() {
		return (value);
	}

	public String getStatus() {
		return (status);
	}

	public String getTime() {
		return (time);
	}

	public String getDevice() {
		return (device);
	}

	public String getSource() {
		return (source);
	}
	
}
