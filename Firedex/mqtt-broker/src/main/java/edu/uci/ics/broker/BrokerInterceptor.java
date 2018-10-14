package edu.uci.ics.broker;

import io.moquette.interception.AbstractInterceptHandler;
import io.moquette.interception.messages.InterceptConnectMessage;
import io.moquette.interception.messages.InterceptConnectionLostMessage;
import io.moquette.interception.messages.InterceptDisconnectMessage;
import io.moquette.interception.messages.InterceptPublishMessage;
import io.moquette.interception.messages.InterceptSubscribeMessage;
import io.moquette.interception.messages.InterceptUnsubscribeMessage;

public class BrokerInterceptor extends AbstractInterceptHandler  {
	
	public BrokerInterceptor() {
		
	}
	
	@Override
	public void onConnect(InterceptConnectMessage connectMessage) {
		System.out.println("---");
		System.out.println("connection");
		System.out.println("identifier: " + connectMessage.getClientID());
		System.out.println("---");
	}
	
	@Override
	public void onPublish(InterceptPublishMessage publishMessage) {
		System.out.println("---");
		System.out.println("publish");
		System.out.println("topic: " + publishMessage.getTopicName());
		System.out.println("---");
	}
	
	@Override
	public void onSubscribe(InterceptSubscribeMessage subscribeMessage) {
		System.out.println("---");
		System.out.println("subscription");
		System.out.println("topic: " + subscribeMessage.getTopicFilter());
		System.out.println("identifier: " + subscribeMessage.getClientID());
		System.out.println("---");
	}
	
	@Override
	public void onUnsubscribe(InterceptUnsubscribeMessage unsubscribeMessage) {
		System.out.println("---");
		System.out.println("unsubscription");
		System.out.println("topic: " + unsubscribeMessage.getTopicFilter());
		System.out.println("identifier: " + unsubscribeMessage.getClientID());
		System.out.println("---");
	}
	
	@Override
	public void onConnectionLost(InterceptConnectionLostMessage connectionLostMessage) {
		System.out.println("---");
		System.out.println("connection-lost");
		System.out.println("identifier: " + connectionLostMessage.getClientID());
		System.out.println("---");
	}
	
	@Override
	public void onDisconnect(InterceptDisconnectMessage disconnectMessage) {
		System.out.println("---");
		System.out.println("disconnection");
		System.out.println("identifier: " + disconnectMessage.getClientID());
		System.out.println("---");
	}

	@Override
	public String getID() {
		return ("BrokerInterceptor");
	}
	
}
