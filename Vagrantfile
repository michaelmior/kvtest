# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"
Vagrant.require_version ">= 1.5.0"

$script = <<SCRIPT
# Install Mininet
sudo /mininet/mininet/util/install.sh

# Fix broken Open vSwitch
sudo apt-get install -y openvswitch-datapath-source
sudo module-assistant -i auto-install openvswitch-datapath
sudo service openvswitch-switch start

# Configure SSH
cp /mininet/src/_ssh/id_rsa* /home/vagrant/.ssh/
cat /mininet/src/_ssh/id_rsa.pub >> /home/vagrant/.ssh/authorized_keys
echo "StrictHostKeyChecking no" >> /home/vagrant/.ssh/config
chmod og-rwx /home/vagrant/.ssh/*
sudo chown -R vagrant:vagrant /home/vagrant/.ssh/*

# Download data files
wget -c http://mior.ca/up/rubis-csv.tar.gz -O /home/vagrant/rubis-csv.tar.gz
(cd /mininet/src; tar xzf /home/vagrant/rubis-csv.tar.gz)
SCRIPT

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "hashicorp/precise64"

  config.vm.synced_folder ".", "/mininet"
  config.vm.provision "shell", inline: $script
end
