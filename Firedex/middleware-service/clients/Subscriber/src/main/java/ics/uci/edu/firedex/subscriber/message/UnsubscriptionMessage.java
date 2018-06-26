package ics.uci.edu.firedex.subscriber.message;

public class UnsubscriptionMessage {
	private String message;
	
	public UnsubscriptionMessage(String message) {
		this.message = message;
	}
	
	public String getMessage() {
		return (message);
	}
	
}
