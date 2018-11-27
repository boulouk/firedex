package edu.uci.ics.configuration;

public class Server {
	private Middleware middleware;
	private Broker broker;
	
	public Server(Middleware middleware, Broker broker) {
		this.middleware = middleware;
		this.broker = broker;
	}
	
	public Middleware getMiddleware() {
		return (middleware);
	}
	
	public Broker getBroker() {
		return (broker);
	}

}
