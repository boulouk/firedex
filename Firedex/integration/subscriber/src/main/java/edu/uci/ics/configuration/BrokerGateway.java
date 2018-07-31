package edu.uci.ics.configuration;

public class BrokerGateway {
	private String host;
	private int port;
	
	public BrokerGateway(String host, int port) {
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
