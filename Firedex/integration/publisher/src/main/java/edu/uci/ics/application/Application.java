package edu.uci.ics.application;

import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.List;

import edu.uci.ics.configuration.Configuration;
import edu.uci.ics.configuration.Publishing;
import edu.uci.ics.publisher.PublishProcess;
import edu.uci.ics.publisher.Publisher;

public class Application {
	
	public static void main(String[] args) throws Exception {
		String configurationFile = args[0];
		String outputFile = args[1];
		
		Configuration configuration = Configuration.initialize(configurationFile);
		
		Publisher publisher = new Publisher(configuration);
		publisher.connect();
		
		List<Publishing> publishings = configuration.getPublisher().getPublishings();
		List<PublishProcess> publishProcesses = new ArrayList<>();
		for ( Publishing publishing : publishings ) {
			PublishProcess publishProcess = new PublishProcess(publisher, publishing);
			publishProcesses.add(publishProcess);
		}
		
		for ( PublishProcess publishProcess : publishProcesses )
			publishProcess.startProcess();
		
		int runningTime = configuration.getPublisher().getRunningTime() * 1000;
		Thread.sleep(runningTime);
		
		for ( PublishProcess publishProcess : publishProcesses )
			publishProcess.stopProcess();
		
		for ( PublishProcess publishProcess : publishProcesses )
			publishProcess.waitProcess();
		
		publisher.disconnect();
		
		PrintWriter output = new PrintWriter(outputFile);
		
		output.println("[");
		for ( int i = 0; i < publishProcesses.size(); i++ ) {
			PublishProcess publishProcess = publishProcesses.get(i);
			String topic = publishProcess.getPublishing().getTopic();
			int messages = publishProcess.getMessages();
			if ( i != (publishProcesses.size() - 1) )
				output.println( String.format("   { \"topic\": \"%s\", \"messages\": \"%d\" }, " , topic, messages) );
			else
				output.println( String.format("   { \"topic\": \"%s\", \"messages\": \"%d\" }" , topic, messages) );
		}
		output.println("]");
		
		output.close();
		
		System.exit(0);
	}
	
}
