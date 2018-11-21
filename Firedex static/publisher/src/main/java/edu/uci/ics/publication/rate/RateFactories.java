package edu.uci.ics.publication.rate;

import java.util.HashMap;
import java.util.Map;
import java.util.Set;

public class RateFactories {
	private static Map<String, RateFactory> rateFactories;

	static {
		rateFactories = new HashMap<>();
		
		DeterministicRateFactory deterministicRateFactory = new DeterministicRateFactory();
		rateFactories.put(deterministicRateFactory.name(), deterministicRateFactory);
		RandomRateFactory randomRateFactory = new RandomRateFactory();
		rateFactories.put(randomRateFactory.name(), randomRateFactory);
	}

	private RateFactories() {
		
	}
	
	public static Set<String> all() {
		return ( rateFactories.keySet() );
	}

	public static RateFactory create(String name) {
		return ( rateFactories.get(name) );
	}

}
