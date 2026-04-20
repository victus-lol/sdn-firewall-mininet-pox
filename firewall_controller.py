from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.packet import ethernet, ipv4

log = core.getLogger()

class FirewallSwitch(object):

    def __init__(self, connection):
        self.connection = connection
        self.mac_to_port = {}
        connection.addListeners(self)
        log.info("Switch %s connected", connection)

    def _handle_PacketIn(self, event):
        packet = event.parsed
        in_port = event.port

        # Learn MAC → port
        self.mac_to_port[packet.src] = in_port

        ip_packet = packet.find('ipv4')

        #  FIREWALL: block h1 → h3
        if ip_packet:
            src_ip = str(ip_packet.srcip)
            dst_ip = str(ip_packet.dstip)

            if src_ip == "10.0.0.1" and dst_ip == "10.0.0.3":
                log.info("BLOCKING TRAFFIC: %s -> %s", src_ip, dst_ip)

                # Install DROP rule
                msg = of.ofp_flow_mod()
                msg.match = of.ofp_match.from_packet(packet, in_port)
                msg.priority = 65535
                self.connection.send(msg)

                # Drop current packet cleanly
                packet_out = of.ofp_packet_out()
                packet_out.data = event.ofp
                packet_out.in_port = in_port
                self.connection.send(packet_out)

                return   #  stop further processing

        #  NORMAL LEARNING SWITCH (OUTSIDE firewall block!)
        if packet.dst in self.mac_to_port:
            out_port = self.mac_to_port[packet.dst]
        else:
            out_port = of.OFPP_FLOOD

        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet, in_port)
        msg.actions.append(of.ofp_action_output(port=out_port))
        msg.priority = 1
        self.connection.send(msg)

        # Send packet immediately
        packet_out = of.ofp_packet_out()
        packet_out.data = event.ofp
        packet_out.actions.append(of.ofp_action_output(port=out_port))
        self.connection.send(packet_out)


def launch():
    def start_switch(event):
        log.info("Controlling %s", event.connection)
        FirewallSwitch(event.connection)

    core.openflow.addListenerByName("ConnectionUp", start_switch)
