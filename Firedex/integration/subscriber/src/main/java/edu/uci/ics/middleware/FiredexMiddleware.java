package edu.uci.ics.middleware;

import java.util.ArrayList;
import java.util.List;

import org.json.JSONArray;
import org.json.JSONObject;

import com.mashape.unirest.http.HttpResponse;
import com.mashape.unirest.http.JsonNode;
import com.mashape.unirest.http.Unirest;
import com.mashape.unirest.http.exceptions.UnirestException;

import edu.uci.ics.configuration.Configuration;
import edu.uci.ics.configuration.Subscription;
import edu.uci.ics.exception.FiredexException;
import edu.uci.ics.model.SubscriptionConfiguration;
import edu.uci.ics.model.SubscriptionConfigurationRequest;
import edu.uci.ics.utility.JsonUtility;

public class FiredexMiddleware {
	private Configuration configuration;
	private String baseApi;

	public FiredexMiddleware(Configuration configuration) {
		this.configuration = configuration;
		String middlewareHost = configuration.getMiddleware().getHost();
		int middlewarePort = configuration.getMiddleware().getPort();
		this.baseApi = String.format("http://%s:%d/api/firedex", middlewareHost, middlewarePort);
	}

	public List<SubscriptionConfiguration> subscriberConfiguration(List<Subscription> subscriptions) throws FiredexException {
		try {
			String url = baseApi + "/subscriptions/";
			String identifier = configuration.getSubscriber().getIdentifier();
			SubscriptionConfigurationRequest subscriptionConfigurationRequest = new SubscriptionConfigurationRequest(identifier, subscriptions);
			String body = JsonUtility.toJson(subscriptionConfigurationRequest);
			HttpResponse<JsonNode> response = Unirest
					.post(url)
					.header("Content-Type", "application/json")
					.header("Accept", "application/json")
					.body(body)
					.asJson();
			
			List<SubscriptionConfiguration> subscriptionConfigurations = new ArrayList<>();
			
			JSONArray jsonArray = response.getBody().getArray();
			for ( int i = 0; i < jsonArray.length(); i++ ) {
				JSONObject jsonObject = jsonArray.getJSONObject(i);
				
				String mac = jsonObject.getString("mac");
				String ip = jsonObject.getString("ip");
				String topic = jsonObject.getString("topic");
				int utilityFunction = jsonObject.getInt("utility_function");
				int port = jsonObject.getInt("port");
				int priority = jsonObject.getInt("priority");
				int dropRate = jsonObject.getInt("drop_rate");
				
				SubscriptionConfiguration subscriptionConfiguration = new SubscriptionConfiguration(identifier, ip, mac, topic, utilityFunction, port, priority, dropRate);
				subscriptionConfigurations.add(subscriptionConfiguration);
			}
			
			return (subscriptionConfigurations);
		} catch (UnirestException exception) {
			exception.printStackTrace();
			throw ( new FiredexException() );
		}
	}

}
