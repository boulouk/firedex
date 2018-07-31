package edu.uci.ics.configuration;

import java.io.File;
import java.io.IOException;
import java.nio.charset.Charset;
import java.util.List;

import com.google.common.io.Files;

import edu.uci.ics.utility.JsonUtility;

public class Configuration {
	private Broker broker;
	private Publisher publisher;
	
	public Configuration(Broker broker, Publisher publisher) {
		this.broker = broker;
		this.publisher = publisher;
	}

	public static Configuration initialize(String file) throws IOException {
		List<String> lines = Files.readLines( new File(file), Charset.defaultCharset() );
		StringBuilder json = new StringBuilder();
		lines.forEach( (line) -> json.append(line + System.lineSeparator()) );
		Configuration configuration = JsonUtility.fromJson(json.toString(), Configuration.class);
		return (configuration);
	}
	
	public Broker getBroker() {
		return (broker);
	}
	
	public Publisher getPublisher() {
		return (publisher);
	}
	
}
