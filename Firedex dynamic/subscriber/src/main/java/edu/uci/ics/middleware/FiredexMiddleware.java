package edu.uci.ics.middleware;

import com.mashape.unirest.http.HttpResponse;
import com.mashape.unirest.http.JsonNode;
import com.mashape.unirest.http.Unirest;
import com.mashape.unirest.http.exceptions.UnirestException;

import edu.uci.ics.configuration.Configuration;
import edu.uci.ics.exception.FiredexException;
import edu.uci.ics.model.middleware.SubscriptionCompletion;
import edu.uci.ics.model.middleware.SubscriptionIntentionInsert;
import edu.uci.ics.model.middleware.SubscriptionIntentionModify;
import edu.uci.ics.model.middleware.SubscriptionIntentionRemove;
import edu.uci.ics.model.middleware.SubscriptionIntentionResponse;
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
	
	public SubscriptionIntentionResponse subscriptionIntentionInsert(SubscriptionIntentionInsert subscriptionIntentionInsert) throws FiredexException {
		String json = JsonUtility.toJson(subscriptionIntentionInsert);
		String url = baseApi + "/subscription-intention/insert/";
		
		return ( subscriptionIntentionRequest(json, url) );
	}
	
	public SubscriptionIntentionResponse subscriptionIntentionModify(SubscriptionIntentionModify subscriptionIntentionModify) throws FiredexException {
		String json = JsonUtility.toJson(subscriptionIntentionModify);
		String url = baseApi + "/subscription-intention/modify/";
		
		return ( subscriptionIntentionRequest(json, url) );
	}

	public SubscriptionIntentionResponse subscriptionIntentionRemove(SubscriptionIntentionRemove subscriptionIntentionRemove) throws FiredexException {
		String json = JsonUtility.toJson(subscriptionIntentionRemove);
		String url = baseApi + "/subscription-intention/remove/";
			
		return ( subscriptionIntentionRequest(json, url) );
	}
	
	private SubscriptionIntentionResponse subscriptionIntentionRequest(String json, String url) throws FiredexException {
		try {
			HttpResponse<JsonNode> response = Unirest
					.post(url)
					.header("Content-Type", "application/json")
					.header("Accept", "application/json")
					.body(json)
					.asJson();
			
			json = response.getBody().toString();	
			SubscriptionIntentionResponse subscriptionIntentionResponse = JsonUtility.fromJson(json, SubscriptionIntentionResponse.class);
			return (subscriptionIntentionResponse);
		} catch (UnirestException exception) {
			throw ( new FiredexException() );
		}
	}
	
	public void subscriptionCompletion(SubscriptionCompletion subscriptionCompletion) throws FiredexException {
		try {
			String json = JsonUtility.toJson(subscriptionCompletion);
			
			String url = baseApi + "/subscription-completion/";
			
			Unirest
				.post(url)
				.header("Content-Type", "application/json")
				.header("Accept", "application/json")
				.body(json)
				.asJson();
			
			System.out.println("subscription completion");
		} catch (UnirestException exception) {
			throw ( new FiredexException() );
		}
	}

}
