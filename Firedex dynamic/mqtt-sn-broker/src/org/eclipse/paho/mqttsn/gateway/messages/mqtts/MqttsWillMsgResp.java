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

/**
 * This object represents a Mqtts WILLMSGRESP message.
 * 
 */
public class MqttsWillMsgResp extends MqttsMessage{
	
	/**
	 * MqttsWillMsgResp constructor.Sets the appropriate message type. 
	 */
	public MqttsWillMsgResp() {
		msgType = MqttsMessage.WILLMSGRESP;
	}
	
	/**
	 * MqttsWillMsgResp constructor.Sets the appropriate message type and constructs 
	 * a Mqtts WILLMSGRESP message from a received byte array.
	 * @param data: The buffer that contains the WILLMSGRESP message.
	 */
	public MqttsWillMsgResp(byte[] data){
		msgType = MqttsMessage.WILLMSGRESP;
	}
	
	/**
	 * Method to convert this message to a byte array for transmission.
	 * @return A byte array containing the WILLMSGRESP message as it should appear on the wire.
	 */
	public byte [] toBytes() {
		int length = 2;
		byte[] data = new byte[length];
		data[0] = (byte)length;
		data[1] = (byte)msgType;		
		return data;
	}
}