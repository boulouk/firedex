package edu.uci.ics.publisher;

import edu.uci.ics.configuration.Publishing;
import edu.uci.ics.distribution.PoissonDistribution;
import edu.uci.ics.exception.FiredexException;
import edu.uci.ics.model.Event;
import edu.uci.ics.utility.LoggerUtility;

public class PublishProcess {
	private Publisher publisher;
	private Publishing publishing;
	private int messages;
	
	private Thread processThread;
	private boolean continueCondition;
	
	public PublishProcess(Publisher publisher, Publishing publishing) {
		this.publisher = publisher;
		this.publishing = publishing;
		this.messages = 0;
		
		this.processThread = new Thread( () -> run() );
	}
	
	public Publisher getPublisher() {
		return (publisher);
	}
	
	public Publishing getPublishing() {
		return (publishing);
	}
	
	public int getMessages() {
		return (messages);
	}
	
	public void startProcess() {
		continueCondition = true;
		processThread.start();
	}
	
	private void run() {
		String topic = publishing.getTopic();
		int qualityOfService = publishing.getQualityOfService();
		boolean retained = publishing.isRetained();
		int period = publishing.getParameter();
		
		PoissonDistribution poissonDistribution = new PoissonDistribution(period);
		
		try {
			while (continueCondition) {
				Event event = Event.random();
				publisher.publish(topic, event, qualityOfService, retained);
				messages = messages + 1;
				long waitTime = (long) ( poissonDistribution.next() * 1000 );
				Thread.sleep(waitTime);
			}
			
			StringBuilder log = new StringBuilder();
			log.append("---");
			log.append( System.lineSeparator() );
			log.append( String.format("topic: %s", topic) );
			log.append( System.lineSeparator() );
			log.append( String.format("messages: %d", messages) );
			log.append( System.lineSeparator() );
			log.append("---");
			log.append( System.lineSeparator() );
			
			LoggerUtility.log( log.toString() );
		} catch (Exception exception) {
			
		}
	}
	
	public void stopProcess() {
		continueCondition = false;
	}
	
	public void waitProcess() throws FiredexException {
		try {
			processThread.join();
		} catch (InterruptedException exception) {
			throw ( new FiredexException() );
		}
	}

}
