package edu.uci.ics.mqtt;

import edu.uci.ics.exception.FiredexException;
import edu.uci.ics.model.SubscriptionConfiguration;

public interface BrokerConnection {

	int getLocalPort();

	void connect() throws FiredexException;

	void subscribe(SubscriptionConfiguration subscriptionConfiguration) throws FiredexException;

	void disconnect() throws FiredexException;

	void addOnEventListener(OnEvent onEventListener);

	void removeOnEventListener(OnEvent onEventListener);

}