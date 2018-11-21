package edu.uci.ics.middleware;

import com.mashape.unirest.http.Unirest;
import com.mashape.unirest.http.exceptions.UnirestException;

import edu.uci.ics.configuration.Configuration;
import edu.uci.ics.exception.FiredexException;
import edu.uci.ics.model.middleware.PublicationCompletion;
import edu.uci.ics.model.middleware.PublicationIntention;
import edu.uci.ics.utility.JsonUtility;

public class FiredexMiddleware {
	private Configuration configuration;
	private String baseApi;

	public FiredexMiddleware(Configuration configuration) {
		this.configuration = configuration;
		this.baseApi = baseApi();
	}

	private String baseApi() {
		String middlewareHost = configuration.getServer().getMiddleware().getHost();
		int middlewarePort = configuration.getServer().getMiddleware().getPort();
		String baseApi = String.format("http://%s:%d/api/firedex", middlewareHost, middlewarePort);
		return (baseApi);
	}
	
	public void publicationIntention(PublicationIntention publicationIntention) throws FiredexException {
		try {
			String json = JsonUtility.toJson(publicationIntention);
			
			String url = baseApi + "/publication-intention/";
			
			Unirest
				.post(url)
				.header("Content-Type", "application/json")
				.header("Accept", "application/json")
				.body(json)
				.asJson();
			
		} catch (UnirestException exception) {
			throw ( new FiredexException() );
		}
	}
	
	public void publicationCompleted(PublicationCompletion publicationCompletion) throws FiredexException {
		try {
			String json = JsonUtility.toJson(publicationCompletion);
			
			String url = baseApi + "/publication-completion/";
			
			Unirest
				.post(url)
				.header("Content-Type", "application/json")
				.header("Accept", "application/json")
				.body(json)
				.asJson();
			
		} catch (UnirestException exception) {
			throw ( new FiredexException() );
		}
	}

}
