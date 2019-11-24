# Firedex

FireDeX is a cross-layer middleware that facilitates timely and effective exchange of data for coordinating emergency response activities. Emergency scenarios may challenge/congest the network infrastructure. FireDeX addresses these situations by prioritizing event delivery and by dropping some low priority events. It adopts a publish-subscribe data exchange paradigm with brokers at the network edge to manage prioritized delivery of mission-critical data from IoT sources to relevant subscribers.

See [1, 2] for more details on the FireDeX middleware.

## Getting started
These instructions will get you a copy of the FireDeX project up and running on your local machine. 

## Prerequisites

Install [VirtualBox](https://www.virtualbox.org/).  
Install [Ubuntu 14.04](http://releases.ubuntu.com/14.04/).

## Installing - Option 1 (easy, recommended)
Download the [FireDeX Virtual Machine](https://drive.google.com/open?id=13HCe2FB2J-KxWhJDb8zuDfxpH3_lhk9U). Then, import the FireDeX.ova file in VirtualBox and launch the Virtual Machine.

Note:  
username = firedex  
password = firedex

## Installing - Option 2 (advanced, from source)
These steps will walk you trough the installation of the FireDeX project from scratch (clean Ubuntu Virtual Machine).  

To install:
- Java
- Git
- Mininet
- Modified version of OVS
- PyCharm and Eclipse
- Get the FireDeX source code

### Java
To install Java type the following commands on your terminal.

```
sudo apt-add-repository ppa:webupd8team/java
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
sudo mininet/util/install.sh -nfv
```

### OVS
To install the modified version of OVS take the following steps: 

- remove the OVS version installed with Mininet

```
sudo apt-get remove openvswitch-common openvswitch-datapath-dkms openvswitch-controller openvswitch-pki openvswitch-switch
```

- download the new OVS version

```
sudo wget http://openvswitch.org/releases/openvswitch-2.1.0.tar.gz
sudo tar zxfv openvswitch-2.1.0.tar.gz
cd openvswitch-2.1.0/
```

- make minimal changes to `OVS_HOME/ofproto/ofproto-dpif-xlate.c` as follows [3]:
  - add headers
  ```
  #include <stdlib.h>
  #include <time.h>
  ```
  - add global variable
  ```
  static bool is_srand_initialized = false;
  ```
  - modify functions
  ```
  static void
  xlate_select_group(struct xlate_ctx *ctx, struct group_dpif *group)
  {
      struct flow_wildcards *wc = &ctx->xout->wc;
      const struct ofputil_bucket *bucket;
      uint32_t basis;

      // The following tells the caching code that every packet in
      // the flow in question must go to the userspace "slow path".
      ctx->xout->slow |= SLOW_CONTROLLER;

      basis = hash_bytes(ctx->xin->flow.dl_dst, sizeof ctx->xin->flow.dl_dst, 0);
      bucket = group_best_live_bucket(ctx, group, basis);
      if (bucket) {
          memset(&wc->masks.dl_dst, 0xff, sizeof wc->masks.dl_dst);
          xlate_group_bucket(ctx, bucket);
      }
  }

  static const struct ofputil_bucket *
  group_best_live_bucket(const struct xlate_ctx *ctx,
                     const struct group_dpif *group,
                     uint32_t basis) // basis in not being used
  {
      uint32_t rand_num = 0, sum = 0;
      const struct ofputil_bucket *bucket = NULL;
      const struct list *buckets;

      // initialize random seed once
      if (!is_srand_initialized) {
          srand(time(NULL));
          is_srand_initialized = true;
      }

      // generate a random number in [1, 100]
      rand_num = (rand() % 100) + 1;

      group_dpif_get_buckets(group, &buckets);
      LIST_FOR_EACH (bucket, list_node, buckets) {
          if (bucket_is_alive(ctx, bucket, 0)) {
              sum += bucket->weight;
              if (rand_num <= sum) {
                  return bucket; // return this bucket
              }
          }
      }

      return bucket; // return NULL
  }
  ```
  
- compile the OVS source code

```
sudo apt-get install build-essential fakeroot
sudo apt-get install debhelper autoconf automake libssl-dev pkg-config bzip2 openssl python-all procps python-qt4 python-zopeinterface python-twisted-conch dh-autoreconf
`DEB_BUILD_OPTIONS='parallel=8 nocheck' fakeroot debian/rules binary`
```

- install OVS

```
cd ..
sudo dpkg -i openvswitch-common*.deb openvswitch-pki*.deb openvswitch-switch*.deb
```

### PyCharm and Eclipse
Install [PyCharm](https://www.jetbrains.com/pycharm/) and [Eclipse](https://www.eclipse.org/).

### Get the FireDeX source code
Download the FireDeX repository.

```
git clone git://github.com/boulouk/firedex
```

### Finishing up
Finally you need to import the project dependencies (make sure that you are using Python 2.7).

#### FireDeX static dependencies
Run PyCharm (file _PY_CHARM_HOME/bin/pycharm.sh_) as root (sudo) and open the following projects in the _firedex-static_ directory:
- experimental-framework
- sdn-controller
- firedex-coordinator-service

Import the following dependencies:
- experimental-framework -> numpy, requests, matplotlib, pandas (add the Mininet project as a dependency)
- sdn-controller -> ryu, decorator (mark the _application_ directory as _Sources Root_, add the NetworkX project as a dependency)
- firedex-coordinator-service -> flask, numpy, requests

#### FireDeX dynamic dependencies

Run PyCharm (file _PY_CHARM_HOME/bin/pycharm.sh_) as root (sudo) and open the following projects in the _firedex-dynamic_ directory:
- experimental-framework
- sdn-controller
- firedex-coordinator-service

Import the following dependencies:
- experimental-framework -> numpy, requests (add the Mininet project as a dependency)
- sdn-controller -> ryu, decorator (mark the _application_ directory as _Sources Root_, add the NetworkX project as a dependency)
- firedex-coordinator-service -> flask, numpy, cvxpy, requests

## Running - FireDeX static
Run PyCharm (file _PY_CHARM_HOME/bin/pycharm.sh_) as root (sudo) and open the following projects in the _firedex-static_ directory:
- experimental-framework
- sdn-controller
- firedex-coordinator-service

The configuration parameters are in the _scenario_ directory of the experimental-framework project:
- experiment_scenario.py
  - _RUN_ defines the type of experiment to run (analytical model, Mininet simulation, both)
- firedex_scenario.py
  - _EXPERIMENT_DURATION_ sets the duration of the experiment
  - _NETWORK_FLOWS_ and _PRIORITIES_ allow to set respectively the number of network flows and the number of priorities
  - _NETWORK_FLOW_ALGORITHM_, _PRIORITY_ALGORITHM_ and _DROP_RATE_ALGORITHM_ apply the various FireDeX algorithms
  - _TOLERANCE_ represents the percentage of bandwidth reserved for temporary traffic peaks
- network_scenario.py
  - _BANDWIDTH_ defines the available bandwidth between broker and subscribers
- topology_scenario.py
  - _SUBSCRIBER_ allows to modify the number of subscribers and their subscriptions (topic and utility function)
  - _PUBLISHER_ allows to modify the number of publishers and their publications (topic, publication rate and message size)

Note: run the applications in the following order:
- firedex-coordinator-service (file to run: firedex_middleware.py)
- sdn-controller (file to run: sdn_controller.py)
- experimental-framework (file to run: experimental_framework.py - to plot the results: analysis_framework.py)

The default configuration runs 10 subscribers with ρ = 1.5 (network load).  

The following images show the performance of the system (response time and success rate) of the default configuration.

![Response time](https://github.com/boulouk/firedex/blob/master/documentation/static-response-time.png)

![Success rate](https://github.com/boulouk/firedex/blob/master/documentation/static-success-rate.png)

## Running - FireDeX dynamic
Run PyCharm (file _PY_CHARM_HOME/bin/pycharm.sh_) as root (sudo) and open the following projects in the _firedex-dynamic_ directory:
- experimental-framework
- sdn-controller
- firedex-coordinator-service

The configuration parameters are in the _scenario_ directory of the experimental-framework project:
- experiment_scenario.py
  - _EXPERIMENT_DURATION_ sets the duration of the experiment
  - _SUBSCRIBER_ allows to modify the number of subscribers and their subscriptions (topic and utility function)
  - _PUBLISHER_ allows to modify the number of publishers and their publications (topic, publication rate and message size)
- firedex_scenario.py
  - _NETWORK_FLOWS_ and _PRIORITIES_ allow to set respectively the number of network flows and the number of priorities
  - _NETWORK_FLOW_ALGORITHM_, _PRIORITY_ALGORITHM_ and _DROP_RATE_ALGORITHM_ apply the various FireDeX algorithms
  - _RHO_TOLERANCE_ represents the percentage of bandwidth reserved for temporary traffic peaks
- network_scenario.py
  - _BANDWIDTH_ defines the available bandwidth between broker and subscribers  

Note: run the applications in the following order:
- firedex-coordinator-service (file to run: firedex_middleware.py)
- sdn-controller (file to run: sdn_controller.py)
- experimental-framework (file to run: experimental_framework.py - to plot the results use the dashboard)

The default configuration runs 5 subscribers with ρ = 1.2 (network load).  

The following images show the performance experienced by subscriptions with different importance (high importance/priority vs. low importance/priority).

![Subscriptions with different priorities](https://github.com/boulouk/firedex/blob/master/documentation/dashboard.png)

## References

[1] https://hal.inria.fr/hal-01877555  
[2] https://hal.inria.fr/hal-01895274  
[3] https://github.com/saeenali/openvswitch/wiki/Stochastic-Switching-using-Open-vSwitch-in-Mininet
