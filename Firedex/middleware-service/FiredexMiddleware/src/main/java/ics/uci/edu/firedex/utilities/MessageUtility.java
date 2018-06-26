package ics.uci.edu.firedex.utilities;

public class MessageUtility {
	
	static { }
	
	private MessageUtility() { }
	
	public static String toString(byte[] message) {
		return ( new String(message) );
	}
	
	public static byte[] toBytes(String message) {
		return ( message.getBytes() );
	}

}
