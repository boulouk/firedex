package edu.uci.ics.mqtt;

import edu.uci.ics.model.Event;

public interface OnEvent {
	
	public void onEvent(String topic, int port, Event event);

}
