package ics.uci.edu.firedex.publisher.utilities;

import java.util.List;

import com.google.common.collect.ImmutableList;

public class Global {
	public static final String BROKER = "tcp://iqueue.ics.uci.edu:1883"; // Public UCI Mosquitto broker
	public static final String CLIENT = "Publisher";
	
	public static final List<String> TOPIC = ImmutableList.of("fire", "smoke", "temperature");
	public static final List<Integer> VALUE = ImmutableList.of(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
	public static final List<String> STATUS = ImmutableList.of("low", "medium", "high");
	public static final List<String> TIME = ImmutableList.of("June 14th, 2018", "June 15th, 2018", "June 16th, 2018");
	public static final List<String> DEVICE = ImmutableList.of("Arduino", "Raspberry PI 2", "Raspberry PI 3");
	public static final List<String> SOURCE = ImmutableList.of("10.0.0.1", "10.0.0.2", "10.0.0.3");
	
	public static final int QUALITY_OF_SERVICE = 0;
	public static final boolean RETAINED = false;
	
	private Global() { }
	
}
