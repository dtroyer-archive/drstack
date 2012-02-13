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
Command-line interface to the OpenStack Identity, Compute and Storage APIs
"""

import argparse
import logging
import os
import rlcompleter
import readline
import sys
import urlparse

from cmd2 import Cmd, make_option, options
import httplib2

from glance import client as glance_client
#from keystoneclient.v2_0 import client as keystone_client
from novaclient.v1_1 import client as nova_client
from novaclient import exceptions
from novaclient import utils

import drstack.compat.keystone as keystone_client

import drstack.create as create_cmd
import drstack.delete as delete_cmd
import drstack.list as list_cmd
import drstack.show as show_cmd


# Handle broken modules (keystoneclient I'm looking at you!)
logging.basicConfig()


def can_haz_slash(str):
    """ ensure str ends with a '/' """
    if str[-1:] != '/':
        str += '/'
    return str


def can_haznt_slash(str):
    """ ensure str doesn't end with a '/' """
    str = str.rstrip('/')
    return str


class DrStack(Cmd, object):
    """Naive command loop for the Good Doctor(tm)"""

    # Set our default prompt
    prompt = "dr> "

    # Allow some args to be set from the command loop
    settable = Cmd.settable + \
            """allow_shell allow shell access for unknown commands
               default_flavor default flavor for 'create image'
               default_image default image for 'create image'
               auth_url authentiation URL
               password OS_PASSWORD
               tenant_name OS_TENANT_NAME
               username OS_USERNAME"""

    # Override default cmd2 behaviours:
    # Remove the following default commands from the list:
    del Cmd.do_shortcuts

    gc = None
    kc = None
    nc = None

    allow_shell = True
    default_flavor = None
    default_image = None
    auth_token = None
    auth_url = None
    password = None
    tenant_name = None
    username = None

    create_commands = ()
    create_instance = None
    create_subjects = None

    delete_commands = ()
    delete_instance = None
    delete_subjects = None

    list_commands = ()
    list_instance = None
    list_subjects = None

    show_commands = ()
    show_instance = None
    show_subjects = None

    def default(self, line):
        """Attempt to execute unknown commands in a shell"""
        if self.allow_shell:
            self.do_shell(line)
        else:
            raise exceptions.CommandError(line)

    def do_EOF(self, line):
        return True

    def emptyline(self):
        pass

    def onecmd(self, line):
        ret = super(DrStack, self).onecmd(line)
        return ret

    def preloop(self):
        print "Welcome to DrStack"
        super(DrStack, self).preloop()

    def postloop(self):
        print

    #@options([make_option('--flavor', help='instance type'),
    #          make_option('--image', help='image to boot')
    #         ])

    def complete_create(self, text, line, bx, ex):
        if not self.create_subjects:
            (self.create_instance,
             self.create_subjects,
             self.create_commands) = \
                self.find_subjects(create_cmd)
        if not text:
            comp = self.create_commands[:]
        else:
            comp = [c for c in self.create_commands if c.startswith(text)]
        return comp

    def do_create(self, line, opts=None):
        """create <subject>
        Create various subject types"""
        # Find all CREATE subjects
        if not self.create_subjects:
            (self.create_instance,
             self.create_subjects,
             self.create_commands) = \
                self.find_subjects(create_cmd)
        args = line.split()
        self.create_subjects[args[0]](args)

    def complete_delete(self, text, line, bx, ex):
        if not self.delete_subjects:
            (self.delete_instance,
             self.delete_subjects,
             self.delete_commands) = \
                    self.find_subjects(delete_cmd)
        if not text:
            comp = self.delete_commands[:]
        else:
            comp = [c for c in self.delete_commands if c.startswith(text)]
        return comp

    def do_delete(self, line):
        """delete instance|image|user|tenant
        Delete various object types"""
        # Find all DELETE subjects
        if not self.delete_subjects:
            (self.delete_instance,
             self.delete_subjects,
             self.delete_commands) = \
                    self.find_subjects(delete_cmd)
        args = line.split()
        self.delete_subjects[args[0]](args)

    def complete_list(self, text, line, bx, ex):
        if not self.list_commands:
            (self.list_instance, self.list_subjects, self.list_commands) = \
                    self.find_subjects(list_cmd)
        if not text:
            comp = self.list_commands[:]
        else:
            comp = [c for c in self.list_commands if c.startswith(text)]
        return comp

    def do_list(self, line):
        """list <subject>
        List various subject types"""
        # Find all LIST subjects
        if not self.list_subjects:
            (self.list_instance, self.list_subjects, self.list_commands) = \
                    self.find_subjects(list_cmd)
        args = line.split()
        self.list_subjects[args[0]](args)

    def complete_show(self, text, line, bx, ex):
        if not self.show_subjects:
            (self.show_instance,
             self.show_subjects,
             self.show_commands) = \
                    self.find_subjects(show_cmd)
        if not text:
            comp = self.show_commands[:]
        else:
            comp = [c for c in self.show_commands if c.startswith(text)]
        return comp

    def do_show(self, line):
        """show <subject>
        Show details on various subject types"""
        if not line:
            # hacky-hack to display settable values
            # called from cmd2's do_set() with no args
            Cmd.do_show(self, line)
        else:
            # Find all SHOW subjects
            if not self.show_subjects:
                (self.show_instance,
                 self.show_subjects,
                 self.show_commands) = \
                        self.find_subjects(show_cmd)
            args = line.split()
            self.show_subjects[args[0]](args)

    def do_set(self, line):
        super(DrStack, self).do_set(line)
        self.setprompt()

    def find_subjects(self, verb_module):
        """Get all subject methods in the verb module"""
        subjects = {}
        subject_completion = []
        for verb in (v for v in dir(verb_module) if v.endswith('Command')):
            verb_instance = getattr(verb_module, verb)(top=self)
            for subject in (s for s in dir(verb_instance)
                    if s.startswith('on_')):
                command = subject[3:].replace('_', '-')
                callback = getattr(verb_instance, subject)
                arguments = getattr(callback, 'arguments', [])
                subjects[command] = callback
                subject_completion.append(command + ' ')
        return (verb_instance, subjects, subject_completion)

    def get_glance_client(self):
        if not self.gc:
            self.gc = self._get_glance_client()

    def _get_glance_client(self):
        """
        Get glance client, auth with token from keystone
        """
        u = urlparse.urlparse(self.glance_url)
        use_ssl = (self.glance_url is not None and u.scheme == 'https')
        return glance_client.Client(
                host=u.hostname,
                port=u.port,
                use_ssl=use_ssl,
                auth_tok=self.auth_token,
                creds=None)

    def _get_keystone(self):
        """
        Authenticate with keystone and save the token.
        Get URLs to other services from the returned service catalog.
        """
        if not self.kc:
            self.kc = keystone_client.Client(
                    endpoint=can_haznt_slash(self.auth_url),
                    username=self.username,
                    password=self.password,
                    tenant_name=self.tenant_name,
                    auth_url=can_haznt_slash(self.auth_url))
            self.kc.authenticate()
            self.auth_token = self.kc.auth_token
            self.glance_url = self.kc.glance_url

    def _get_nova(self):
        """
        Get nova client
        """
        if not self.nc:
            self.nc = nova_client.Client(
                    self.username,
                    self.password,
                    self.tenant_name,
                    can_haz_slash(self.auth_url))
            self.nc.authenticate()

    def lookup_flavor(self, flavor):
        """Look up flavor by name"""
        if flavor:
            for f in self.nc.flavors.list():
                if flavor == f.name:
                    return f.id
        return None

    def lookup_image(self, image):
        """Look up image by name"""
        if image:
            for i in self.nc.images.list():
                if image == i.name:
                    return i
        return None

    def set_auth(self, auth_token=None,
                 auth_url=None, password=None,
                 tenant_name=None, username=None):
        self.auth_token = auth_token
        self.auth_url = can_haz_slash(auth_url)
        self.password = password
        self.tenant_name = tenant_name
        self.username = username
        self.setprompt()
        self._get_keystone()

    def setprompt(self, p=None):
        if p:
            self.prompt = p
        else:
            self.prompt = self.tenant_name + ":" + self.username + '> '


