package ics.uci.edu.firedex.subscriber.mqtt;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.eclipse.paho.client.mqttv3.MqttException;

import ics.uci.edu.firedex.subscriber.message.PriorityMessage;
import ics.uci.edu.firedex.subscriber.model.Priority;
import ics.uci.edu.firedex.subscriber.utilities.Global;
import ics.uci.edu.firedex.subscriber.utilities.JsonUtility;

public class PriorityService {
	private static PriorityService instance;
	
	private Map<Integer, Integer> priorityService;
	private boolean initialized;
	
	private PriorityConnection priorityConnection;
	
	private PriorityService() { }
	
	public static PriorityService getInstance() {
		if ( instance == null )
			instance = new PriorityService();
		return (instance);
	}
	
	public void initialize(String broker, String identifier) throws MqttException {
		priorityService = new HashMap<>();
		initialized = false;
		
		MessageHandler messageHandler = new MessageHandler( (topic, message) -> onPriorityChanged(message) );
		priorityConnection = new PriorityConnection(broker, identifier, messageHandler);
		priorityConnection.connect();
		priorityConnection.subscribe(Global.PRIORITY_TOPIC);
	}
	
	public boolean isInitialized() {
		return (initialized);
	}
	
	public List<Integer> getPriorities() {
		List<Integer> priorities = new ArrayList<>();
		priorities.addAll( priorityService.keySet() );
		return (priorities);
	}
	
	public int getPort(int priority) {
		return ( priorityService.getOrDefault(priority, -1) );
	}
	
	private void onPriorityChanged(String strMessage) {
		PriorityMessage priorityMessage = JsonUtility.fromJson(strMessage, PriorityMessage.class);
		priorityService.clear();
		for ( Priority priority : priorityMessage.getPriorities() )
			priorityService.put( priority.getPriorityLevel(), priority.getPriorityPort() );
		
		initialized = true;
	}

}
