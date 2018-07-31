package edu.uci.ics.utility;

public class MessageUtility {
	
	static {
		
	}
	
	private MessageUtility() {
		
	}
	
	synchronized public static String toString(byte[] message) {
		return ( new String(message) );
	}
	
	synchronized public static byte[] toBytes(String message) {
		return ( message.getBytes() );
	}

}
