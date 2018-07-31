package edu.uci.ics.model;

public class Message implements Comparable<Message> {
	private Event event;
	private int priority;
	
	public Message(Event event, int priority) {
		this.event = event;
		this.priority = priority;
	}
	
	public Event getEvent() {
		return (event);
	}
	
	public int getPriority() {
		return (priority);
	}

	@Override
	public int compareTo(Message that) {
		return (  Integer.compare( this.getPriority(), that.getPriority() )  ); 
	}

}
