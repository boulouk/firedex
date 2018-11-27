package edu.uci.ics.broker;

import java.io.File;
import java.io.IOException;

import io.moquette.server.Server;

public class Broker {
	private Server server;
	private BrokerInterceptor brokerInterceptor;
	
	public Broker() {
		this.server = new Server();
		this.brokerInterceptor = new BrokerInterceptor();
	}
	
	public void start(File configurationFile) throws IOException {
		server.startServer(configurationFile);
		server.addInterceptHandler(brokerInterceptor);
	}
	
	public void stop() {
		server.removeInterceptHandler(brokerInterceptor);
		server.stopServer();
	}

}
