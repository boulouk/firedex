package edu.uci.ics.mqtt;

public interface OnMessage {
	
	public void onMessage(String topic, byte[] content);

}
