# Firedex

FireDeX is a cross-layer middleware that supports timely delivery of mission-critical messages (i.e. events) over an IoT data exchange service. Emergency scenarios may challenge/congest the network infrastructure. FireDeX addresses these situations by prioritizing event delivery and by dropping some low priority events.

See also the following resources for more details on FireDeX:
- https://www.ics.uci.edu/~dsm/papers/2018/firedex-middleware.pdf
- https://www.ics.uci.edu/~dsm/papers/2018/firedex-poster-abstract.pdf

## Getting started
These instructions will get you a copy of the project up and running on your local machine.

## Prerequisites

Install [VirtualBox](https://www.virtualbox.org/).  
Install Ubuntu 14.04.

## Installing

We will need to install:
- Java
- Git
- Mininet
- Modified version of OVS
- PyCharm and Eclipse

### Java
To install Java type the following commands on your terminal.

```
sudo apt-get-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install oracle-java8-installer
```

### Git
To install Git type the following command on your terminal.

```
sudo apt-get install git
```

Download the FireDeX repository and import the FireDeX.vbox file in VirtualBox, then launch the Virtual Machine.

Note:
username = firedex
password = firedex

...

## Authors
List of authors.
