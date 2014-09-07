# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure('2') do |config|
  config.vm.box = 'ubuntu/trusty64'

  config.vm.provider :virtualbox do |vbox|
    vbox.customize ["modifyvm", :id, "--memory", "3072"]
    vbox.cpus = 2
  end

  config.vm.network :private_network, ip: '192.168.9.10'
  config.vm.network :forwarded_port, guest: 80, host: 8080
end
