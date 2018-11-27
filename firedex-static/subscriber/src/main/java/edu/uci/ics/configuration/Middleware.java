package edu.uci.ics.configuration;

public class Middleware {
	private String host;
	private int port;
	
	public Middleware(String host, int port) {
		this.host = host;
		this.port = port;
	}
	
	public String getHost() {
		return (host);
	}
	
	public int getPort() {
		return (port);
	}

}
