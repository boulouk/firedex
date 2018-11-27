package edu.uci.ics.utility;

import java.lang.reflect.Type;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

public class JsonUtility {
	private static final Gson gson;
	
	static {
		GsonBuilder gsonBuilder = new GsonBuilder();
		gsonBuilder.setPrettyPrinting();
		gson = gsonBuilder.create();
	}
	
	private JsonUtility() {
		
	}
	
	public static String toJson(Object object) {
		return ( gson.toJson(object) );
	}
	
	public static <T> T fromJson(String json, Type type) {
		return ( gson.fromJson(json, type) );
	}

}
