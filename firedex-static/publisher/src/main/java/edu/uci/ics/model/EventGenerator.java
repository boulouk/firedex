package edu.uci.ics.model;

import java.util.Date;

import edu.uci.ics.configuration.Configuration;

public class EventGenerator {
	private static String PUBLISHER;
	private static int IDENTIFIER;
	
	static {
		PUBLISHER = "";
		IDENTIFIER = 0;
	}
	
	public static void initialize(Configuration configuration) {
		PUBLISHER = configuration.getPublisher().getIdentifier();
	}
	
	public static Event create(int size) {
		String publisher = PUBLISHER;
		int identifier = IDENTIFIER;
		long timestamp = ( new Date() ).getTime();
		int padding = size - 30;
		
		Event event = new Event(publisher, identifier, timestamp, padding);
		
		IDENTIFIER = IDENTIFIER + 1;
		
		return (event);
	}

}
