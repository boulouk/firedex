package edu.uci.ics.model.result;

public class PublicationResult {
	private String topic;
	private int messages;
	
	public PublicationResult(String topic, int messages) {
		this.topic = topic;
		this.messages = messages;
	}
	
	public String getTopic() {
		return (topic);
	}
	
	public int getMessages() {
		return (messages);
	}

}
