What is it?
===========
A Simple web app deployed with ansible, The app consists of two haproxies,
nodejs mongodb and a simple client that does random queries on the rest-api
and generates _some_ load (tunable _eyes\_interval_).
The used web app is a slightly modified version of the openshift demo app
[restify-mongodb-parks|https://github.com/snuf/restify-mongodb-parks]
There is also a vagrant file for virtualbox and libvirt that allows easy
testing and rollout of multiple machines if required.
There are several configuration options availabie. These depend on the hostnames used, and will by default revert to a setup based on the amount of [haproxy] nodes.
![sorry no ascii art here](https://docs.google.com/drawings/d/1TXs5D3RMw-MsE8qdvoliXRLU12ViAYPbifUoPm-Q5-M/pub?w=950&amp;h=637)

### TODOs
1.  Real status page instead of dirty 503.
2.  Make MongoDB a real cluster instead of dumb usable nodes.
3.  Add the layer 7 checks to haproxy.

## Setup (not vagrant)

When not using vagrant (_revamp_) there are a couple manual steps
required. In the _hosts_ file that is used with _ansible_ :

0. Go to the ansible directory

   _cd /ansible_  

1. Make sure the correct user is used and this user has sudo rights:

   ansible\_ssh\_user=vagrant
2. If the user above has **no** ssh key distributed or if a single private ssh key or password can be used for all hosts:

   ansible\_ssh\_pass=vagrant  
   _or_  
   ansible\_ssh\_private\_key\_file=~/.ssh/id_bootstrap  

3. Edit the proxies to point at the correct ones or comment the lines out:

   proxy\_http: "http://172.28.128.1:3128"  
   proxy\_https: "http://172.28.128.1:3128"  

   Set the interval to a desired float, or 0 for non wait.  
   eyes\_interval: 0.  

4. Enter the correct IPs/hosts under the groups and the desired options:

   [haproxy]  
   1st Loadbalancer sits front of nodejs entities.  
   2nd Loadbalancer sits in front of mongodb.  
   Minimum 0, advised 2.  

   [mongodb]  
   Backend servers that contain the data.  
   Minimum 1, advised multiuple.  

   [nodejs]  
   Frontend servers that serve the site and api.  
   Minimum 1, advised multiple.  

   [eyes]  
   Host that runs a script that gets parks from random longtitude and lattitude in the us degrees.  
   Minimum 0, advised 1 can be multiple.  

You can add multiple hosts/ips for each group, but for [haproxy] we only
use one host/ip per group type of [nodejs] and [mongodb]. If a single
[haproxy] host/ip is added both [nodejs] and [mongodb] will live behind
the single [haproxy]. if no [haproxy] is used a single a [nodejs] is
directly wired to a single [mongodb].

## Ansible setup on older ubuntu.

Make sure you have a "recent" ansible version on the ubuntu host that runs the playbook (minimal 2.2.2.0) If no proxies are required, leave out the proxies.

    sudo bash  
    export http_proxy=http://172.28.128.1:3128  
    export https_proxy=http://172.28.128.1:3128  
    apt-get update  
    apt-get install -y software-properties-common  
    apt-add-repository -y ppa:ansible/ansible  
    apt-get update  
    apt-get install -y ansible  

## Running the playbook

The ansible playbook can be checked, will have one failure at the end...:  

    ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook --check -i hosts playbook.yaml  

After successfully runnig the dry-runm the script can be run:  

    ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i hosts playbook.yaml  

## Setup with vagrant

For now the Vagrantfile assumes virtualbox or libvirt. The alterations named
in setup above are to be done in the _hosts.header_ file, except for the
addition of the hosts/ips themselves, which are generated from _vagrant status_.
Changing the amount of nodes is done in the Vagrantfile, by altiering the
_hosts_ list. Names are respectively _haproxy, mongodb, nodejs, eyes_ to
create multiple hosts a number is added with a dash _-_.
e.g. haproxy, haproxy-1 ... etc etc etc etc  ...

deploy everything: _./revamp full_  
(re)-deploy vms: _./revamp refresh_  
update hosts file: _./revamp hosts_  
run ansible: _./revamp ansible_  
