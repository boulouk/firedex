package edu.uci.ics.publication.rate;

public class DeterministicRateFactory implements RateFactory {
	
	public DeterministicRateFactory() {
		
	}
	
	@Override
	public String name() {
		return ("deterministic");
	}
	
	@Override
	public Rate create(double rate) {
		DeterministicRate deterministicRate = new DeterministicRate(rate);
		return (deterministicRate);
	}

}
