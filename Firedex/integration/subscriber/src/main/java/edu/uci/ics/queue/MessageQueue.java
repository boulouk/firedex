package edu.uci.ics.queue;

import java.util.concurrent.PriorityBlockingQueue;

import edu.uci.ics.exception.FiredexException;
import edu.uci.ics.model.Message;

public class MessageQueue {
	private PriorityBlockingQueue<Message> messages;
	
	public MessageQueue() {
		messages = new PriorityBlockingQueue<>();
	}
	
	public void blockingPut(Message message) {
		messages.put(message);
	}
	
	public Message blockingTake() throws FiredexException {
		try {
			Message message = messages.take();
			return (message);
		} catch (InterruptedException exception) {
			throw ( new FiredexException() );
		}
	}

}
