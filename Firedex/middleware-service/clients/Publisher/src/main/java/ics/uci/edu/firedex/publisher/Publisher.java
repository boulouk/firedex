package ics.uci.edu.firedex.publisher;

import java.util.Random;

import org.eclipse.paho.client.mqttv3.MqttException;

import ics.uci.edu.firedex.publisher.message.EventMessage;
import ics.uci.edu.firedex.publisher.model.Event;
import ics.uci.edu.firedex.publisher.utilities.Global;
import ics.uci.edu.firedex.publisher.utilities.JsonUtility;

public class Publisher {
	
	public static void main(String[] args) throws InterruptedException, MqttException {
		String broker = Global.BROKER;
		String identifier = Global.CLIENT;
		
		BrokerConnection brokerConnection = new BrokerConnection(broker, identifier);
		brokerConnection.connect();
		
		int qualityOfService = Global.QUALITY_OF_SERVICE;
		boolean retained = Global.RETAINED;
		
		for (int i = 0; i < 100000; i++) {
			EventMessage eventMessage = eventMessage();
			String eventContent = JsonUtility.toJson(eventMessage);
			String topic = eventMessage.getEvent().getTopic();
			brokerConnection.publish(topic, eventContent, qualityOfService, retained);
			
			Thread.sleep(5000);
		}
		
		brokerConnection.disconnect();
	}
	
	private static EventMessage eventMessage() {
		Random random = new Random();
		
		String topic = Global.TOPIC.get(  random.nextInt( Global.TOPIC.size() )  );
		int value = Global.VALUE.get(  random.nextInt( Global.VALUE.size() )  );
		String status = Global.STATUS.get(  random.nextInt( Global.STATUS.size() )  );
		String time = Global.TIME.get(  random.nextInt( Global.TIME.size() )  );
		String device = Global.DEVICE.get(  random.nextInt( Global.DEVICE.size() )  );
		String source = Global.SOURCE.get(  random.nextInt( Global.SOURCE.size() )  );
		
		Event event = new Event(topic, value, status, time, device, source);
		EventMessage eventMessage = new EventMessage(event);
		return (eventMessage);
	}
	
}
