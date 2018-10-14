package edu.uci.ics.utility;

import java.io.FileNotFoundException;
import java.io.PrintWriter;

import edu.uci.ics.configuration.Configuration;

public class LoggerUtility {
	private static PrintWriter log;
	
	static {
		
	}
	
	private LoggerUtility() {
		
	}
	
	public static void initialize(Configuration configuration) {
		try {
			String logFile = configuration.getOutput().getLogFile();
			log = new PrintWriter(logFile);
		} catch (FileNotFoundException exception) {
			
		}
	}
	
	public static void log(String message) {
		log.println(message);
	}
	
	public static void terminate() {
		log.close();
	}

}
