==========================
Using the docker appliance
==========================

Installing Docker
=================

Using your favorite method :


Initial clone
=============

Pull the image :

.. code:: bash

    docker pull bibi21000/janitoo_hostsensor

Create a data volume container :

.. code:: bash

    docker create -v /root/.ssh/ -v /opt/janitoo/etc/ --name hostsensor_store bibi21000/janitoo_hostsensor /bin/true

And run it :

.. code:: bash

    docker run -d --volumes-from hostsensor_store -p 8882:22 --name hostsensor_running bibi21000/janitoo_hostsensor

Inspect your running docker image :

.. code:: bash

    docker inspect hostsensor_running
