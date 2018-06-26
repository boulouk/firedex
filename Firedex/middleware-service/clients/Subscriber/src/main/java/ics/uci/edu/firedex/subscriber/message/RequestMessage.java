package ics.uci.edu.firedex.subscriber.message;

import ics.uci.edu.firedex.subscriber.model.Request;

public class RequestMessage {
	private Request request;
	
	public RequestMessage(Request request) {
		this.request = request;
	}
	
	public Request getRequest() {
		return (request);
	}

}
