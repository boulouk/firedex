package edu.uci.ics.mqtt;

import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import edu.uci.ics.configuration.Configuration;
import edu.uci.ics.exception.FiredexException;
import edu.uci.ics.utility.MessageUtility;

public class BrokerConnection {
	private Configuration configuration;
	private MqttClient client;
	
	public BrokerConnection(Configuration configuration) {
		this.configuration = configuration;
		this.client = null;
	}
	
	public void connect() throws FiredexException {
		synchronized (this) {
			try {
				String brokerHost = configuration.getBroker().getHost();
				int brokerPort = configuration.getBroker().getPort();
				String url = String.format( "tcp://%s:%d", brokerHost, brokerPort );
				
				String identifier = configuration.getPublisher().getIdentifier();
				
				client = new MqttClient(url, identifier, null);
				
				MqttConnectOptions connectOptions = new MqttConnectOptions();
				connectOptions.setCleanSession(true);
				connectOptions.setAutomaticReconnect(true);
				
				client.connect(connectOptions);
			} catch (MqttException exception) {
				exception.printStackTrace();
				throw ( new FiredexException() );
			}
		}
	}
	
	public void publish(String topic, String content, int qualityOfService, boolean retained) throws FiredexException {
		synchronized (this) {
			try {
				MqttMessage message = new MqttMessage();
				message.setPayload( MessageUtility.toBytes(content) );
				message.setQos(qualityOfService);
				message.setRetained(retained);
				
				client.publish(topic, message);
			} catch (MqttException exception) {
				throw ( new FiredexException() );
			}
		}
	}
	
	public void disconnect() throws FiredexException {
		synchronized (this) {
			try {
				client.disconnect();
			} catch (MqttException exception) {
				throw ( new FiredexException() );
			}
		}
	}

}
