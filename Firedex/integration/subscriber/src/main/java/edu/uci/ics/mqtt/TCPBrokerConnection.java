package edu.uci.ics.mqtt;

import java.util.ArrayList;
import java.util.List;

import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;

import edu.uci.ics.configuration.Configuration;
import edu.uci.ics.exception.FiredexException;
import edu.uci.ics.model.SubscriptionConfiguration;

public class TCPBrokerConnection implements BrokerConnection {
	private Configuration configuration;
	private int localPort;
	
	private MqttClient client;
	
	private List<SubscriptionConfiguration> subscriptions;
	private List<OnEvent> onEventListeners;
	
	public TCPBrokerConnection(Configuration configuration, int localPort) {
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
				String brokerHost = configuration.getBroker().getHost();
				int brokerPort = configuration.getBroker().getPort();
				String url = String.format( "tcp://%s:%d" , brokerHost, brokerPort );
				
				String baseIdentifier = configuration.getSubscriber().getIdentifier();
				String identifier = String.format( "%s.%d", baseIdentifier, localPort );
				
				this.client = new MqttClient(url, identifier, null);
				
				client.setCallback(
					new MessageHandler( (topic, message) -> onEvent(topic, message) )
				);
				
				MqttConnectOptions connectOptions = new MqttConnectOptions();
				connectOptions.setCleanSession(false);
				connectOptions.setAutomaticReconnect(true);
				connectOptions.setSocketFactory( new CustomSocketFactory(localPort) );
				
				client.connect(connectOptions);
				
				System.err.println( client.isConnected() );
			} catch (MqttException exception) {
				exception.printStackTrace();
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
			} catch (MqttException exception) {
				exception.printStackTrace();
				throw ( new FiredexException() );
			}
		}
	}
	
	@Override
	public void disconnect() throws FiredexException {
		synchronized (this) {
			try {
				client.disconnect();
			} catch (MqttException exception) {
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
