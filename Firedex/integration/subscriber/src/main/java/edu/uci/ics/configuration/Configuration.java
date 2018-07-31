package edu.uci.ics.configuration;

import java.io.File;
import java.io.IOException;
import java.nio.charset.Charset;
import java.util.List;

import com.google.common.io.Files;

import edu.uci.ics.utility.JsonUtility;

public class Configuration {
	private Middleware middleware;
	private Broker broker;
	private BrokerGateway brokerGateway;
	private Subscriber subscriber;
	
	public Configuration(Middleware middleware, Broker broker, BrokerGateway brokerGateway, Subscriber subscriber) {
		this.middleware = middleware;
		this.broker = broker;
		this.brokerGateway = brokerGateway;
		this.subscriber = subscriber;
	}

	public static Configuration initialize(String file) throws IOException {
		List<String> lines = Files.readLines( new File(file), Charset.defaultCharset() );
		StringBuilder json = new StringBuilder();
		lines.forEach( (line) -> json.append(line + "\n") );
		Configuration configuration = JsonUtility.fromJson(json.toString(), Configuration.class);
		return (configuration);
	}
	
	public Middleware getMiddleware() {
		return (middleware);
	}
	
	public Broker getBroker() {
		return (broker);
	}
	
	public BrokerGateway getBrokerGateway() {
		return (brokerGateway);
	}
	
	public Subscriber getSubscriber() {
		return (subscriber);
	}
	
}
