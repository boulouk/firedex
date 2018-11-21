package edu.uci.ics.mqtt;

import java.util.ArrayList;
import java.util.List;

import org.eclipse.paho.mqttsn.udpclient.SimpleMqttsClient;

import edu.uci.ics.configuration.Configuration;
import edu.uci.ics.exception.FiredexException;
import edu.uci.ics.model.Event;

public class BrokerConnection {
	private Configuration configuration;
	
	private SimpleMqttsClient client;
	private int port;
	
	private List<String> subscriptions;
	private List<OnEvent> onEventListeners;
	
	public BrokerConnection(Configuration configuration, int port) {
		this.configuration = configuration;
		
		this.client = null;
		this.port = port;
		
		this.subscriptions = new ArrayList<>();
		this.onEventListeners = new ArrayList<>();
	}
	
	public int getPort() {
		return (port);
	}
	
	public List<String> getSubscriptions() {
		return (subscriptions);
	}
	
	public void connect() throws FiredexException {
		try {
			String host = configuration.getServer().getBroker().getHost();
			int port = configuration.getServer().getBroker().getPort();
			int maxMessageLength = 1024; int minMessageLength = 2;
			int maxRetries = 0; int ackWaitingTime = 5; boolean autoReconnect = true;
			int localPort = getPort();
			
			client = new SimpleMqttsClient(host, port,
										   maxMessageLength, minMessageLength,
										   maxRetries, ackWaitingTime, autoReconnect, localPort
										  );
			
			client.setCallback(  new MqttsCallback( (topic, content) -> onEvent(topic, content) )  );
			
			String baseIdentifier = configuration.getSubscriber().getIdentifier();
			String identifier = String.format("%s.%d", baseIdentifier, localPort);
			boolean cleanStart = true; int keepAlive = 86400;
			
			client.connect(identifier, cleanStart, keepAlive);
		} catch (Exception exception) {
			throw ( new FiredexException() );
		}
	}
	
	public void subscribe(String topic) throws FiredexException {
		try {
			client.subscribe(topic);
			subscriptions.add(topic);
		} catch (Exception exception) {
			throw ( new FiredexException() );
		}
	}
	
	public void unsubscribe(String topic) throws FiredexException {
		try {
			client.unsubscribe(topic);
			subscriptions.remove(topic);
		} catch (Exception exception) {
			throw ( new FiredexException() );
		}
	}
	
	public void disconnect() throws FiredexException {
		try {
			client.disconnect();
		} catch (Exception exception) {
			throw ( new FiredexException() );
		}
	}
	
	public void addOnEventListener(OnEvent onEventListener) {
		onEventListeners.add(onEventListener);
	}
	
	public void removeOnEventListener(OnEvent onEventListener) {
		onEventListeners.remove(onEventListener);
	}
	
	private void onEvent(String topic, byte[] content) {
		Event event = Event.deserialize(content);
		for ( OnEvent onEventListener : onEventListeners )
			onEventListener.onEvent(topic, port, event);
	}
	
}
