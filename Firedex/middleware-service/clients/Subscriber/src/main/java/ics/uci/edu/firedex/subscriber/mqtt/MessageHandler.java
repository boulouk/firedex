package ics.uci.edu.firedex.subscriber.mqtt;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import ics.uci.edu.firedex.subscriber.utilities.MessageUtility;

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
