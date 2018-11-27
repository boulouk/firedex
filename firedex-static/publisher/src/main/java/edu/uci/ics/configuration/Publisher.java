package edu.uci.ics.configuration;

import java.util.List;

public class Publisher {
	private String identifier;
	private String host;
	private int runningTime;
	
	private List<Publication> publications;
	
	public Publisher(String identifier, String host, int runningTime, List<Publication> publishings) {
		this.identifier = identifier;
		this.host = host;
		this.runningTime = runningTime;
		
		this.publications = publishings;
	}

	public String getIdentifier() {
		return (identifier);
	}
	
	public String getHost() {
		return (host);
	}
	
	public int getRunningTime() {
		return (runningTime);
	}
	
	public List<Publication> getPublications() {
		return (publications);
	}

}
