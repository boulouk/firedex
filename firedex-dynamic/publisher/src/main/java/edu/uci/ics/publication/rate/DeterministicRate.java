package edu.uci.ics.publication.rate;

public class DeterministicRate implements Rate {
	private double interval;
	
	public DeterministicRate(double rate) {
		this.interval = 1 / rate;
	}
	
	@Override
	public double next() {
		return (interval);
	}

}
