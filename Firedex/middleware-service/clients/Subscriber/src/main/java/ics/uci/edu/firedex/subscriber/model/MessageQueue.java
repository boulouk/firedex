package ics.uci.edu.firedex.subscriber.model;

import java.util.concurrent.PriorityBlockingQueue;

public class MessageQueue {
	private PriorityBlockingQueue<Event> events;
	
	public MessageQueue() {
		events = new PriorityBlockingQueue<>();
	}
	
	public void blockingPut(Event event) {
		events.put(event);
	}
	
	public Event blockingTake() throws InterruptedException {
		Event event = events.take();
		return (event);
	}
	
	public void clear() {
		events.clear();
	}

}
