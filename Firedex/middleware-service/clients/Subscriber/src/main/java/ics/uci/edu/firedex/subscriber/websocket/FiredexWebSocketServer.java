package ics.uci.edu.firedex.subscriber.websocket;

import java.net.InetSocketAddress;

import org.java_websocket.WebSocket;
import org.java_websocket.handshake.ClientHandshake;
import org.java_websocket.server.WebSocketServer;

public abstract class FiredexWebSocketServer extends WebSocketServer {
	private WebSocket webSocket;

	public FiredexWebSocketServer(int port) {
		super( new InetSocketAddress(port) );
	}
	
	public WebSocket getWebSocket() {
		return (webSocket);
	}
	
	@Override
	public void onStart() { }
	
	@Override
	public void onOpen(WebSocket webSocket, ClientHandshake clientHandshake) { 
		this.webSocket = webSocket;
	}
	
	@Override
	public abstract void onMessage(WebSocket webSocket, String message);
	
	@Override
	public void onError(WebSocket webSocket, Exception exception) { }
	
	@Override
	public void onClose(WebSocket webSocket, int code, String reason, boolean remote) {
		webSocket = null;
	}

}
