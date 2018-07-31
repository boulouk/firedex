package edu.uci.ics.model;

import java.util.Date;

import edu.uci.ics.utility.RandomUtility;

public class Event {
	private int value;
	private long timestamp;
	
	public Event(int value, long timestamp) {
		this.value = value;
		this.timestamp = timestamp;
	}

	public int getValue() {
		return (value);
	}

	public long getTimestamp() {
		return (timestamp);
	}
	
	public static Event random() {
		int value = RandomUtility.randomInteger(1, 100);
		long timestamp = ( new Date() ).getTime();
		
		Event randomEvent = new Event(value, timestamp);
		return (randomEvent);
	}
	
}
