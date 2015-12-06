# -*- coding: utf-8 -*-
"""The hostsensor Janitoo helper

"""

__license__ = """
    This file is part of Janitoo.

    Janitoo is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Janitoo is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Janitoo. If not, see <http://www.gnu.org/licenses/>.

"""
__author__ = 'Sébastien GALLET aka bibi21000'
__email__ = 'bibi21000@gmail.com'
__copyright__ = "Copyright © 2013-2014-2015 Sébastien GALLET aka bibi21000"

import logging
logger = logging.getLogger(__name__)
import os, sys
import threading
import time
from uptime import uptime

from datetime import datetime, timedelta
from janitoo.options import get_option_autostart
from janitoo.utils import HADD, HADD_SEP, json_dumps, json_loads
from janitoo.node import JNTNode
from janitoo.value import JNTValue
from janitoo.component import JNTComponent
from janitoo.thread import JNTBusThread
from janitoo.bus import JNTBus
from janitoo.classes import COMMAND_DESC

##############################################################
#Check that we are in sync with the official command classes
#Must be implemented for non-regression
from janitoo.classes import COMMAND_DESC

COMMAND_DISPLAY = 0x0061
COMMAND_AV_CHANNEL = 0x2100
COMMAND_AV_VOLUME = 0x2101
COMMAND_NOTIFY = 0x3010

assert(COMMAND_DESC[COMMAND_DISPLAY] == 'COMMAND_DISPLAY')
assert(COMMAND_DESC[COMMAND_AV_CHANNEL] == 'COMMAND_AV_CHANNEL')
assert(COMMAND_DESC[COMMAND_AV_VOLUME] == 'COMMAND_AV_VOLUME')
assert(COMMAND_DESC[COMMAND_NOTIFY] == 'COMMAND_NOTIFY')
##############################################################

def make_load(**kwargs):
    return Load(**kwargs)

def make_uptime(**kwargs):
    return Uptime(**kwargs)

def make_thread(options):
    if get_option_autostart(options, 'hostsensor') == True:
        return HostSensorThread(options)
    else:
        return None

class HostSensorThread(JNTBusThread):
    """The HostSensor thread

    """
    def init_bus(self):
        """Build the bus
        """
        self.section = 'hostsensor'
        self.bus = JNTBus(options=self.options, oid=self.section, product_name="Host sensor controller")

class Load(JNTComponent):
    """ Return Load system """

    def __init__(self, bus=None, addr=None, **kwargs):
        JNTComponent.__init__(self, 'hostsensor.load', bus=bus, addr=addr, name="Load statistics",
                product_name="Load statistics", product_type="Software", product_manufacturer="Load statistics", **kwargs)
        logger.debug("[%s] - __init__ node uuid:%s", self.__class__.__name__, self.uuid)

        uuid="load"
        self.values[uuid] = self.value_factory['sensor_float'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            help='The load average',
            label='Load',
            get_data_cb=self.get_load_average,
            genre=0x01,
        )
        config_value = self.values[uuid].create_config_value(help='The load average index (1, 5, and 15m)', label='loadavg', get_data_cb=self.get_config, type=0x02)
        self.values[config_value.uuid] = config_value
        poll_value = self.values[uuid].create_poll_value(default=60)
        self.values[poll_value.uuid] = poll_value

    def get_config(self, node_uuid, index):
        """
        """
        if index == 0:
            if index not in self.values['load'].instances:
                self.values['load'].instances[0] = {}
                self.values['load'].instances[1] = {}
                self.values['load'].instances[2] = {}
            self.values['load'].instances[0]['config'] = '1 minutes'
            self.values['load'].instances[1]['config'] = '5 minutes'
            self.values['load'].instances[2]['config'] = '15 minutes'
        return self.values['load'].instances[index]['config']

    def get_load_average(self, node_uuid, index):
        """
        """
        if index>2:
            return None
        if index == 0:
            avg = list(os.getloadavg())
            for i in [0, 1, 2]:
                self.values['load'].instances[i]['data'] = avg[i]
        return self.values['load'].instances[i]['data']

class Uptime(JNTComponent):
    """ Return Load system """

    def __init__(self, bus=None, addr=None, **kwargs):
        JNTComponent.__init__(self, 'hostsensor.uptime', bus=bus, addr=addr, name="Uptime",
                product_name="Uptime", product_type="Software", product_manufacturer="Uptime", **kwargs)
        logger.debug("[%s] - __init__ node uuid:%s", self.__class__.__name__, self.uuid)

        uuid="uptime"
        self.values[uuid] = self.value_factory['sensor_float'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            help='Uptime in seconds',
            label='Uptime',
            get_data_cb=self.get_uptime,
            genre=0x01,
        )
        poll_value = self.values[uuid].create_poll_value(default=60)
        self.values[poll_value.uuid] = poll_value

    def get_uptime(self, node_uuid, index):
        """
        """
        return uptime()
