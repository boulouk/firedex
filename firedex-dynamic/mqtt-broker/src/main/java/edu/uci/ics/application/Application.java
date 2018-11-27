package edu.uci.ics.application;

import java.io.File;

import edu.uci.ics.broker.Broker;

public class Application {
	
	public static void main(String[] args) throws Exception {
		String file = args[0];
		File configurationFile = new File(file);
		Broker broker = new Broker();
		broker.start(configurationFile);
	}
	
}
