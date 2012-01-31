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
LIST command
"""

from drstack import base
from drstack import utils


class ListCommand(base.Command):

    def __init__(self, top=None):
        super(ListCommand, self).__init__(cmd='list', top=top)

    def on_flavor(self, args):
        utils.print_list(self.top.nc.flavors.list(), ['id', 'name'])

    def on_image(self, args):
        utils.print_list(self.top.nc.images.list(), ['id', 'name'])

    def on_instance(self, args):
        utils.print_list(self.top.nc.servers.list(detailed=False),
                ['id', 'name'])

    def on_keypair(self, args):
        utils.print_list(self.top.nc.keypairs.list(), ['id', 'name'])

    def on_role(self, args):
        utils.print_list(self.top.kc.roles.list(), ['id', 'name'])

    def on_security_group(self, args):
        utils.print_list(self.top.nc.security_groups.list(), ['id', 'name'])

    def on_security_group_rules(self, args):
        utils.print_list(self.top.nc.security_group_rules.list(),
                ['id', 'name'])

    def on_service(self, args):
        utils.print_list(self.top.kc.services.list(), ['id', 'name'])

    def on_tenant(self, args):
        utils.print_list(self.top.kc.tenants.list(limit=999), ['name', 'id'])

    def on_user(self, args):
        utils.print_list(self.top.kc.users.list(limit=999), ['name', 'id'])
