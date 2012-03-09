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
Keystone client
"""

import logging

from keystoneclient import exceptions
from keystoneclient import service_catalog
from keystoneclient.v2_0 import client as keystone_client
from keystoneclient.v2_0 import users as keystone_users


_logger = logging.getLogger(__name__)


class Client(keystone_client.Client):

    def __init__(self, endpoint=None, **kwargs):
        super(Client, self).__init__(endpoint=endpoint, **kwargs)

        # Use our UserManager
        self.users = UserManager(self)

    def _extract_service_catalog(self, url, body):
        """ Set the client's service catalog from the response data. """
        self.service_catalog = service_catalog.ServiceCatalog(body)
        try:
            self.auth_token = self.service_catalog.get_token()['id']
        except KeyError:
            raise exceptions.AuthorizationFailure()

        # FIXME(ja): we should be lazy about setting managment_url.
        # in fact we should rewrite the client to support the service
        # catalog (api calls should be directable to any endpoints)
        try:
            self.management_url = self.service_catalog.url_for(attr='region',
                filter_value=self.region_name, endpoint_type='adminURL')
        except KeyError:
            #print "no admin url"
            pass
        except:
            # Unscoped tokens don't return a service catalog
            _logger.exception("unable to retrieve service catalog with token")

        # Get the glance endpoint
        try:
            self.glance_url = self.service_catalog.url_for(attr='region',
                filter_value=self.region_name,
                service_type='image', endpoint_type='publicURL')
        except KeyError:
            print "no glance url?"
        except:
            # Unscoped tokens don't return a service catalog
            _logger.exception("unable to retrieve service catalog with token")


class UserManager(keystone_users.UserManager):

    def __init__(self, *args, **kwargs):
        super(UserManager, self).__init__(*args, **kwargs)

    def get_by_name(self, user_name):
        """
        Get a user by name.
        """
        try:
            return (u for u in self.list() if u.name == user_name).next()
        except StopIteration:
            msg = 'User %s not found' % user_name
            raise exceptions.NotFound(msg)

    def get_by_name_or_id(self, user):
        """
        Get a user by name, fall back to id if not found.
        """
        try:
            user_ref = self.get_by_name(user)
        except exceptions.NotFound:
            try:
                user_ref = self.get(user)
            except Exception, e:
                msg = 'User %s not found' % user
                raise exceptions.NotFound(msg)
        return user_ref
