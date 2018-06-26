package ics.uci.edu.firedex.utilities;

import java.lang.reflect.Type;

import com.google.gson.Gson;

public class JsonUtility {
	private static Gson gson;
	
	static {
		gson = new Gson();
	}
	
	private JsonUtility() { }
	
	public static String toJson(Object object) {
		return ( gson.toJson(object) );
	}
	
	public static <T> T fromJson(String json, Type type) {
		return ( gson.fromJson(json, type) );
	}

}
