=======
DrStack
=======

DrStack is an oddly named common command-line client for the OpenStack
Identity, Compute and Image APIs.  It is a thin wrapper to the
stock python-keystoneclient, python-novaclient and glance libraries
that implement the actual API clients.

DrStack's primary goal is to provide a unified shell command structure
and (as much as possible) a common language to describe operations
in OpenStack.

Configuration
=============

DrStack is entirely configured with environment variables and command-line
options.  It looks for
the standard variables listed in http://wiki.openstack.org/CLIAuth for
the 'password flow' variation.

::

   export OS_AUTH_URL=url-to-openstack-identity
   export OS_TENANT_NAME=tenant
   export OS_USERNAME=user
   export OS_PASSWORD=password    # yes, it isn't secure, we'll address it in the future

Alternatively the command-line options look very similar, but without the OS::

   --auth_url
   --tenant_name
   --username
   --password

Additional command-line options and their associated environment variables
are listed here::

   --debug             # turns on some debugging of the API conversation
                         (via httplib2)
   --default_flavor    # the _name_ of the flavor used to create an instance
                         if flavor= is not specified in *create instance*
   --default_image     # the _name_ of the image used to create an instance
                         if image= is not specified in *create instance*

Usage
=====

DrStack provides a command-line interface via the *dr* script.  Invoked
with no arguments, or only the configuration options above, it provides
an interactive readline-based interface to its entire command set.

When invoked in interactive mode, the client credentials are cached to
avoid the need to set up each object on every command invocation.
Bash-style tab completion is enabled.

Commands
========

DrStack uses a verb-subject command structure.

In interactive mode, <TAB><TAB> will display the list of available 
subjects for each command verb.

**CREATE**

**DELETE**

**LIST**

**SHOW**
