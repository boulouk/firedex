package edu.uci.ics.configuration;

public class Web {
	private boolean abilitate;
	private int port;
	
	public Web(boolean abilitate, int port) {
		this.abilitate = abilitate;
		this.port = port;
	}
	
	public boolean isAbilitate() {
		return (abilitate);
	}
	
	public int getPort() {
		return (port);
	}

}
