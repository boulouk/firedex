package edu.uci.ics.utility;

import java.util.Random;

public class RandomUtility {
	private static final Random random;
	
	static {
		random = new Random();
	}
	
	private RandomUtility() {
		
	}
	
	public static int randomInteger(int lowerBound, int upperBound) {
		int value = lowerBound + (  random.nextInt( (upperBound - lowerBound + 1) )  );
		return (value);
	}
	
	public static double randomDouble(int lowerBound, int upperBound) {
		double x = random.nextDouble();
		int x1 = 0; int y1 = lowerBound;
		int x2 = 1; int y2 = upperBound;
		double y = ( (x - x1) * (y2 - y1) ) / (x2 - x1) + y1;
		return (y);
	}
	
	public static String randomString(int length) {
		String alphabet = "abcdefghijklmnopqrstuvwxyz";
		
		StringBuilder stringBuilder = new StringBuilder();
		for (int i = 0; i < length; i++) {
			int index = random.nextInt(alphabet.length());
			stringBuilder.append( alphabet.charAt(index) );
		}
		
		return ( stringBuilder.toString() );
	}

}
