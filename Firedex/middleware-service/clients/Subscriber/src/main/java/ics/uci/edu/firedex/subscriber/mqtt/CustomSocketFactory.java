package ics.uci.edu.firedex.subscriber.mqtt;

import java.io.IOException;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.UnknownHostException;

import javax.net.SocketFactory;

public class CustomSocketFactory extends SocketFactory {
	private int customPort;
	
	public CustomSocketFactory(int customPort) {
		this.customPort = customPort;
	}
	
	@Override
	public Socket createSocket() throws IOException {
		Socket socket = new Socket();
		socket.bind( new InetSocketAddress(customPort) );
		return (socket);
	}
	
	@Override
	public Socket createSocket(String host, int port) throws IOException, UnknownHostException {
		return ( new Socket(host, port, InetAddress.getLocalHost(), customPort) );
	}

	@Override
	public Socket createSocket(InetAddress host, int port) throws IOException {
		return ( new Socket(host, port, InetAddress.getLocalHost(), customPort) );
	}

	@Override
	public Socket createSocket(String host, int port, InetAddress localHost, int localPort) throws IOException, UnknownHostException {
		return ( new Socket(host, port, InetAddress.getLocalHost(), customPort) );
	}

	@Override
	public Socket createSocket(InetAddress address, int port, InetAddress localAddress, int localPort) throws IOException {
		return ( new Socket(address, port, InetAddress.getLocalHost(), customPort) );
	}
	
}
