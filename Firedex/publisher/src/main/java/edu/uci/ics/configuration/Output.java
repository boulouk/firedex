package edu.uci.ics.configuration;

public class Output {
	private String logFile;
	private String outputFile;
	
	public Output(String logFile, String outputFile) {
		this.logFile = logFile;
		this.outputFile = outputFile;
	}
	
	public String getLogFile() {
		return (logFile);
	}
	
	public String getOutputFile() {
		return (outputFile);
	}

}
