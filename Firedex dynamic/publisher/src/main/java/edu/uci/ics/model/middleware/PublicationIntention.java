package edu.uci.ics.model.middleware;

import java.util.List;

import edu.uci.ics.configuration.Publication;

public class PublicationIntention {
	private String identifier;
	private List<Publication> publications;
	
	public PublicationIntention(String identifier, List<Publication> publications) {
		this.identifier = identifier;
		this.publications = publications;
	}
	
	public String getIdentifier() {
		return (identifier);
	}
	
	public List<Publication> getPublications() {
		return (publications);
	}

}
