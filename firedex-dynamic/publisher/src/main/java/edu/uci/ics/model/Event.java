package edu.uci.ics.model;

import java.util.Arrays;

import com.google.common.primitives.Longs;

public class Event {
	private String publisher;
	private long identifier;
	private long timestamp;
	private int padding;
	
	public Event(String publisher, long identifier, long timestamp, int padding) {
		this.publisher = publisher;
		this.identifier = identifier;
		this.timestamp = timestamp;
		this.padding = padding;
	}
	
	public String getPublisher() {
		return (publisher);
	}
	
	public long getIdentifier() {
		return (identifier);
	}

	public long getTimestamp() {
		return (timestamp);
	}
	
	public int getPadding() {
		return (padding);
	}
	
	public static byte[] serialize(Event event) {
		String publisher = event.getPublisher();
		long identifier = event.getIdentifier();
		long timestamp = event.getTimestamp();
		int padding = event.getPadding();
		
		int size = 14 + 8 + 8 + padding;
		byte[] result = new byte[size];
		
		byte[] publisherBytes = publisher.getBytes();
		put(result, publisherBytes, 0);
		
		byte[] identifierBytes = Longs.toByteArray(identifier);
		put(result, identifierBytes, 14);
		
		byte[] timestampBytes = Longs.toByteArray(timestamp);
		put(result, timestampBytes, 22);
		
		return (result);
	}
	
	private static void put(byte[] result, byte[] array, int startIndex) {
		for ( int i = 0; i < array.length; i++ )
			result[ startIndex + i ] = array[i];
	}
	
	public static Event deserialize(byte[] bytes) {
		byte[] publisherBytes = get(bytes, 0, 13);
		String publisher = new String(publisherBytes);
		byte[] identifierBytes = get(bytes, 14, 21);
		long identifier = Longs.fromByteArray(identifierBytes);
		byte[] timestampBytes = get(bytes, 22, 29);
		long timestamp = Longs.fromByteArray(timestampBytes);
		int padding = bytes.length - 30;
		
		Event event = new Event(publisher, identifier, timestamp, padding);
		return (event);
	}
	
	private static byte[] get(byte[] result, int startIndex, int endIndex) {
		byte[] bytes = Arrays.copyOfRange(result, startIndex, endIndex + 1);
		return (bytes);
	}
	
}
