package ics.uci.edu.firedex.subscriber.message;

public class DisconnectMessage {
	private String message;

	public DisconnectMessage(String message) {
		this.message = message;
	}
	
	public String getMessage() {
		return (message);
	}
	
}
