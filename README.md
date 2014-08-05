# Setup

First install [Vagrant](http://www.vagrantup.com/downloads.html).
To provision and start the VM, run `vagrant up` in the project directory.
To connect to the VM, simply run `vagrant ssh`.
Files for this project will be available in `/mininet`.

This configuration uses a base VM created with [Packer](http://packer.io/).
If necessary, this VM can be rebuilt by installing packer and running `packer build ubuntu64.json` in the `packer/` directory.

# Configuration

To turn on/off the network traffic scheduling, modify the following:

   vim /mininet/src/joinHelpers.py
   set config['TRAFFIC_SCHEDULING'] to True or False

# Running

To run the server and the client code, first you need to start mininet:

    cd /mininet/src
    ./scripts/start_topology.sh

CustomTopo will only run a simple tree topology with 4 hosts.
There are other topology definitions in `CustomTopo.py`.

You can start the server by invoking

    ./scripts/test.sh

Once the server is started and both it finished loading both user and item
data, you can invoke the client using the command below.

    python client.py

To end servers and clients, invoke

    ./scripts/clean.sh
