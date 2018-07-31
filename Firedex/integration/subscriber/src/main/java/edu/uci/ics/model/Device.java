package edu.uci.ics.model;

import edu.uci.ics.utility.RandomUtility;

public class Device {
	private String identifier;
	private String name;
	private String model;
	private String version;
	
	public Device(String identifier, String name, String model, String version) {
		this.identifier = identifier;
		this.name = name;
		this.model = model;
		this.version = version;
	}

	public String getIdentifier() {
		return (identifier);
	}

	public String getName() {
		return (name);
	}

	public String getModel() {
		return (model);
	}
	
	public String getVersion() {
		return (version);
	}
	
	public static Device random() {
		String identifier = RandomUtility.randomString(6);
		String name = RandomUtility.randomString(6);
		String model = RandomUtility.randomString(3);
		String version = RandomUtility.randomString(1);
		
		Device device = new Device(identifier, name, model, version);
		return (device);
	}

}
