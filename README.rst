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

::

   image      instance

**DELETE**

::

   image      instance

**LIST**

::

   flavor                 image                  
   instance               keypair                role                 
   security-group         security-group-rules   service              
   tenant                 user                 

**SHOW**

::

   flavor     image      instance   tenant     user

Internals
=========

DrStack is a new command-line interface to the existing OpenStack client
libraries (python-novaclient, python-keystoneclient, glance).  It borrows
some code from those libraries to change the behaviour; those files are
located in drstack.compat.

In the case of glance, since the client bits are not yet separated from
the main code yet, the entire thing must be installed.

Sample Session
==============

Configure via env and run DrStack::

   dtroyer@beaker:~/src/openstack/drstack $ export OS_AUTH_URL=http://192.168.9.11:5000/v2.0
   dtroyer@beaker:~/src/openstack/drstack $ export OS_TENANT_NAME=admin
   dtroyer@beaker:~/src/openstack/drstack $ export OS_USERNAME=admin
   dtroyer@beaker:~/src/openstack/drstack $ export OS_PASSWORD=0penstack
   dtroyer@beaker:~/src/openstack/drstack $ dr list instance
   +--------------------------------------+---------+
   |                  id                  |   name  |
   +--------------------------------------+---------+
   | ead97d84-6988-47fc-9637-3564fc36bc4b | test    |
   +--------------------------------------+---------+
   dtroyer@beaker:~/src/openstack/drstack $ dr --username=demo --tenant-name=demo list instance
   +--------------------------------------+---------+
   |                  id                  |   name  |
   +--------------------------------------+---------+
   +--------------------------------------+---------+
   dtroyer@beaker:~/src/openstack/drstack $ dr show instance dcbc2185-ba17-4f81-95a9-c3fae9b2b042
   +------------------------+--------------------------------------+
   |        Property        |                Value                 |
   +------------------------+--------------------------------------+
   | OS-DCF:diskConfig      | MANUAL                               |
   | OS-EXT-STS:power_state | 1                                    |
   | flavor                 | m1.small                             |
   | id                     | dcbc2185-ba17-4f81-95a9-c3fae9b2b042 |
   | image                  | 754c231e-ade2-458c-9f91-c8df107ff7ef |
   | name                   | test                                 |
   | private_address        | 10.4.128.13                          |
   | status                 | ACTIVE                               |
   | user                   | vish                                 |
   +------------------------+--------------------------------------+
   dtroyer@beaker:~/src/openstack/drstack $ dr create image name=DrStack_0.1.0_source <dist/drstack-0.1.0.tar.gz
   Added new image with ID: 62f39031-2d3d-47d4-a467-6f9de0d1b7c3
   dtroyer@beaker:~/src/openstack/drstack $ dr list image
   +--------------------------------------+--------------------------------------------+
   |                  id                  |                    name                    |
   +--------------------------------------+--------------------------------------------+
   | 62f39031-2d3d-47d4-a467-6f9de0d1b7c3 | DrStack_0.1.0_source                       |
   +--------------------------------------+--------------------------------------------+
   dtroyer@beaker:~/src/openstack/drstack $ dr show image 62f39031-2d3d-47d4-a467-6f9de0d1b7c3
   +-----------+--------------------------------------+
   | Property  |                Value                 |
   +-----------+--------------------------------------+
   | id        | 62f39031-2d3d-47d4-a467-6f9de0d1b7c3 |
   | is_public | False                                |
   | min_disk  | 0                                    |
   | min_ram   | 0                                    |
   | name      | DrStack_0.1.0_source                 |
   | owner     | 2136df1a9984451eb470b37039d16dd2     |
   | status    | active                               |
   +-----------+--------------------------------------+

