package edu.uci.ics.model.middleware;

public class UnsubscriptionIntention {
	private String topic;
	
	public UnsubscriptionIntention(String topic) {
		this.topic = topic;
	}
	
	public String getTopic() {
		return (topic);
	}

}
