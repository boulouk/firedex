package edu.uci.ics.configuration;

import java.util.List;

public class Publisher {
	private String identifier;
	private String host;
	
	private int startAfter;
	private int runningTime;
	
	private List<Publication> publications;
	
	public Publisher(String identifier, String host, int startAfter, int runningTime, List<Publication> publishings) {
		this.identifier = identifier;
		this.host = host;
		
		this.startAfter = startAfter;
		this.runningTime = runningTime;
		
		this.publications = publishings;
	}

	public String getIdentifier() {
		return (identifier);
	}
	
	public String getHost() {
		return (host);
	}
	
	public int getStartAfter() {
		return (startAfter);
	}
	
	public int getRunningTime() {
		return (runningTime);
	}
	
	public List<Publication> getPublications() {
		return (publications);
	}

}
