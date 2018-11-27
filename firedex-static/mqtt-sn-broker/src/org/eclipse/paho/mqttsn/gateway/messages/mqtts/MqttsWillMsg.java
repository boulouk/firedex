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
 * This object represents a Mqtts WILLMSG message.
 * 
 */
public class MqttsWillMsg extends MqttsMessage {
	
	//Mqtts WILLMSG fields
	private String willMsg;
	
	/**
	 * MqttsWillMsg constructor.Sets the appropriate message type. 
	 */
	public MqttsWillMsg() {
		msgType = MqttsMessage.WILLMSG; 
	}
	
	/**
	 * MqttsWillMsg constructor.Sets the appropriate message type and constructs 
	 * a Mqtts WILLMSG message from a received byte array.
	 * @param data: The buffer that contains the WILLMSG message.
	 */
	public MqttsWillMsg(byte[] data) {
		msgType = MqttsMessage.WILLMSG;
		try {
			willMsg = new String(data, 2, data[0] - 2, Utils.STRING_ENCODING);
		} catch (UnsupportedEncodingException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	/**
	 * Method to convert this message to a byte array for transmission.
	 * @return A byte array containing the WILLMSG message as it should appear on the wire.
	 * (Don't needed in the GW)
	 */
	public byte[] toBytes(){
		int length = willMsg.length() + 2;
		byte[] data = new byte[length];
		data[0] = (byte)length;   
		data[1] = (byte)msgType;  
		System.arraycopy(willMsg.getBytes(), 0, data, 2, willMsg.length());	
		return data;		
	}

	public String getWillMsg() {
		return willMsg;
	}

	public void setWillMsg(String willMsg) {
		this.willMsg = willMsg;
	}
}