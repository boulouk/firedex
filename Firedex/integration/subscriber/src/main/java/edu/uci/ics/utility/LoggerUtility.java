package edu.uci.ics.utility;

public class LoggerUtility {
	
	static {
		
	}
	
	private LoggerUtility() {
		
	}
	
	synchronized public static void log(String message) {
		System.out.println(message);
	}

}
