package edu.uci.ics.model.web;

public class WebRequest {
	private String type;
	private String content;
	
	public WebRequest(String type, String content) {
		this.type = type;
		this.content = content;
	}
	
	public String getType() {
		return (type);
	}
	
	public String getContent() {
		return (content);
	}
	
}
