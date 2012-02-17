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
CREATE command
"""

import sys
import time

from glance.common import exception as gc_exceptions

from drstack import base
from drstack.compat import glance
from drstack import utils


class CreateCommand(base.Command):

    def __init__(self, top=None):
        super(CreateCommand, self).__init__(cmd='create', top=top)

    # Based on glance/bin/glance.image_add()
    def on_image(self, args):
        """
        Image metadata is specified in the command as atribute=value pairs.

        id                  Optional; image ID
                            Default: generated UUID
        name                Required; name of image
        is_public           Optional; image visibility to public;
                            Default: False
        protected           Optional; protect image from deletion;
                            Default: False
        disk_format         Optional; 'vhd', 'vmdk', 'raw', 'qcow2', 'ami'
                            Default: 'raw'.
        container_format    Optional; 'ovf' or 'ami';
                            Default: 'ovf'
        location            Optional; URI of current image location;
                            a local file is specified as:
                            location=file:///usr/share/images/image.tar.gz
                            If not specified image will be read from stdin
                            Default: None

        Other attributes are handled as custom properties.
        """
        self.top.get_glance_client()
        try:
            fields = glance.get_image_fields_from_args(args[1:])
        except RuntimeError, e:
            print e
            return

        if 'name' not in fields.keys() or not fields['name']:
            print "Please specify a name for the image using name=VALUE"

        image_meta = {
                'name': fields.pop('name'),
                'is_public': utils.bool_from_string(
                    fields.pop('is_public', False)),
                'protected': utils.bool_from_string(
                    fields.pop('protected', False)),
                'disk_format': fields.pop('disk_format', 'raw'),
                'min_disk': fields.pop('min_disk', 0),
                'min_ram': fields.pop('min_ram', 0),
                'container_format': fields.pop('container_format', 'ovf')}

        # Strip any args that are not supported
        unsupported_fields = ['status', 'size']
        for field in unsupported_fields:
            if field in fields.keys():
                print 'Found non-settable field %s. Removing.' % field
                fields.pop(field)

        if 'location' in fields.keys():
            image_meta['location'] = fields.pop('location')

        # We need either a location or image data/stream to add...
        image_location = image_meta.get('location')
        image_data = None
        if not image_location:
            # Grab the image data stream from stdin or redirect,
            # otherwise error out
            image_data = sys.stdin

        try:
            image_meta = self.top.gc.add_image(image_meta, image_data)
            image_id = image_meta['id']
            print "Added new image with ID: %s" % image_id
        except gc_exceptions.ClientConnectionError, e:
            host = options.host
            port = options.port
            print ("Failed to connect to the Glance API server "
                   "%(host)s:%(port)d. Is the server running?" % locals())
        except Exception, e:
            print "Failed to add image. Got error: %s" % e
            pieces = unicode(e).split('\n')
            for piece in pieces:
                print piece

    def on_instance(self, args):
        self.top._get_nova()
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

    def on_role(self, args):
        if len(args) < 2:
            print "role name missing"
            return
        print self.top.kc.roles.create(args[1])
