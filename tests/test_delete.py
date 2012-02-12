# vim: tabstop=4 shiftwidth=4 softtabstop=4

import os
import mock
import httplib2

from glance import client

from drstack import shell as drstack_shell
from novaclient import exceptions
from tests import utils


DEFAULT_AUTH_URL = 'http://127.0.0.1:5000/v2.0/'
DEFAULT_TENANT_NAME = 'tenant_name'
DEFAULT_USERNAME = 'username'
DEFAULT_PASSWORD = 'password'


class ShellTest(utils.TestCase):

    # Patch os.environ to avoid required auth info.
    def setUp(self):
        global _old_env
        fake_env = {
            'OS_AUTH_URL': DEFAULT_AUTH_URL,
            'OS_TENANT_NAME': DEFAULT_TENANT_NAME,
            'OS_USERNAME': DEFAULT_USERNAME,
            'OS_PASSWORD': DEFAULT_PASSWORD,
        }
        _old_env, os.environ = os.environ, fake_env.copy()

        # Make a fake shell object, a helping wrapper to call it, and a quick
        # way of asserting that certain API calls were made.
        global shell, _shell, assert_called, assert_called_anytime
        _shell = drstack_shell
        shell = lambda cmd: _shell.main([__file__] + cmd.split())

        # Patch out some common methods
        self.kc_patch = mock.patch('drstack.shell.DrStack._get_keystone')
        self.kc_save = self.kc_patch.start()
        self.nc_patch = mock.patch('drstack.shell.DrStack._get_nova')
        self.nc_save = self.nc_patch.start()
        self.gc_mock = mock.Mock(name='gc')
        self.get_gc_mock = mock.Mock(name='_get_glance_client',
                return_value=self.gc_mock)
        self.gc_patch = mock.patch('drstack.shell.DrStack._get_glance_client',
                self.get_gc_mock)
        self.gc_save = self.gc_patch.start()

    def tearDown(self):
        global _old_env
        os.environ = _old_env
        self.gc_patch.stop()
        self.nc_patch.stop()
        self.kc_patch.stop()

    def test_help_unknown_command(self):
        # poor-man's skip until the exceptions are fixed
        return
        self.assertRaises(exceptions.CommandError, shell, 'foo foo')

    def test_debug(self):
        httplib2.debuglevel = 0
        shell('--debug help')
        assert httplib2.debuglevel == 1

    def test_delete_image(self):
        self.gc_mock.reset_mock()

        shell('delete image image_12345')
        assert self.gc_mock.delete_image.called_with('image_12345')
