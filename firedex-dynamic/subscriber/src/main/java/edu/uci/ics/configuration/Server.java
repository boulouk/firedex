package edu.uci.ics.configuration;

public class Server {
	private Middleware middleware;
	private Broker broker;
	private Web web;
	
	public Server(Middleware middleware, Broker broker, Web web) {
		this.middleware = middleware;
		this.broker = broker;
		this.web = web;
	}
	
	public Middleware getMiddleware() {
		return (middleware);
	}
	
	public Broker getBroker() {
		return (broker);
	}
	
	public Web getWeb() {
		return (web);
	}

}
