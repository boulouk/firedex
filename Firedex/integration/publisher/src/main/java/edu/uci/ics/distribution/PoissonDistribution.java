package edu.uci.ics.distribution;

import java.util.ArrayList;
import java.util.List;

public class PoissonDistribution {
	private double lambda;
	private List<Double> values;

	public PoissonDistribution(double lambda) {
		this.lambda = lambda;
		this.values = new ArrayList<>();
		
		values.add(lambda);
	}

	public double next() {
		double value = -Math.log( Math.random() ) / lambda;
		values.add(value);
		return (value);
	}
	
	public double average() {
		double sum = 0;
		
		for ( Double value : values )
			sum += value;
		
		double average = (double) sum / (double) values.size();
		return (average);
	}
	
}
