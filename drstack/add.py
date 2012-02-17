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
ADD command
"""

from drstack import base
from drstack import utils


class AddCommand(base.Command):

    def __init__(self, top=None):
        super(AddCommand, self).__init__(cmd='add', top=top)

    def on_role_user(self, args):
        if len(args) < 4:
            print "Not enough args: 3 required"
            return
        try:
            self.top.kc.roles.add_user_role(args[1], args[2], args[3])
            print "Role added to user"
        except:
            print "Role not added to user"
