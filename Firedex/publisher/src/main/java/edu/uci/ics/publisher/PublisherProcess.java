package edu.uci.ics.publisher;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ScheduledThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

import edu.uci.ics.configuration.Configuration;
import edu.uci.ics.configuration.Publication;
import edu.uci.ics.exception.FiredexException;
import edu.uci.ics.model.Event;
import edu.uci.ics.model.EventGenerator;
import edu.uci.ics.model.result.PublicationResult;
import edu.uci.ics.model.result.PublisherResult;
import edu.uci.ics.publication.rate.Rate;
import edu.uci.ics.publication.rate.RateFactories;
import edu.uci.ics.publication.rate.RateFactory;
import edu.uci.ics.utility.LoggerUtility;

public class PublisherProcess {
	private Configuration configuration;
	
	private Publisher publisher;
	private List<Publication> publications;
	private Map<String, Integer> publicationsToTopic;
	
	private ScheduledThreadPoolExecutor scheduler;
	
	public PublisherProcess(Configuration configuration, Publisher publisher) {
		this.configuration = configuration;
		
		this.publisher = publisher;
		this.publications = configuration.getPublisher().getPublications();
		this.publicationsToTopic = new HashMap<String, Integer>();
		
		this.scheduler = new ScheduledThreadPoolExecutor(1);
	}
	
	public void startProcess() throws FiredexException {
		for ( Publication publication : publications ) {
			String topic = publication.getTopic();
			publicationsToTopic.put(topic, 0);
			
			String rateType = publication.getRateType();
			double rate = publication.getRate();
			RateFactory rateFactory = RateFactories.create(rateType);
			Rate publicationRate = rateFactory.create(rate);
			
			int messageSize = publication.getMessageSize();
			int qualityOfService = publication.getQualityOfService();
			boolean retained = publication.isRetained();
			
			scheduleEvent(topic, publicationRate, messageSize, qualityOfService, retained);
		}
	}
	
	private void publishEvent(String topic, Rate rate, int messageSize, int qualityOfService, boolean retained) {
		try {
			Event event = EventGenerator.create(messageSize);
			publisher.publish(topic, event, qualityOfService, retained);
			
			int currentPublicationsToTopic = publicationsToTopic.get(topic);
			publicationsToTopic.replace(topic, currentPublicationsToTopic + 1);
			
			scheduleEvent(topic, rate, messageSize, qualityOfService, retained);
		} catch (FiredexException exception) {
			LoggerUtility.log("Something bad happened.");
		}
	}
	
	private void scheduleEvent(String topic, Rate rate, int messageSize, int qualityOfService, boolean retained) {
		int delay = (int) (rate.next() * 1000);
		scheduler.schedule( () -> publishEvent(topic, rate, messageSize, qualityOfService, retained), delay, TimeUnit.MILLISECONDS);
	}
	
	public void stopProcess() throws FiredexException {
		scheduler.shutdown();
	}
	
	public void waitProcess() throws FiredexException {
		try {
			scheduler.awaitTermination(60, TimeUnit.SECONDS);
		} catch (InterruptedException exception) {
			throw ( new FiredexException() );
		}
	}

	public PublisherResult publisherResult() {
		List<PublicationResult> publicationsResult = new ArrayList<>();
		for ( String topic : publicationsToTopic.keySet() ) {
			int messages = publicationsToTopic.get(topic);
			
			PublicationResult publicationResult = new PublicationResult(topic, messages);
			publicationsResult.add(publicationResult);
		}
		
		PublisherResult publisherResult = new PublisherResult(configuration, publicationsResult);
		return (publisherResult);
	}

}
