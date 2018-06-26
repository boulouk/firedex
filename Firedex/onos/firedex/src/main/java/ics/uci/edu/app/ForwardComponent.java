/*
 * Copyright 2015 Open Networking Foundation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package ics.uci.edu.app;

import java.util.HashMap;
import java.util.Map;
import java.util.Set;

import org.apache.felix.scr.annotations.Activate;
import org.apache.felix.scr.annotations.Component;
import org.apache.felix.scr.annotations.Deactivate;
import org.apache.felix.scr.annotations.Reference;
import org.apache.felix.scr.annotations.ReferenceCardinality;
import org.onlab.packet.Ethernet;
import org.onlab.packet.ICMP;
import org.onlab.packet.IPv4;
import org.onlab.packet.Ip4Prefix;
import org.onlab.packet.TCP;
import org.onlab.packet.TpPort;
import org.onlab.packet.UDP;
import org.onosproject.core.ApplicationId;
import org.onosproject.core.CoreService;
import org.onosproject.net.DeviceId;
import org.onosproject.net.Host;
import org.onosproject.net.HostId;
import org.onosproject.net.Path;
import org.onosproject.net.PortNumber;
import org.onosproject.net.flow.DefaultTrafficSelector;
import org.onosproject.net.flow.DefaultTrafficTreatment;
import org.onosproject.net.flow.FlowRuleService;
import org.onosproject.net.flow.TrafficSelector;
import org.onosproject.net.flow.TrafficTreatment;
import org.onosproject.net.flow.TrafficTreatment.Builder;
import org.onosproject.net.flowobjective.DefaultForwardingObjective;
import org.onosproject.net.flowobjective.FlowObjectiveService;
import org.onosproject.net.flowobjective.ForwardingObjective;
import org.onosproject.net.host.HostService;
import org.onosproject.net.packet.PacketContext;
import org.onosproject.net.packet.PacketPriority;
import org.onosproject.net.packet.PacketProcessor;
import org.onosproject.net.packet.PacketService;
import org.onosproject.net.topology.PathService;
import org.onosproject.net.topology.Topology;
import org.onosproject.net.topology.TopologyService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Component(immediate = true)
public class ForwardComponent {

	private static Logger log = LoggerFactory.getLogger(ForwardComponent.class);

	private static final int PRIORITY = 128;
	private static final int QOS_PRIORITY = 65535;
	private static final int TIMEOUT = 60;

	@Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
	protected CoreService coreService;

	@Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
	protected FlowObjectiveService flowObjectiveService;

	@Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
	protected FlowRuleService flowRuleService;

	@Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
	protected PacketService packetService;

	@Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
	protected HostService hostService;

	@Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
	protected TopologyService topologyService;

	@Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
	protected PathService pathService;

	private ApplicationId applicationId;
	private final PacketProcessor packetProcessor = new FiredexPacketProcessor();
	private final TrafficSelector intercept = DefaultTrafficSelector.builder().build();
	
	private Map<Integer, Integer> qosMapping;

	@Activate
	public void activate() {
		applicationId = coreService.registerApplication("ics.uci.edu.app");
		packetService.addProcessor(packetProcessor, PRIORITY);
		packetService.requestPackets(intercept, PacketPriority.CONTROL, applicationId);
		
		qosMapping = new HashMap<>();
		qosMapping.put(10000, 0);
		qosMapping.put(10001, 1);
		qosMapping.put(10002, 2);
		qosMapping.put(10003, 3);
		
		log.info("Started");
	}

	@Deactivate
	public void deactivate() {
		packetService.removeProcessor(packetProcessor);
		flowRuleService.removeFlowRulesById(applicationId);
		log.info("Stopped");
	}
	
	private void flood(PacketContext packetContext) {
		Topology topology = topologyService.currentTopology();
		if ( topologyService.isBroadcastPoint(topology, packetContext.inPacket().receivedFrom()) )
			packetOut(packetContext, PortNumber.FLOOD);
		else
			packetContext.block();
    }

	private void installRule(PacketContext packetContext, PortNumber port) {
		Ethernet ethernet = packetContext.inPacket().parsed();
		TrafficSelector.Builder trafficSelectorBuilder = DefaultTrafficSelector.builder();

		// ARP packets.
		if (ethernet.getEtherType() == Ethernet.TYPE_ARP) {
			packetOut(packetContext, port);
			return;
		}

		// Ethernet packets.
		trafficSelectorBuilder
			.matchInPort( packetContext.inPacket().receivedFrom().port() )
			.matchEthSrc( ethernet.getSourceMAC() )
			.matchEthDst( ethernet.getDestinationMAC() );

		boolean qos = false;
		
		// If IPv4 packet than match IPv4 and TCP/UDP/ICMP fields.
		if (ethernet.getEtherType() == Ethernet.TYPE_IPV4) {
			IPv4 ipv4 = (IPv4) ethernet.getPayload();
			byte ipv4Protocol = ipv4.getProtocol();
			
			Ip4Prefix sourceAddress = Ip4Prefix.valueOf(ipv4.getSourceAddress(), 32);
			Ip4Prefix destinationAddress = Ip4Prefix.valueOf(ipv4.getDestinationAddress(), 32);
			trafficSelectorBuilder
				.matchEthType(Ethernet.TYPE_IPV4)
				.matchIPSrc(sourceAddress)
				.matchIPDst(destinationAddress);

			if (ipv4Protocol == IPv4.PROTOCOL_TCP) {
				TCP tcp = (TCP) ipv4.getPayload();
				trafficSelectorBuilder
					.matchIPProtocol(ipv4Protocol)
					.matchTcpSrc( TpPort.tpPort(tcp.getSourcePort()) )
					.matchTcpDst( TpPort.tpPort(tcp.getDestinationPort()) );
				
				Set<Integer> qosPorts = qosMapping.keySet();
				if ( qosPorts.contains(tcp.getDestinationPort()) )
					qos = true;
			}
			if (ipv4Protocol == IPv4.PROTOCOL_UDP) {
				UDP udp = (UDP) ipv4.getPayload();
				trafficSelectorBuilder
					.matchIPProtocol(ipv4Protocol)
					.matchUdpSrc( TpPort.tpPort(udp.getSourcePort()) )
					.matchUdpDst( TpPort.tpPort(udp.getDestinationPort()) );
				
				Set<Integer> qosPorts = qosMapping.keySet();
				if ( qosPorts.contains(udp.getDestinationPort()) )
					qos = true;
			}
			if (ipv4Protocol == IPv4.PROTOCOL_ICMP) {
				ICMP icmp = (ICMP) ipv4.getPayload();
				trafficSelectorBuilder
					.matchIPProtocol(ipv4Protocol)
					.matchIcmpType(icmp.getIcmpType())
					.matchIcmpCode(icmp.getIcmpCode());
			}
		}
		
		TrafficSelector trafficSelector = trafficSelectorBuilder.build();
		
		Builder trafficTreatmentBuilder = DefaultTrafficTreatment.builder();
		if ( qos == true ) {
			// If UDP or TCP, QoS is enabled -> just forward to the correspondent queue.
			IPv4 ipv4 = (IPv4) ethernet.getPayload();
			byte ipv4Protocol = ipv4.getProtocol();
			int portToMap = -1;
			if (ipv4Protocol == IPv4.PROTOCOL_TCP) {
				TCP tcp = (TCP) ipv4.getPayload();
				int tcpPort = tcp.getDestinationPort();
				portToMap = tcpPort;
			}
			if (ipv4Protocol == IPv4.PROTOCOL_UDP) {
				UDP udp = (UDP) ipv4.getPayload();
				int udpPort = udp.getDestinationPort();
				portToMap = udpPort;
			}
			int queue = qosMapping.get(portToMap);
			trafficTreatmentBuilder.setQueue(queue, port);
		} else if ( qos == false )
			// Otherwise, forward to the correspondent output port.
			trafficTreatmentBuilder.setOutput(port);
		
		TrafficTreatment trafficTreatment = trafficTreatmentBuilder.build();

		ForwardingObjective forwardingObjective = DefaultForwardingObjective.builder()
			.withSelector(trafficSelector)
			.withTreatment(trafficTreatment)
			.withPriority(QOS_PRIORITY)
			.withFlag(ForwardingObjective.Flag.VERSATILE)
			.fromApp(applicationId)
			.makeTemporary(TIMEOUT)
			.add();

		DeviceId device = packetContext.inPacket().receivedFrom().deviceId();
		
		flowObjectiveService.forward(device, forwardingObjective);

		log.info("New rule: " + forwardingObjective);
		
        packetOut(packetContext, port);
	}

	private void packetOut(PacketContext packetContext, PortNumber port) {
		packetContext.treatmentBuilder().setOutput(port);
		packetContext.send();
	}

	private class FiredexPacketProcessor implements PacketProcessor {
		@Override
		public void process(PacketContext packetContext) {
			// Drop already handled packets.
			if (packetContext.isHandled())
				return;

			Ethernet ethernet = packetContext.inPacket().parsed();
			if ( ethernet == null )
				return;
			
			HostId toHostIdentifier = HostId.hostId( ethernet.getDestinationMAC() );

			if ( ethernet.getEtherType() == Ethernet.TYPE_LLDP || ethernet.getEtherType() == Ethernet.TYPE_BSN )
				return;
			
			// Drop lldp packets.
			if (toHostIdentifier.mac().isLldp())
				return;

			// Drop multicast packets.
			if (ethernet.getEtherType() == Ethernet.TYPE_IPV4) {
				if (toHostIdentifier.mac().isMulticast())
					return;
			}
			
			Host toHost = hostService.getHost(toHostIdentifier);
			// Do we know who this is for? If not, flood.
			if (toHost == null) {
				flood(packetContext);
				return;
			}

			// Are we on an edge switch that our destination is on? If so,
			// simply forward out to the destination.
			DeviceId inDeviceIdentifier = packetContext.inPacket().receivedFrom().deviceId();
			if (inDeviceIdentifier.equals(toHost.location().deviceId())) {
				PortNumber inPort = packetContext.inPacket().receivedFrom().port();
				if (!inPort.equals(toHost.location().port()))
					installRule(packetContext, toHost.location().port());
				return;
			}

			// Otherwise, get a set of paths that lead from here to the
			// destination edge switch.
			Topology topology = topologyService.currentTopology();
			DeviceId toIdentifier = toHost.location().deviceId();
			Set<Path> paths = topologyService.getPaths(topology, inDeviceIdentifier, toIdentifier);

			// If there are not paths, drop
			if (paths.isEmpty()) {
				flood(packetContext);
				return;
			}

			// Otherwise, pick a path that does not lead back to where we
			// came from; if no such path, drop.
			Path path = pickForwardOrNull(paths, packetContext.inPacket().receivedFrom().port());
			if (path == null) {
				flood(packetContext);
				return;
			}
			
			// Otherwise, forward.
			installRule(packetContext, path.src().port());
		}

		private Path pickForwardOrNull(Set<Path> paths, PortNumber notToPort) {
			for (Path path : paths)
				if (!path.src().port().equals(notToPort))
					return (path);
			return (null);
		}
	}

}
