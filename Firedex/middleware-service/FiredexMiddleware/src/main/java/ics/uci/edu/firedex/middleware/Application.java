package ics.uci.edu.firedex.middleware;

import java.util.ArrayList;
import java.util.List;

import org.eclipse.paho.client.mqttv3.MqttException;

import ics.uci.edu.firedex.message.PriorityMessage;
import ics.uci.edu.firedex.model.Priority;
import ics.uci.edu.firedex.utilities.Global;
import ics.uci.edu.firedex.utilities.JsonUtility;

public class Application {
	
	public static void main(String[] args) throws MqttException {
		String broker = Global.BROKER;
		String identifier = Global.CLIENT;
		
		BrokerConnection brokerConnection = new BrokerConnection(broker, identifier);
		brokerConnection.connect();
		
		String topic = Global.TOPIC;
		int qualityOfService = Global.QUALITY_OF_SERVICE;
		boolean retained = Global.RETAINED;
		
		PriorityMessage wrongPriorityMessage = wrongPriorityMessage();
		String wrongContent = JsonUtility.toJson(wrongPriorityMessage);
		brokerConnection.publish(topic, wrongContent, qualityOfService, retained);
		System.out.println( String.format("Published message on topicp: %s", topic) );
		
		PriorityMessage defaultPriorityMessage = defaultPriorityMessage();
		String defaultContent = JsonUtility.toJson(defaultPriorityMessage);
		brokerConnection.publish(topic, defaultContent, qualityOfService, retained);
		System.out.println( String.format("Published message on topicp: %s", topic) );
		
		brokerConnection.disconnect();
	}
	
	private static PriorityMessage wrongPriorityMessage() {
		Priority priority0 = new Priority(0, 9444);
		Priority priority1 = new Priority(1, 1332);
		Priority priority2 = new Priority(2, 10041);
		Priority priority3 = new Priority(3, 50000);
		List<Priority> priorities = new ArrayList<Priority>();
		priorities.add(priority0);
		priorities.add(priority1);
		priorities.add(priority2);
		priorities.add(priority3);
		
		PriorityMessage priorityMessage = new PriorityMessage(priorities);
		return (priorityMessage);
	}
	
	private static PriorityMessage defaultPriorityMessage() {
		Priority priority0 = new Priority(0, 10000);
		Priority priority1 = new Priority(1, 10001);
		Priority priority2 = new Priority(2, 10002);
		Priority priority3 = new Priority(3, 10003);
		List<Priority> priorities = new ArrayList<Priority>();
		priorities.add(priority0);
		priorities.add(priority1);
		priorities.add(priority2);
		priorities.add(priority3);
		
		PriorityMessage priorityMessage = new PriorityMessage(priorities);
		return (priorityMessage);
	}
	
}
