package edu.uci.ics.mqtt;

import edu.uci.ics.model.SubscriptionConfiguration;

public interface OnEvent {
	
	public void onEvent(SubscriptionConfiguration subscription, String event);

}
