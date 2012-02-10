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

from keystoneclient import service_catalog
from keystoneclient.v2_0 import client as keystone_client


class Client(keystone_client.Client):

    def __init__(self, endpoint=None, **kwargs):
        super(Client, self).__init__(endpoint=endpoint, **kwargs)

    def _extract_service_catalog(self, url, body):
        """ Set the client's service catalog from the response data. """
        self.service_catalog = service_catalog.ServiceCatalog(body)
        try:
            self.auth_token = self.service_catalog.get_token()
        except KeyError:
            raise exceptions.AuthorizationFailure()

        # FIXME(ja): we should be lazy about setting managment_url.
        # in fact we should rewrite the client to support the service
        # catalog (api calls should be directable to any endpoints)
        try:
            self.management_url = self.service_catalog.url_for(attr='region',
                filter_value=self.region_name, endpoint_type='internalURL')
        except:
            # Unscoped tokens don't return a service catalog
            _logger.exception("unable to retrieve service catalog with token")
