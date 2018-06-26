package ics.uci.edu.firedex.subscriber.message;

import ics.uci.edu.firedex.subscriber.model.Subscription;

public class SubscribeMessage {
	private Subscription subscription;
	
	public SubscribeMessage() { }

	public SubscribeMessage(Subscription subscription) {
		this.subscription = subscription;
	}
	
	public Subscription getSubscription() {
		return (subscription);
	}
	
}
