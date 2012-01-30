=======
DrStack
=======

DrStack is an oddly named common command-line client for the OpenStack
Identity, Compute and Image APIs.  It is a thin wrapper to the
stock python-keystoneclient, python-novaclient and glance libraries
that implement the actual API clients.

DrStack's primary goal is to provide a unified shell command structure
and (as much as possible) a common language to describe operations
in openStack.

Configuration
=============

DrStack is entirely configured with environment variables and command-line
options.  It looks for
the standard variables listed in http://wiki.openstack.org/CLIAuth for
the 'password flow' variation.

   export OS_AUTH_URL=url-to-openstack-identity
   export OS_TENANT_NAME=tenant
   export OS_USERNAME=user
   export OS_PASSWORD=password    # yes, it isn't secure, we'll address it in the future

Alternatively the command-line options look very similar, but without the OS:

   --auth_url
   --tenant_name
   --username
   --password
