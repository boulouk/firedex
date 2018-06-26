package ics.uci.edu.firedex.subscriber.message;

public class GetPriorityMessage {
	private String message;

	public GetPriorityMessage(String message) {
		this.message = message;
	}
	
	public String getMessage() {
		return (message);
	}
	
}
