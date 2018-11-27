/*******************************************************************************
 * Copyright (c) 2008, 2013 IBM Corp.
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

package org.eclipse.paho.mqttsn.gateway.exceptions;

public class MqttsException extends Exception{
	private static final long serialVersionUID = 1L;

	private Throwable cause = null; 

	public MqttsException() {
		super();
	}

	public MqttsException(String s) {
		super(s);
	}

	public MqttsException(Throwable cause) {
		super( (cause==null)? null : cause.toString() );
		this.cause = cause;
	}

	public Throwable getCause(){
		return this.cause;
	}
}
