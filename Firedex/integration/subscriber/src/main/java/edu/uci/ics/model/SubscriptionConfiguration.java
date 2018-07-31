package edu.uci.ics.model;

public class SubscriptionConfiguration {
	private String identifier;
	private String ip;
	private String mac;
	private String topic;
	private int utilityFunction;
	private int port;
	private int priority;
	private int dropRate;
	
	public SubscriptionConfiguration(String identifier, String ip, String mac, String topic, int utilityFunction, int port, int priority, int dropRate) {
		this.identifier = identifier;
		this.ip = ip;
		this.mac = mac;
		this.topic = topic;
		this.utilityFunction = utilityFunction;
		this.port = port;
		this.priority = priority;
		this.dropRate = dropRate;
	}

	public String getIdentifier() {
		return (identifier);
	}

	public String getIp() {
		return (ip);
	}

	public String getMac() {
		return (mac);
	}

	public String getTopic() {
		return (topic);
	}

	public int getUtilityFunction() {
		return (utilityFunction);
	}

	public int getPort() {
		return (port);
	}

	public int getPriority() {
		return (priority);
	}

	public int getDropRate() {
		return (dropRate);
	}

}
