==========================
Using the docker appliance
==========================

.. jnt-badge::
    :badges: docker


Installing Docker
=================

Install docker using the following documentation https://docs.docker.com/engine/installation/


Initial installation
====================

Create a 'store' container  :

.. code:: bash

    $ make docker-local-store

Create a 'running' container :

.. code:: bash

    $ make docker-local-running

Yous should now have 2 created containers :

.. code:: bash

    $ docker ps -a

.. code:: bash

    CONTAINER ID        IMAGE                          COMMAND             CREATED             STATUS      PORTS       NAMES
    888a3279e971        bibi21000/janitoo_hostsensor   "/root/auto.sh"     29 seconds ago      Created                 hostsensor_running
    02479e7eeea1        bibi21000/janitoo_hostsensor   "/bin/true"         42 seconds ago      Created                 hostsensor_store


Start the container
===================

Start it :

.. code:: bash

    $ docker start hostsensor_running

Check that is running :

.. code:: bash

    $ docker ps

.. code:: bash

    CONTAINER ID        IMAGE                          COMMAND             CREATED              STATUS          PORTS                  NAMES
    cc1a58b59f7c        bibi21000/janitoo_hostsensor   "/root/auto.sh"     About a minute ago   Up 8 seconds    0.0.0.0:8884->22/tcp   hostsensor_running

And stop it :

.. code:: bash

    $ docker stop hostsensor_running


Customize your installation
===========================

You can find basis customizations tips here : https://bibi21000.github.io/janitoo_docker_appliance/customize.html.

This configuration is saved in the 'store' container.

Configuration
-------------

Update the hostsensor configuration file :

.. code:: bash

    $ ssh root@127.0.0.1 -p 8884

Default password is janitoo. You can change it but it will be restored on the next running container update. Prefer the key solutions.

Open the configuration file. The docker image contains a nano or vim for editing files :

.. code:: bash

    root@8eafc45f6d09:~# vim /opt/janitoo/etc/janitoo_hostsensor.conf

You must at least update the broker ip. It should match the ip address of your shared "mosquitto" :

.. code:: bash

    broker_ip = 192.168.1.14

If you plan to install more than one janitoo_hostsensor image on your network, you must change the hadd of the bus and components :

.. code:: bash

    hadd = 0121/0000

to

.. code:: bash

    hadd = 0122/0000

And so on for 0121/0001, 0121/0002, ... Keep in mind that hadd must be unique on your network.

Save your updates and restart jnt_hostsensor :

.. code:: bash

    root@8eafc45f6d09:~# killall jnt_hostsensor

Disks
-----

The configuration is autogenerated on first startup (if empty). You can clean it but don't remove erverything ou remove the component from bus configuration.

.. code:: bash

    [hostsensor__disks]
    heartbeat = 60
    name = Disks
    location = Docker
    hadd = 0121/0002
    partition_config_0 = /root/.ssh
    total_config_0 = /root/.ssh
    used_config_0 = /root/.ssh
    free_config_0 = /root/.ssh
    percent_use_config_0 = /root/.ssh

Sensors
-------

Connect via ssh to the docker appliance and run the following command :

.. code:: bash

    root@11ec5283ffbd:~# sensors

It will detect the sensors :

.. code:: bash

    acpitz-virtual-0
    Adapter: Virtual device
    temp1:        +48.0 C  (crit = +105.0 C)

    fam15h_power-pci-00c4
    Adapter: PCI adapter
    power1:        0.00 W  (crit =  24.99 W)

    k10temp-pci-00c3
    Adapter: PCI adapter
    temp1:        +47.8 C  (high = +70.0 C)
                           (crit = +100.0 C, hyst = +99.0 C)

There is 2 temperature with the same name, update your sensor configuration http://www.lm-sensors.org/ if you want to monitor both.

Open the configuration file using your favorite editor :

.. code:: bash

    root@8eafc45f6d09:~# vim /opt/janitoo/etc/janitoo_hostsensor.conf

Add a component to the bus configuration :

.. code:: bash

    [hostsensor]
    ...
    components.lmsensor = hostsensor.lmsensor

Add a configuration for the component :

.. code:: bash

    [hostsensor__lmsensor]
    heartbeat = 20
    name = lm-sensors
    location = Docker
    hadd = 0121/0004
    temperature_config_0 = temp1

temperature_config_0 should be the name 'detected' in the steps below : temp1

Save and restart your server to apply.

Performances
============

The top result in the running appliance :

.. code:: bash

    root@7de7e4993b13:~# top

.. code:: bash

    top - 19:08:40 up 10 days, 46 min,  1 user,  load average: 0.34, 0.50, 0.58
    Tasks:   8 total,   1 running,   7 sleeping,   0 stopped,   0 zombie
    %Cpu(s):  7.3 us,  3.9 sy,  0.0 ni, 88.5 id,  0.0 wa,  0.0 hi,  0.3 si,  0.0 st
    KiB Mem:  11661364 total, 11257872 used,   403492 free,   586084 buffers
    KiB Swap: 19530748 total,   301772 used, 19228976 free.  4392228 cached Mem

      PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND
       42 root      20   0  489236  23464   4480 S   3.0  0.2   1:01.15 /usr/local/bin/python /usr/local/bin/jnt_hostsensor -c /etc/janitoo/janitoo_hostsensor+
       55 root      20   0   21940   1424   1048 R   0.3  0.0   0:00.25 top
        1 root      20   0   21740   1600   1328 S   0.0  0.0   0:00.04 /bin/bash /root/auto.sh
       10 root      20   0   55508  10176   1412 S   0.0  0.1   0:00.25 /usr/bin/python /usr/bin/supervisord -c /etc/supervisor/supervisord.conf
       11 root      39  19   23500   1492   1200 S   0.0  0.0   0:00.45 top -b
       13 root      20   0   55176   3112   2444 S   0.0  0.0   0:00.02 /usr/sbin/sshd -D
       32 root      20   0   82716   3936   3076 S   0.0  0.0   0:00.15 sshd: root@pts/0
       34 root      20   0   20244   2056   1568 S   0.0  0.0   0:00.03 -bash

Administer your containers
==========================

You can find basis administration tips here : https://bibi21000.github.io/janitoo_docker_appliance/administer.html.
