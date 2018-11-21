package edu.uci.ics.mqtt;

import org.eclipse.paho.mqttsn.udpclient.SimpleMqttsCallback;

public class MqttsCallback implements SimpleMqttsCallback {
	private OnMessage onMessage;
	
	public MqttsCallback(OnMessage onMessage) {
		this.onMessage = onMessage;
	}
	
	@Override
	public void disconnected(int code) {
		
	}

	@Override
	public void publishArrived(boolean retained, int qualityOfService, String topic, byte[] payload) {
		onMessage.onMessage(topic, payload);
	}

}
