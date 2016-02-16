Vagrant installation for romana openstack
=========================================

We use ansible to bring up devstack and romana inside vagrant VM's,
we also use ansible to render Vagrantfile.

For people who doesn't have ansible there is a pre-rended Vagrantfile provided.

Configuration
-------------
Rename `config.rb.example` into `config.rb` and edit default configuration.

Start
-----

Just type `vagrant up`.
Cold start might fetch some few hundred megapytes of data and could take up to an hour.


Cache
-----
Once you have running setup you can copy over some data so you wouldn't download it evey time
(reduces startup time for me from 1+ hour to 20 minutes)

```
vagrant ssh romana-controller
mkdir -p /home/vagrant/romana/romana-install/deps/stack
sudo cp -af /var/cache/apt/archives /home/vagrant/romana/romana-install/deps
cd /opt/stack
sudo cp -f cinder glance horizon keystone neutron noVNC	nova requirements /home/vagrant/romana/romana-install/deps/stack/
```
