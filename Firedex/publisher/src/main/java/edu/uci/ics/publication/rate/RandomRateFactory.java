package edu.uci.ics.publication.rate;

public class RandomRateFactory implements RateFactory {

	public RandomRateFactory() {
		
	}
	
	@Override
	public String name() {
		return ("random");
	}
	
	@Override
	public Rate create(double rate) {
		RandomRate randomRate = new RandomRate(rate);
		return (randomRate);
	}	

}
