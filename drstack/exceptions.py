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
DrStack exceptions
"""


class CommandException(Exception):
    """
    The base exception for commands
    """
    def __init__(self, message=None, command=None):
        self.message = message or self.__class__.message
        self.command = command

    def __str__(self):
        if self.command:
            retstr = "%s: %s" % (self.message, self.command)
        else:
            retstr = "%s" % (self.message)
        return retstr

class NotAuthorized(CommandException):
    """
    Command requires more authorization than is available
    """
    message = "Not authorized to execute"
