package edu.uci.ics.model.result;

import java.util.List;

import edu.uci.ics.configuration.Configuration;

public class PublisherResult {
	private Configuration configuration;
	private List<PublicationResult> publicationsResult;
	
	public PublisherResult(Configuration configuration, List<PublicationResult> publicationsResult) {
		this.configuration = configuration;
		this.publicationsResult = publicationsResult;
	}
	
	public Configuration getConfiguration() {
		return (configuration);
	}
	
	public List<PublicationResult> getPublicationsResult() {
		return (publicationsResult);
	}
	
}
