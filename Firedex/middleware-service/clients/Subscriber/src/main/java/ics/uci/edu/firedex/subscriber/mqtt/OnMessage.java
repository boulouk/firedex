package ics.uci.edu.firedex.subscriber.mqtt;

public interface OnMessage {
	
	public void onMessage(String topic, String message);

}
