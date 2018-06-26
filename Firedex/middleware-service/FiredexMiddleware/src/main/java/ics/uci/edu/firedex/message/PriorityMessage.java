package ics.uci.edu.firedex.message;

import java.util.List;

import ics.uci.edu.firedex.model.Priority;

public class PriorityMessage {
	private List<Priority> priorities;
	
	public PriorityMessage(List<Priority> priorities) {
		this.priorities = priorities;
	}
	
	public List<Priority> getPriorities() {
		return (priorities);
	}

}
