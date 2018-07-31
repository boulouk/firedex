package edu.uci.ics.mqtt;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import edu.uci.ics.utility.MessageUtility;

public class MessageHandler implements MqttCallback {
	private OnMessage onMessage;

	public MessageHandler(OnMessage onMessage) {
		this.onMessage = onMessage;
	}
	
	public void connectionLost(Throwable cause) { }

	public void deliveryComplete(IMqttDeliveryToken deliveryToken) { }

	public void messageArrived(String topic, MqttMessage message) {
		onMessage.onMessage(  topic, MessageUtility.toString( message.getPayload() )  );
	}

}
