package ics.uci.edu.firedex.subscriber.model;

public class Priority {
	private int priorityLevel;
	private int priorityPort;
	
	public Priority() { }
	
	public Priority(int priorityLevel, int priorityPort) {
		this.priorityLevel = priorityLevel;
		this.priorityPort = priorityPort;
	}

	public int getPriorityLevel() {
		return (priorityLevel);
	}

	public void setPriorityLevel(int priorityLevel) {
		this.priorityLevel = priorityLevel;
	}

	public int getPriorityPort() {
		return (priorityPort);
	}

	public void setPriorityPort(int priorityPort) {
		this.priorityPort = priorityPort;
	}

}
