package ics.uci.edu.firedex.subscriber;

public class Subscriber {

	public static void main(String[] args) throws Exception {
		Manager manager = new Manager();
		manager.start();
		Thread.sleep( Long.MAX_VALUE );
	}

}
