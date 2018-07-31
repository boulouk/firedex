package edu.uci.ics.mqtt;

import edu.uci.ics.configuration.Configuration;
import edu.uci.ics.exception.FiredexException;

public class BrokerConnectionFactory {
	
	private BrokerConnectionFactory() {
		
	}
	
	public static BrokerConnection create(String type, Configuration configuration, int localPort) throws FiredexException {
		if ( type.equals("UDP") )
			return ( new UDPBrokerConnection(configuration, localPort) );
		else if ( type.equals("TCP") )
			return ( new TCPBrokerConnection(configuration, localPort) );
		else
			throw ( new FiredexException() );
	}

}
