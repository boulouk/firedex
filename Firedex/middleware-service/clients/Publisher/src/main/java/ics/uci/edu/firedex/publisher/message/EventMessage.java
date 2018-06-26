package ics.uci.edu.firedex.publisher.message;

import ics.uci.edu.firedex.publisher.model.Event;

public class EventMessage {
	private Event event;
	
	public EventMessage(Event event) {
		this.event = event;
	}
	
	public Event getEvent() {
		return (event);
	}
	
}
