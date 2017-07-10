# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
#
# on osx...
#  sudo sysctl -w kern.maxfiles=20480
#  sudo sysctl -w kern.maxfilesperproc=18000
#

hosts = ["haproxy", "haproxy-1", "nodejs", "nodejs-1", "nodejs-2", "nodejs-3", "mongodb", "mongodb-1", "eyes", "eyes-1"]
# hosts = ["haproxy", "haproxy-1", "nodejs", "mongodb", "eyes"]
# hosts = ["haproxy", "nodejs", "mongodb", "eyes"]
# hosts = ["nodejs", "mongodb", "eyes"]
memory = 512
cpus = 1
vidmem = 1
cpulimit = 50
box="ubuntu/trusty64"
libvirtBox="iknite/trusty64"

##
#
##
Vagrant.configure("2") do |config|
  config.vm.box = box
  # config.vm.network "private_network", type: "dhcp"

  hosts.each do |i|
    config.vm.define "#{i}" do |node|
      node.vm.host_name = "#{i}"
      node.vm.provider :virtualbox do |vb, override|
          # on osx the bridge is an issue..
          override.vm.network "private_network", type: "dhcp"
          vb.customize ["modifyvm", :id, "--memory", memory]
          vb.customize ["modifyvm", :id, "--cpus", cpus]
          vb.customize ["modifyvm", :id, "--vram", vidmem]
          vb.customize ["modifyvm", :id, "--cpuexecutioncap", cpulimit]
      end
      node.vm.provider :libvirt do |lv, override|
        override.vm.box=libvirtBox
        override.ssh.password = "vagrant"
        lv.cpus = cpus
        lv.memory = memory
        lv.video_vram = vidmem * 1024
      end
    end
  end 
  config.vm.provision "shell", inline: <<-SHELL
    echo $HOSTNAME
    for service in chef-client puppet
    do
        if [ -f "/etc/init.d/$service" ]; then
            service $service stop
            update-rc.d $service disable
        fi
    done
  SHELL
end
