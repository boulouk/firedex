package ics.uci.edu.firedex.subscriber.model;

public class Request {
	private String type;
	private String content;
	
	public Request() { }

	public Request(String type, String content) {
		this.type = type;
		this.content = content;
	}

	public String getType() {
		return (type);
	}

	public void setType(String type) {
		this.type = type;
	}

	public String getContent() {
		return (content);
	}

	public void setContent(String content) {
		this.content = content;
	}

}
