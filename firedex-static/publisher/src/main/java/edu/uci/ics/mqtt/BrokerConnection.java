package edu.uci.ics.mqtt;

import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import edu.uci.ics.configuration.Configuration;
import edu.uci.ics.exception.FiredexException;

public class BrokerConnection {
	private Configuration configuration;
	private MqttClient client;

	public BrokerConnection(Configuration configuration) {
		this.configuration = configuration;
		this.client = null;
	}

	public void connect() throws FiredexException {
		try {
			String url = url();
			String identifier = configuration.getPublisher().getIdentifier();

			client = new MqttClient(url, identifier, null);

			MqttConnectOptions connectOptions = new MqttConnectOptions();
			connectOptions.setCleanSession(true);
			connectOptions.setAutomaticReconnect(true);

			client.connect(connectOptions);
		} catch (MqttException exception) {
			throw ( new FiredexException() );
		}

	}

	private String url() {
		String brokerHost = configuration.getBroker().getHost();
		int brokerPort = configuration.getBroker().getPort();
		String url = String.format("tcp://%s:%d", brokerHost, brokerPort);
		return (url);
	}

	public void publish(String topic, byte[] content, int qualityOfService, boolean retained) throws FiredexException {
		try {
			MqttMessage message = new MqttMessage();
			message.setPayload(content);
			message.setQos(qualityOfService);
			message.setRetained(retained);

			client.publish(topic, message);
		} catch (MqttException exception) {
			throw ( new FiredexException() );
		}
	}

	public void disconnect() throws FiredexException {
		try {
			client.disconnect();
		} catch (MqttException exception) {
			throw ( new FiredexException() );
		}
	}

}
