package ics.uci.edu.firedex.subscriber.utilities;

public class Global {
	public static final int WEB_SOCKET_SERVER = 8888;
	
	public static final String BROKER = "tcp://iqueue.ics.uci.edu:1883"; // Public UCI Mosquitto broker
	public static final String CLIENT = "Subscriber";
	
	public static final String PRIORITY_CLIENT = CLIENT + "-" + "priority";
	public static final String PRIORITY_TOPIC = "priorities";
	
	private Global() { }
	
}
