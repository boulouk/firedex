package edu.uci.ics.subscriber.web;

import java.net.InetSocketAddress;
import java.net.UnknownHostException;

import org.java_websocket.WebSocket;
import org.java_websocket.handshake.ClientHandshake;
import org.java_websocket.server.WebSocketServer;

public class SubscriberEndPoint extends WebSocketServer {
	private WebSocket client;
	private OnWebMessage onWebMessage;

	public SubscriberEndPoint(int port) throws UnknownHostException {
		super( new InetSocketAddress(port) );
		
		this.client = null;
		this.onWebMessage = null;
	}
	
	public void setOnWebMessage(OnWebMessage onWebMessage) {
		this.onWebMessage = onWebMessage;
	}

	@Override
	public void onClose(WebSocket client, int code, String reason, boolean remote) {
		this.client = null;
	}

	@Override
	public void onError(WebSocket client, Exception exception) {
		this.client = null;
	}
	
	public void sendMessage(String message) {
		if ( this.client != null )
			this.client.send(message);
	}

	@Override
	public void onMessage(WebSocket client, String message) {
		if ( this.client != null )
			onWebMessage.onWebMessage(message);
	}

	@Override
	public void onOpen(WebSocket client, ClientHandshake handshake) {
		this.client = client;
	}

}
