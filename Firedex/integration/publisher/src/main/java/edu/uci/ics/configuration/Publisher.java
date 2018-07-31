package edu.uci.ics.configuration;

import java.util.List;

public class Publisher {
	private String identifier;
	private int runningTime;
	private List<Publishing> publishings;
	
	public Publisher(String identifier, int runningTime, List<Publishing> publishings) {
		this.identifier = identifier;
		this.runningTime = runningTime;
		this.publishings = publishings;
	}

	public String getIdentifier() {
		return (identifier);
	}
	
	public int getRunningTime() {
		return (runningTime);
	}
	
	public List<Publishing> getPublishings() {
		return (publishings);
	}

}
