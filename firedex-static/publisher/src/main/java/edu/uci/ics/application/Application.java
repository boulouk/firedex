package edu.uci.ics.application;

import java.io.PrintWriter;

import edu.uci.ics.configuration.Configuration;
import edu.uci.ics.exception.FiredexException;
import edu.uci.ics.model.EventGenerator;
import edu.uci.ics.model.result.PublisherResult;
import edu.uci.ics.publisher.Publisher;
import edu.uci.ics.publisher.PublisherProcess;
import edu.uci.ics.utility.JsonUtility;
import edu.uci.ics.utility.LoggerUtility;

public class Application {

	public static void main(String[] args) {
		try {
			String configurationFile = args[0];
			Configuration configuration = configuration(configurationFile);
			
			initializeApplication(configuration);
			
			Publisher publisher = new Publisher(configuration);
			publisher.connect();
			
			System.out.println("PUBLISHER: connected.");
			
			PublisherProcess publisherProcess = new PublisherProcess(configuration, publisher);
			
			System.out.println("PUBLISHER: start publications.");
			publisherProcess.startProcess();
			
			int runningTime = configuration.getPublisher().getRunningTime() * 1000;
			Thread.sleep(runningTime);
			
			publisherProcess.stopProcess();
			publisherProcess.waitProcess();
			
			System.out.println("PUBLISHER: end publications.");

			publisher.disconnect();
			
			System.out.println("PUBLISHER: disconnected.");
			
			String outputFile = configuration.getOutput().getOutputFile();
			PrintWriter output = new PrintWriter(outputFile);
			
			PublisherResult publisherResult = publisherProcess.publisherResult();
			String result = JsonUtility.toJson(publisherResult);
			output.println(result);
			
			output.close();
			
			System.out.println("PUBLISHER: completed.");
			
			terminateApplication();

			System.exit(0);
		} catch (Exception exception) {
			System.out.println("Something bad happened.");
		}
	}
	
	private static Configuration configuration(String configurationFile) throws FiredexException {
		Configuration configuration = Configuration.initialize(configurationFile);
		return (configuration);
	}
	
	private static void initializeApplication(Configuration configuration) {
		LoggerUtility.initialize(configuration);
		EventGenerator.initialize(configuration);
	}
	
	private static void terminateApplication() {
		LoggerUtility.terminate();
	}

}
