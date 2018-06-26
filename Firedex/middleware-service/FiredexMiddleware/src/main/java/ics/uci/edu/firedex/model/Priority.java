package ics.uci.edu.firedex.model;

public class Priority {
	private int priorityLevel;
	private int priorityPort;
	
	public Priority(int priorityLevel, int priorityPort) {
		this.priorityLevel = priorityLevel;
		this.priorityPort = priorityPort;
	}
	
	public int getPriorityLevel() {
		return (priorityLevel);
	}
	
	public int getPriorityPort() {
		return (priorityPort);
	}

}
