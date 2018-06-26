package ics.uci.edu.firedex.subscriber.message;

import ics.uci.edu.firedex.subscriber.model.Unsubscription;

public class UnsubscribeMessage {
	private Unsubscription unsubscription;
	
	public UnsubscribeMessage() { }
	
	public UnsubscribeMessage(Unsubscription unsubscription) {
		this.unsubscription = unsubscription;
	}

	public Unsubscription getUnsubscription() {
		return (unsubscription);
	}
	
}
