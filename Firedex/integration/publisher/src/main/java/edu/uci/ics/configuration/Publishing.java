package edu.uci.ics.configuration;

public class Publishing {
	private String topic;
	private int qualityOfService;
	private boolean retained;
	private int parameter;
	
	public Publishing(String topic, int qualityOfService, boolean retained, int parameter) {
		this.topic = topic;
		this.qualityOfService = qualityOfService;
		this.retained = retained;
		this.parameter = parameter;
	}

	public String getTopic() {
		return (topic);
	}

	public int getQualityOfService() {
		return (qualityOfService);
	}

	public boolean isRetained() {
		return (retained);
	}

	public int getParameter() {
		return (parameter);
	}
	
}
