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
from keystoneclient import exceptions as kc_exceptions

from drstack import base
from drstack import exceptions
from drstack import utils


class ListCommand(base.Command):

    def __init__(self, top=None):
        super(ListCommand, self).__init__(cmd='list', top=top)

    def on_flavor(self, args):
        utils.print_list(self.top.nc.flavors.list(), ['id', 'name'])

    def on_image(self, args):
        self.top.get_glance_client()
        utils.print_dict_list(self.top.gc.get_images(), ['id', 'name'])

    def on_imagen(self, args):
        utils.print_list(self.top.nc.images.list(), ['id', 'name'])

    def on_instance(self, args):
        utils.print_list(self.top.nc.servers.list(detailed=False),
                ['id', 'name'])

    def on_keypair(self, args):
        utils.print_list(self.top.nc.keypairs.list(), ['id', 'name'])

    def on_role(self, args):
        try:
            utils.print_list(self.top.kc.roles.list(), ['id', 'name'])
        except kc_exceptions.NotFound:
            # Most likely this is not authorized
            raise exceptions.NotAuthorized(None, 'list role')

    def on_security_group(self, args):
        utils.print_list(self.top.nc.security_groups.list(), ['id', 'name'])

    def on_security_group_rules(self, args):
        utils.print_list(self.top.nc.security_group_rules.list(),
                ['id', 'name'])

    def on_service(self, args):
        try:
            utils.print_list(self.top.kc.services.list(), ['id', 'name'])
        except kc_exceptions.NotFound:
            # Most likely this is not authorized
            raise exceptions.NotAuthorized(None, 'list service')

    def on_tenant(self, args):
        try:
            utils.print_list(self.top.kc.tenants.list(limit=999), ['name', 'id'])
        except kc_exceptions.NotFound:
            # Most likely this is not authorized
            raise exceptions.NotAuthorized(None, 'list tenant')

    def on_user(self, args):
        try:
            utils.print_list(self.top.kc.users.list(limit=999), ['name', 'id'])
        except kc_exceptions.NotFound:
            # Most likely this is not authorized
            raise exceptions.NotAuthorized(None, 'list user')
