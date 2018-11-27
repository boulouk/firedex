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
 * This object represents a Mqtts ADVERTISE message.
 * 
 *
 */
public class MqttsAdvertise extends MqttsMessage {


	//Mqtts ADVERTISE fields
	private int gwId;
	private long duration;

	/**
	 * MqttsAdvertise constructor.Sets the appropriate message type. 
	 */
	public MqttsAdvertise() {
		msgType = MqttsMessage.ADVERTISE;
	}

	/**
	 * MqttsAdvertise constructor.Sets the appropriate message type and constructs
	 * a Mqtts ADVERTISE message from a received byte array.
	 * @param data: The buffer that contains the ADVERTISE message.
	 */
	public MqttsAdvertise(byte[] data) {
		msgType = MqttsMessage.ADVERTISE;
		gwId = (data[2] & 0xFF);
		duration = ((data[3] & 0xFF) << 8) + (data[4] & 0xFF);
	}

	/**
	 * Method to convert this message to a byte array for transmission.
	 * @return A byte array containing the ADVERTISE message as it should appear on the wire.
	 */
	public byte[] toBytes() {
		int length = 5;
		byte[] data = new byte[length];
		data[0] = (byte) length;
		data[1] = (byte) msgType;
		data[2] = (byte) gwId;
		data[3] = (byte) ((duration >> 8) & 0xFF);
		data[4] = (byte) (duration & 0xFF);
		return data;
	}

	public int getGwId() {
		return gwId;
	}

	public void setGwId(int gwId) {
		this.gwId = gwId;
	}

	public long getDuration() {
		return duration;
	}

	public void setDuration(long duration) {
		this.duration = duration;
	}
}