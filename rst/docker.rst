==========================
Using the docker appliance
==========================

Installing Docker
=================

Install docker using the following documentation https://docs.docker.com/engine/installation/


Initial installation
====================

Pull the image :

.. code:: bash

    docker pull bibi21000/janitoo_hostsensor

Create a 'store' container  :

.. code:: bash

    docker create -v /root/.ssh/ -v /opt/janitoo/etc/ --name hostsensor_store bibi21000/janitoo_hostsensor /bin/true

Create a 'running' container :

.. code:: bash

    docker create --volumes-from hostsensor_store -p 8882:22 --name hostsensor_running bibi21000/janitoo_hostsensor

Yous should now have 2 created containers :

.. code:: bash

    docker ps -a

.. code:: bash

    CONTAINER ID        IMAGE                          COMMAND             CREATED             STATUS      PORTS       NAMES
    888a3279e971        bibi21000/janitoo_hostsensor   "/root/auto.sh"     29 seconds ago      Created                 hostsensor_running
    02479e7eeea1        bibi21000/janitoo_hostsensor   "/bin/true"         42 seconds ago      Created                 hostsensor_store


Start the container
===================

Start it :

.. code:: bash

    docker start hostsensor_running

Check that is running :

.. code:: bash

    docker ps

.. code:: bash

    CONTAINER ID        IMAGE                          COMMAND             CREATED              STATUS          PORTS                  NAMES
    cc1a58b59f7c        bibi21000/janitoo_hostsensor   "/root/auto.sh"     About a minute ago   Up 8 seconds    0.0.0.0:8882->22/tcp   hostsensor_running

and stop it :

.. code:: bash

    docker stop hostsensor_running


Update your installation
========================

Delete the 'running' container :

.. code:: bash

    docker rm hostsensor_running

Pull the image release :

.. code:: bash

    docker pull bibi21000/janitoo_hostsensor

And create a new 'running' container :

.. code:: bash

    docker create --volumes-from hostsensor_store -p 8882:22 --name hostsensor_running bibi21000/janitoo_hostsensor


Customize your installation
===========================

You can customize your docker image. This configuration is saved in the 'store' container.

SSH
---

Copy your key to the docker image to bypass the password :

.. code:: bash

    ssh-copy-id root@$127.0.0.1 -p 8882

Disable root login to ssh with password :

.. code:: bash

    sed -i -e "s/^#PermitRootLogin without-password/PermitRootLogin without-password/" /etc/ssh/sshd_config

Configuration
-------------

Update the hostsensor configuration file :

.. code:: bash

    ssh root@$127.0.0.1 -p 8882

Default password is janitoo. You can change it but it will be restored on the next running container update. Prefer the key solutions.

Open the configuration file. The docker image contains a decent release of vim for editing python files.

.. code:: bash

    vim /opt/janitoo/etc/janitoo_hostsensor.conf
