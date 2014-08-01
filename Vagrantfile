# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"
Vagrant.require_version ">= 1.5.0"

$script = <<SCRIPT
# Configure SSH
cp /mininet/src/_ssh/id_rsa* /home/vagrant/.ssh/
cat /mininet/src/_ssh/id_rsa.pub >> /home/vagrant/.ssh/authorized_keys
echo "StrictHostKeyChecking no" >> /home/vagrant/.ssh/config
chmod og-rwx /home/vagrant/.ssh/*
sudo chown -R vagrant:vagrant /home/vagrant/.ssh/*

# Extract data files
(cd /mininet/src; tar xzf /var/tmp/rubis-csv.tar.gz)
SCRIPT

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "mininet-kvtest"
  config.vm.box_url = "http://mior.ca/up/mininet-2.1.0.box"
  config.vm.box_download_checksum_type = "md5"
  config.vm.box_download_checksum = "7f43508a4ae0d80a3ce4db5985670416"

  config.vm.synced_folder ".", "/mininet"
  config.vm.provision "shell", inline: $script
end
