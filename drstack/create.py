# Copyright 2012 Dean Troyer
# Copyright 2011 OpenStack LLC.
# All Rights Reserved
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
CREATE command
"""

import time

from drstack import base
from drstack import utils

class CreateCommand(base.Command):

    def __init__(self, top=None):
        super(CreateCommand, self).__init__(cmd='list', top=top)

    def on_instance(self, args):
        flavor = self.top.default_flavor
        image = self.top.default_image
        name = None
        for a in args:
            if a.startswith("flavor"):
                (x, flavor) = a.split('=')
            elif a.startswith('image'):
                (x, image) = a.split('=')
            elif a.startswith('name'):
                (x, name) = a.split('=')
        flavor = self.top.lookup_flavor(flavor)
        if not flavor:
            print "no flavor specified"
            return
        image = self.top.lookup_image(image)
        if not image:
            print "no image specified"
            return
        if not name:
            name = 'dr'
        self.last_server = self.top.nc.servers.create(image=image,
                                                      flavor=flavor,
                                                      name=name,
                                                      #key_name=key,
                                                      #meta=metadata,
                                                      #userdata=userdata,
                                                      )
        print "server %s started" % self.last_server.id
        status = "BUILD"
        while status == 'BUILD':
            time.sleep(2)
            status = self.top.nc.servers.get(self.last_server.id).status
        print "server %s status: %s" % (self.last_server.id, status)
