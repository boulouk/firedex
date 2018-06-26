package ics.uci.edu.firedex.subscriber.websocket;

import org.java_websocket.WebSocket;

import ics.uci.edu.firedex.subscriber.message.EventMessage;
import ics.uci.edu.firedex.subscriber.model.Event;
import ics.uci.edu.firedex.subscriber.model.MessageQueue;
import ics.uci.edu.firedex.subscriber.utilities.JsonUtility;

public class MessageForwarder {
	private MessageQueue messageQueue;
	private FiredexWebSocketServer firedexWebSocketServer;
	
	public MessageForwarder(MessageQueue messageQueue, FiredexWebSocketServer firedexWebSocketServer) {
		this.messageQueue = messageQueue;
		this.firedexWebSocketServer = firedexWebSocketServer;
	}

	public void start() {
		Thread thread = new Thread( () -> run() );
		thread.start();
	}
	
	public void run() {
		while ( true ) {
			try {
				Event event = messageQueue.blockingTake();
				EventMessage eventMessage = new EventMessage(event);
				WebSocket webSocket = firedexWebSocketServer.getWebSocket();
				if ( webSocket != null ) {
					String message = JsonUtility.toJson(eventMessage);
					webSocket.send(message);
				}
			} catch (Exception exception) { }
		}
	}

}
