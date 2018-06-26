package ics.uci.edu.firedex.subscriber.model;

public class Event implements Comparable<Event> {
	private String topic;
	private int priority;
	private int value;
	private String status;
	private String time;
	private String device;
	private String source;
	
	public Event() { }
	
	public Event(String topic, int priority, int value, String status, String time, String device, String source) {
		this.topic = topic;
		this.priority = priority;
		this.value = value;
		this.status = status;
		this.time = time;
		this.device = device;
		this.source = source;
	}
	
	public String getTopic() {
		return (topic);
	}

	public void setTopic(String topic) {
		this.topic = topic;
	}

	public int getPriority() {
		return (priority);
	}

	public void setPriority(int priority) {
		this.priority = priority;
	}

	public int getValue() {
		return (value);
	}

	public void setValue(int value) {
		this.value = value;
	}

	public String getStatus() {
		return (status);
	}

	public void setStatus(String status) {
		this.status = status;
	}

	public String getTime() {
		return (time);
	}

	public void setTime(String time) {
		this.time = time;
	}

	public String getDevice() {
		return (device);
	}

	public void setDevice(String device) {
		this.device = device;
	}

	public String getSource() {
		return (source);
	}

	public void setSource(String source) {
		this.source = source;
	}

	@Override
	public int compareTo(Event that) {
		return (  Integer.compare( this.getPriority(), that.getPriority() )  );
	}
	
}
