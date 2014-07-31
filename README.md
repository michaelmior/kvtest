# Setup

First install [Vagrant](http://www.vagrantup.com/downloads.html).
To provision and start the VM, run `vagrant up` in the project directory.
To connect to the VM, simply run `vagrant ssh`.
Files for this project will be available in `/mininet`.

# Running

To run the server and the client code, first you need to start mininet:

    cd /mininet/src
    sudo python CustomTopo.py

CustomTopo will only run a simple tree topology with 4 hosts.
There are other topology definitions in `CustomTopo.py`.

You can start the server by invoking

    ./scripts/test.sh

Once the server is started, you can invoke the client using the command below.

    python client.py

To end servers, invoke

    ./scripts/clean.sh
