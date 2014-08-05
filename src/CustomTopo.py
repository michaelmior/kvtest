from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.cli import CLI
import os
import sys
from mininet.net import Controller

# adds the current dir i.e. src to system path to include sshd
sys.path.append(os.path.dirname(__file__))
from sshd import *
from joinHelpers import config


class ControllerV1(Controller):
    "Custom Controller class to invoke our own forwarding.controller_v1"
    def start(self):
        "Starting controller v1"
        self.pox = '%s/pox/pox.py' % os.environ['HOME']
        if(config['TRAFFIC_SCHEDULING'] == True):
            self.cmd(self.pox, 'controller_v1 --traffic_scheduling=True 1> /mininet/src/out/pox.out 2>&1 &')
        else:
            self.cmd(self.pox, 'controller_v1 1> /mininet/src/out/pox.out 2>&1 &')
    def stop(self):
        "Stopping controller v1"
        self.cmd('kill %' + self.pox)

class DataCenter(Topo):
    "Simple Data Center Topology"

    """
    Creating a data-center tree topology with link customization.
    For example fanout of 2 will generate
                  c1
           a1            a2
      e1      e2     e3      e4
    h1   h2 h3  h4 h5  h6  h7  h8
    where cX aX eX are switches and hX are hosts
    """
    "linkopts - (1:core, 2:aggregation, 3: edge) parameters"
    "fanout - number of child switch per parent switch"
    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)

        coreSwitch = self.addSwitch('c1')
        for i in range(fanout):
            aggregationSwitch = self.addSwitch('a' + str((i+1)))
            self.addLink(coreSwitch, aggregationSwitch, **linkopts1)
            for j in range(fanout):
                edgeSwitch = self.addSwitch('e' + str(i*fanout + (j + 1)))
                self.addLink(edgeSwitch, aggregationSwitch, **linkopts2)
                for k in range(fanout):
                    host = self.addHost('h' + str(fanout** 2 * i +  j*fanout + (k + 1)))
                    self.addLink(edgeSwitch, host, **linkopts3)


class SimpleDC(Topo):
    def __init__(self, linkopts1, linkopts2, fanout=2, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)
        coreSwitch = self.addSwitch('c1')
        for i in range(fanout):
            aggregationSwitch = self.addSwitch('a' + str((i+1)))
            self.addLink(coreSwitch, aggregationSwitch, **linkopts1)
            for k in range(fanout):
                host = self.addHost('h' + str(fanout * i + (k + 1)))
                self.addLink(aggregationSwitch, host, **linkopts2)

class TwoThreeTopo(Topo):
    """
    Test example for:
    http://users.ecs.soton.ac.uk/drn/ofertie/openflow_qos_mininet.pdf
    """
    def __init__(self):
        Topo.__init__(self)
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        self.addLink(s1,s2)
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        h5 = self.addHost('h5')
        self.addLink(s1, h3)
        self.addLink(s1, h4)
        self.addLink(s2, h5)

        # set sshd on each hosts
        sshdOpts = '-D -o UseDNS=no -u0'
        sshd

default_linkopts = dict(bw=50, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
topos = { '2s3h': ( lambda: TwoThreeTopo() ),
          'datacenter': (lambda: DataCenter(default_linkopts, default_linkopts, default_linkopts, 3)) }

def testDataCenter():
    setLogLevel('info')
    linkopts = dict(bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
    netopts = dict(host=CPULimitedHost, link=TCLink)
    topo = DataCenter(linkopts, linkopts, linkopts, 2);
    net = Mininet(topo = topo,host=CPULimitedHost,link=TCLink)
    net.start()
    CLI(net)
    # h1 = net.get('h1')
    # h27 = net.get('h27')
    # outputString = h1.cmd('ping', '-c6', h27.IP())
    # print outputString
    net.stop()


def testSimpleDC():
    setLogLevel('info')
    linkopts = dict()
    netopts = dict()
    topo = SimpleDC(linkopts, linkopts, 2);
    net = Mininet(topo = topo, controller = ControllerV1)
    sshdOpts = '-D -o UseDNS=no -u0'
    sshd(net, switch=net['c1'], opts=sshdOpts)

def testTwoThreeTopo():
    setLogLevel('info')
    sshdOpts = '-D -o UseDNS=no -u0'
    topo = TwoThreeTopo();
    net = Mininet(topo = topo)
    sshd(net, switch=net['s1'], opts=sshdOpts)

if __name__ == '__main__':
    testSimpleDC()
