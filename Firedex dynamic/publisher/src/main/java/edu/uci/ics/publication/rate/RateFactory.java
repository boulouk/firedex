package edu.uci.ics.publication.rate;

public interface RateFactory {
	
	public String name();
	public Rate create(double rate);

}