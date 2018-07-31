package edu.uci.ics.mqtt;

import java.util.ArrayList;
import java.util.List;

import org.eclipse.paho.mqttsn.udpclient.SimpleMqttsCallback;
import org.eclipse.paho.mqttsn.udpclient.SimpleMqttsClient;

import edu.uci.ics.configuration.Configuration;
import edu.uci.ics.exception.FiredexException;
import edu.uci.ics.model.SubscriptionConfiguration;
import edu.uci.ics.utility.MessageUtility;

public class UDPBrokerConnection implements BrokerConnection {
	private Configuration configuration;
	private int localPort;
	
	private SimpleMqttsClient client;
	
	private List<SubscriptionConfiguration> subscriptions;
	private List<OnEvent> onEventListeners;
	
	public UDPBrokerConnection(Configuration configuration, int localPort) {
		this.configuration = configuration;
		this.localPort = localPort;
		
		this.client = null;
		
		this.subscriptions = new ArrayList<>();
		this.onEventListeners = new ArrayList<>();
	}

	@Override
	public int getLocalPort() {
		return (localPort);
	}

	@Override
	public void connect() throws FiredexException {
		synchronized ( this ) {
			try {
				String gatewayHost = configuration.getBrokerGateway().getHost();
				int gatewayPort = configuration.getBrokerGateway().getPort();
				
				String baseIdentifier = configuration.getSubscriber().getIdentifier();
				String identifier = String.format("%s.%d", baseIdentifier, localPort);
				
				this.client = new SimpleMqttsClient(gatewayHost, gatewayPort, 1024, 2, 2, 5, true, localPort);
						
				client.setCallback( new SimpleMqttsCallback() {
					
					@Override
					public void publishArrived(boolean retained, int qualityOfService, String topic, byte[] payload) {
						String message = MessageUtility.toString(payload);
						onEvent(topic, message);
					}
					
					@Override
					public void disconnected(int code) { }
				});
				
				client.connect(identifier);
			} catch (Exception exception) {
				throw ( new FiredexException() );
			}
		}
	}

	@Override
	public void subscribe(SubscriptionConfiguration subscriptionConfiguration) throws FiredexException {
		synchronized (this) {
			try {
				client.subscribe(subscriptionConfiguration.getTopic());
				subscriptions.add(subscriptionConfiguration);
			} catch (Exception exception) {
				throw ( new FiredexException() );
			}
		}
	}

	@Override
	public void disconnect() throws FiredexException {
		synchronized (this) {
			try {
				client.disconnect();
			} catch (Exception exception) {
				throw ( new FiredexException() );
			}
		}
	}

	@Override
	public void addOnEventListener(OnEvent onEventListener) {
		onEventListeners.add(onEventListener);
	}
	
	@Override
	public void removeOnEventListener(OnEvent onEventListener) {
		onEventListeners.remove(onEventListener);
	}
	
	private void onEvent(String topic, String event) {
		for ( OnEvent onEventListener : onEventListeners )
			onEventListener.onEvent( byTopic(topic), event );
	}

	private SubscriptionConfiguration byTopic(String topic) {
		for ( SubscriptionConfiguration subscription : subscriptions )
			if ( subscription.getTopic().equals(topic) )
				return (subscription);
		
		return (null);
	}
	
}
