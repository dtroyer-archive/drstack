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
#
# vim: tabstop=4 shiftwidth=4 softtabstop=4

"""
DELETE command
"""

from drstack import base
from drstack import utils


class DeleteCommand(base.Command):

    def __init__(self, top=None):
        super(DeleteCommand, self).__init__(cmd='list', top=top)

    def on_image(self, args):
        self.top.get_glance_client()
        if len(args) < 2:
            print "image id missing"
            return
        self.top.gc.delete_image(args[1])

    def on_instance(self, args):
        self.top._get_nova()
        if len(args) < 2:
            print "instance id missing"
            return
        self.top.nc.servers.delete(args[1])
