package ics.uci.edu.firedex.subscriber.message;

import ics.uci.edu.firedex.subscriber.model.Event;

public class EventMessage {
	private Event event;
	
	public EventMessage(Event event) {
		this.event = event;
	}
	
	public Event getEvent() {
		return (event);
	}
	
}
