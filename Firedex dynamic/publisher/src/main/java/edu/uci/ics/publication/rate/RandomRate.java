package edu.uci.ics.publication.rate;

import edu.uci.ics.utility.RandomUtility;

public class RandomRate implements Rate {
	private double rate;
	
	public RandomRate(double rate) {
		this.rate = rate;
	}
	
	@Override
	public double next() {
		double value = - Math.log( RandomUtility.randomDouble(0, 1) ) / rate;
		return (value);
	}
	
}
