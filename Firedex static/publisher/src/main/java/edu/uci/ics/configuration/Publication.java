package edu.uci.ics.configuration;

public class Publication {
	private String topic;
	private String rateType;
	private double rate;
	private int messageSize;
	private int qualityOfService;
	private boolean retained;

	public Publication(String topic, String rateType, double rate, int messageSize, int qualityOfService, boolean retained) {
		this.topic = topic;
		this.rateType = rateType;
		this.rate = rate;
		this.messageSize = messageSize;
		this.qualityOfService = qualityOfService;
		this.retained = retained;
	}

	public String getTopic() {
		return (topic);
	}

	public String getRateType() {
		return (rateType);
	}

	public double getRate() {
		return (rate);
	}

	public int getMessageSize() {
		return (messageSize);
	}

	public int getQualityOfService() {
		return (qualityOfService);
	}

	public boolean isRetained() {
		return (retained);
	}
	
}