DrStack used cmd2 to give it a built-in shell::

   dtroyer@beaker:~/src/openstack/drstack $ dr
   Welcome to DrStack
   admin:admin> list flavor
   +----+-----------+
   | id |    name   |
   +----+-----------+
   | 1  | m1.tiny   |
   | 2  | m1.small  |
   | 3  | m1.medium |
   | 4  | m1.large  |
   | 5  | m1.xlarge |
   +----+-----------+
   admin:admin> list image
   +--------------------------------------+--------------------------------------------+
   |                  id                  |                    name                    |
   +--------------------------------------+--------------------------------------------+
   | 05ce2caf-e352-4034-b66d-596b78c2bd8d | oneiric-server-cloudimg-amd64-kernel       |
   | 0fe8d01a-4a91-4fa5-b502-574042d7f1b2 | cirros-0.3.0-x86_64-blank-kernel           |
   | 27f8098f-2dc7-4800-afbe-4297cc42c375 | natty-server-cloudimg-amd64                |
   | 2bbabfae-cc71-4089-8995-8ec97c43472d | cirros-0.3.0-x86_64-rootfs                 |
   | 3f3a8f02-b2b9-4512-9a05-1f64cffb65ec | ttylinux-uec-amd64-11.2_2.6.35-15_1        |
   | 73b80005-7da1-4d1a-b5ee-122be0078890 | natty-server-cloudimg-amd64-kernel         |
   | 754c231e-ade2-458c-9f91-c8df107ff7ef | oneiric-server-cloudimg-amd64              |
   | cac71199-987a-471d-9287-144724301c07 | ttylinux-uec-amd64-11.2_2.6.35-15_1-kernel |
   | f1f7be4a-4e65-41ab-bc0b-719a4df3a946 | cirros-0.3.0-x86_64-blank-ramdisk          |
   | fb09d36e-1884-42e7-970b-bffe853b67aa | cirros-0.3.0-x86_64-blank                  |
   +--------------------------------------+--------------------------------------------+
   admin:admin> create instance flavor=m1.small image=oneiric-server-cloudimg-amd64 name=dtroyer
   server 1cdbfd9a-106a-4010-bf1c-9afcdedb9951 started
   server 1cdbfd9a-106a-4010-bf1c-9afcdedb9951 status: ACTIVE
   admin:admin> list instance
   +--------------------------------------+---------+
   |                  id                  |   name  |
   +--------------------------------------+---------+
   | 1cdbfd9a-106a-4010-bf1c-9afcdedb9951 | dtroyer |
   | ead97d84-6988-47fc-9637-3564fc36bc4b | test    |
   +--------------------------------------+---------+
   admin:admin> delete instance 1cdbfd9a-106a-4010-bf1c-9afcdedb9951
   admin:admin> list instance
   +--------------------------------------+---------+
   |                  id                  |   name  |
   +--------------------------------------+---------+
   | ead97d84-6988-47fc-9637-3564fc36bc4b | test    |
   +--------------------------------------+---------+

Do some keystone stuff::

   admin:admin> list tenant
   +--------------------+----------------------------------+
   |        name        |                id                |
   +--------------------+----------------------------------+
   | admin              | 1be4461c727f4227906f000ffae827a0 |
   | demo               | 4f5bb0a385a44c598acde24af0f9e983 |
   | dtroyer            | efdbcaca932946928074d93852fa5d2d |
   +--------------------+----------------------------------+
   admin:admin> list user
   +----------+----------------------------------+
   |   name   |                id                |
   +----------+----------------------------------+
   | admin    | 28f65254922147619290fbcd0792ff15 |
   | demo     | 61c09d4570c24d01994de7829c4d0af0 |
   | dtroyer  | bd0ce17d88cf4a879cb0bdbbd2244a44 |
   +----------+----------------------------------+
   admin:admin> list role
   +----+----------------------+
   | id |         name         |
   +----+----------------------+
   | 1  | admin                |
   | 2  | Member               |
   | 3  | KeystoneAdmin        |
   | 4  | KeystoneServiceAdmin |
   | 5  | sysadmin             |
   | 6  | netadmin             |
   +----+----------------------+

Since DrStack uses cmd2, it has access to the python interpreter::

   admin:admin> py
   Python 2.7.1 (r271:86832, Jun 16 2011, 16:59:05) 
   [GCC 4.2.1 (Based on Apple Inc. build 5658) (LLVM build 2335.15.00)] on darwin
   Type "help", "copyright", "credits" or "license" for more information.
   (DrStack)
     
   >>> self.nc.servers.list()
   [<Server: dtroyer>, <Server: test>]
   >>> 
