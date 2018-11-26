# Firedex

Description of FireDeX.

See also the following resources for more details on FireDeX:
- https://www.ics.uci.edu/~dsm/papers/2018/firedex-middleware.pdf
- https://www.ics.uci.edu/~dsm/papers/2018/firedex-poster-abstract.pdf

## Getting started
These instructions will get you a copy of the FireDeX project up and running on your local machine. 

## Prerequisites

Install [VirtualBox](https://www.virtualbox.org/).  
Install Ubuntu 14.04.

## Installing - Alternative 1
These steps will walk you trough the installation of the FireDeX project from scratch (i.e. clean Ubuntu Virtual Machine).  

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

### Mininet
To install Mininet type the following commands on your terminal.

```
git clone git://github.com/mininet/mininet
mininet/util/install.sh -nfv
```

### OVS
To install the modified version of OVS type the following commands on your terminal.

```
sudo wget http://openvswitch.org/releases/openvswitch-2.1.0.tar.gz
sudo tar zxfv openvswitch-2.1.0.tar.gz
cd openvswitch-2.1.0/
sudo apt-get install build-essential fakeroot
sudo apt-get install debhelper autoconf automake libssl-dev pkg-config bzip2 openssl python-all procps python-qt4 python-zopeinterface python-twisted-conch dh-autoreconf
```

Follow the instructions [here](https://github.com/saeenali/openvswitch/wiki/Stochastic-Switching-using-Open-vSwitch-in-Mininet) to modify the standard version of OVS and then type the following commands on your terminal.

```
`DEB_BUILD_OPTIONS='parallel=8 nocheck' sudo fakeroot debian/rules binary`
cd ..
sudo dpkg -i openvswitch-common*.deb openvswitch-datapath-dkms*.deb openvswitch-pki*.deb openvswitch-switch*.deb
```

### PyCharm and Eclipse
Install [PyCharm](https://www.jetbrains.com/pycharm/) and [Eclipse](https://www.eclipse.org/).

### Finishing up
Finally you need to import the project dependencies (make sure that you are using Python 2.7).

#### FireDeX static dependencies
Run PyCharm (file _PY_CHARM_HOME/bin/pycharm.sh_) as root (sudo) and open the following projects from the _firedex-static_ directory:
- experimental-framework
- sdn-controller
- firedex-coordinator-service

Import the following dependencies:
- experimental-framework -> numpy, requests, matplotlib (add the Mininet project as a dependency)
- sdn-controller -> ryu (mark the _application_ directory as _Sources Root_, add the NetworkX project as a dependency)
- firedex-coordinator-service -> flask, numpy, requests

#### FireDeX dynamic dependencies

Run PyCharm (file _PY_CHARM_HOME/bin/pycharm.sh_) as root (sudo) and open the following projects from the _firedex-dynamic_ directory:
- experimental-framework
- sdn-controller
- firedex-coordinator-service

Import the following dependencies:
- experimental-framework ->
- sdn-controller ->
- firedex-coordinator-service ->

## Installing - Alternative 2
Download the FireDeX repository and the [FireDeX Virtual Machine](xxx). Then, import the FireDeX.vbox file in VirtualBox and launch the Virtual Machine.

Note:  
username = firedex  
password = firedex

## Running - FireDeX static
Run PyCharm (file _PY_CHARM_HOME/bin/pycharm.sh_) as root (sudo) and open the following projects from the _firedex-static_ directory:
- experimental-framework
- sdn-controller
- firedex-coordinator-service

The default configuration 

Note: run the applications in the following order:
- firedex-coordinator-service
- sdn-controller
- experimental-framework

## Running - FireDeX dynamic
Run PyCharm (file _PY_CHARM_HOME/bin/pycharm.sh_) as root (sudo) and open the following projects from the _firedex-static_ directory:
- experimental-framework
- sdn-controller
- firedex-coordinator-service

## Authors
List of authors.
