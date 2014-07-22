'''
Creating a data-center tree topology with link customization.
For example fanout of 2 will generate
             c1
       a1            a2
  e1      e2     e3      e4
h1   h2 h3  h4 h5  h6  h7  h8
where cX aX eX are switches and hX are hosts
'''

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.node import CPULimitedHost
from mininet.link import TCLink

class CustomTopo(Topo):
    "Simple Data Center Topology"

    "linkopts - (1:core, 2:aggregation, 3: edge) parameters"
    "fanout - number of child switch per parent switch"
    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)

        # Add your logic here ...
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



topos = { 'custom': ( lambda: CustomTopo() ) }

if __name__ == '__main__':
    setLogLevel('info')
    linkopts = dict(bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
    # linkopts = dict()
    netopts = dict(host=CPULimitedHost, link=TCLink)
    topo = CustomTopo(linkopts, linkopts, linkopts, 3);
    net = Mininet(topo = topo,host=CPULimitedHost,link=TCLink)
    net.start()
    h1 = net.get('h1')
    h27 = net.get('h27')
    outputString = h1.cmd('ping', '-c6', h27.IP())
    print outputString
    net.stop()