def setdebug(level=0):
    httplib2.debuglevel = level


def main(argv):
    """
    Shell entry point, handles top-level command-line args and
    hacks to make bits like readline and argparse/optparse behave
    """

    # hacky-hack for OS/X's lack of a real readline-capable python
    # to make tab completion work
    readline.parse_and_bind('bind ^I rl_complete')

    parser = argparse.ArgumentParser(description="DrStack")
    parser.add_argument('--auth_token', '--token', dest='auth_token',
                        default=os.environ.get('OS_AUTH_TOKEN', ''),
                        help='OpenStack authentication token')
    parser.add_argument('--auth_url', dest='auth_url',
                        default=os.environ.get('OS_AUTH_URL', ''),
                        help='OpenStack authentication URL')
    parser.add_argument('--password', dest='password',
                        default=os.environ.get('OS_PASSWORD', ''),
                        help='OpenStack password')
    parser.add_argument('--tenant', '--tenant_name', dest='tenant_name',
                        default=os.environ.get('OS_TENANT_NAME', ''),
                        help='OpenStack tenant name')
    parser.add_argument('--username', dest='username',
                        default=os.environ.get('OS_USERNAME', ''),
                        help='OpenStack user')
    parser.add_argument('--default_flavor', dest='default_flavor',
                        default=os.environ.get('DEFAULT_FLAVOR', ''),
                        help='Default flavor to create instance')
    parser.add_argument('--default_image', dest='default_image',
                        default=os.environ.get('DEFAULT_IMAGE', ''),
                        help='Default image to create instance')
    parser.add_argument('--debug', dest='debug', action='store_const',
                        const=1, default=0)
    (args, argv) = parser.parse_known_args(argv)

    # HACK(troyer): remove the above options from the command line
    # so cmd2/optparse don't try to handle them again
    sys.argv = argv

    # Configure included modules for appropriately explicit verbosity
    setdebug(args.debug)

    dr = DrStack()
    dr.set_auth(auth_token=args.auth_token,
                auth_url=args.auth_url,
                password=args.password,
                tenant_name=args.tenant_name,
                username=args.username)

    # Pass in more args directly ... yuck ...
    if args.default_flavor:
        dr.default_flavor = args.default_flavor
    if args.default_image:
        dr.default_image = args.default_image

    if len(argv) > 1:
        dr.allow_shell = False
        try:
            dr.onecmd(' '.join(argv[1:]))
        except Exception as e:
            print "%s" % e
    else:
        dr.cmdloop()


def test_main(argv):
    # The argparse/optparse/cmd2 modules muck about with sys.argv
    # so we save it and restore at the end to let the tests
    # run repeatedly without concatenating the args on each run
    save_argv = sys.argv

    main(argv)

    # Put it back so the next test has a clean copy
    sys.argv = save_argv
