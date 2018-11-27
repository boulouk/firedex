/*******************************************************************************
 * Copyright (c) 2008, 2014 IBM Corp.
 *
 * All rights reserved. This program and the accompanying materials
 * are made available under the terms of the Eclipse Public License v1.0
 * and Eclipse Distribution License v1.0 which accompany this distribution. 
 *
 * The Eclipse Public License is available at 
 *    http://www.eclipse.org/legal/epl-v10.html
 * and the Eclipse Distribution License is available at 
 *   http://www.eclipse.org/org/documents/edl-v10.php.
 *
 * Contributors:
 *    Ian Craggs - initial API and implementation and/or initial documentation
 *******************************************************************************/

package org.eclipse.paho.mqttsn.gateway.messages.mqtts;

import java.io.UnsupportedEncodingException;
import org.eclipse.paho.mqttsn.gateway.utils.Utils;


/**
 * This object represents a Mqtts WILLTOPICUPD message.
 * 
 */
public class MqttsWillTopicUpd extends MqttsMessage {
	
	//Mqtts WILLTOPICUPD fields
	private int qos;
	private boolean retain;
	private String willTopic;
	
	/**
	 * MqttsWillTopicUpd constructor.Sets the appropriate message type. 
	 */
	public MqttsWillTopicUpd() {
		msgType = MqttsMessage.WILLTOPICUPD;
	}
	
	/** 
	 * MqttsWillTopicUpd constructor.Sets the appropriate message type and constructs 
	 * a Mqtts WILLTOPICUPD message from a received byte array.
	 * @param data: The buffer that contains the WILLTOPICUPD message.
	 */
	public MqttsWillTopicUpd(byte[] data) {
		msgType = MqttsMessage.WILLTOPICUPD;
		qos = (data[2] & 0x60) >> 5;
		retain = ((data[2] & 0x10) >> 4 !=0);
		try {
			willTopic = new String(data, 3, data[0] - 3, Utils.STRING_ENCODING);
		} catch (UnsupportedEncodingException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	/**
	 * Method to convert this message to a byte array for transmission.
	 * @return A byte array containing the WILLTOPICUPD message as it should appear on the wire.
	 */
	public byte[] toBytes(){
		int length = 3 + willTopic.length();
		byte[] data = new byte[length];
		int flags = 0;
		if(qos == -1) {
			flags |= 0x60; 
		} else if(qos == 0) {
		
		} else if(qos == 1) {
			flags |= 0x20;
		} else if(qos == 2) {
			flags |= 0x40;
		} else {
			throw new IllegalArgumentException("Unknown QoS value: " + qos);
		}
		if(retain) {
			flags |= 0x10;
		}

		data[0] = (byte)length;   
		data[1] = (byte)msgType;  
		data[2] = (byte)flags;
		System.arraycopy(willTopic.getBytes(), 0, data, 3, willTopic.length());	
		return data;
	}

	public int getQos() {
		return qos;
	}
	public void setQos(int qoS) {
		this.qos = qoS;
	}
	public boolean isRetain() {
		return retain;
	}
	public void setRetain(boolean retain) {
		this.retain = retain;
	}
	public String getWillTopic() {
		return willTopic;
	}
	public void setWillTopic(String willTopic) {
		this.willTopic = willTopic;
	}
}