package edu.uci.ics.model;

import edu.uci.ics.utility.RandomUtility;

public class Location {
	private double latitude;
	private double longitude;
	private int floor;
	private String description;
	
	public Location(double latitude, double longitude, int floor, String description) {
		this.latitude = latitude;
		this.longitude = longitude;
		this.floor = floor;
		this.description = description;
	}

	public double getLatitude() {
		return (latitude);
	}
	
	public double getLongitude() {
		return (longitude);
	}
	
	public int getFloor() {
		return (floor);
	}
	
	public String getDescription() {
		return (description);
	}
	
	public static Location random() {
		double latitude = RandomUtility.randomDouble(0, 90);
		double longitude = RandomUtility.randomDouble(0, 180);
		int floor = RandomUtility.randomInteger(1, 10);
		String description = RandomUtility.randomString(0);
		
		Location location = new Location(latitude, longitude, floor, description);
		return (location);
	}

}
