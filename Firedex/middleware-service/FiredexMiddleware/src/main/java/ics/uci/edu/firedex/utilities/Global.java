package ics.uci.edu.firedex.utilities;

public class Global {
	public static final String BROKER = "tcp://iqueue.ics.uci.edu:1883"; // Public UCI Mosquitto broker
	public static final String CLIENT = "FiredexMiddleware";
	
	public static final String TOPIC = "priorities";
	public static final int QUALITY_OF_SERVICE = 2;
	public static final boolean RETAINED = true;
	
	private Global() { }
	
}
