# vim: tabstop=4 shiftwidth=4 softtabstop=4

import os
import mock
import httplib2

from drstack import shell as drstack_shell
from novaclient import exceptions
from tests import utils


class ShellTest(utils.TestCase):

    # Patch os.environ to avoid required auth info.
    def setUp(self):
        global _old_env
        fake_env = {
            'OS_AUTH_URL': 'http://127.0.0.1:5000/v2.0',
            'OS_TENANT_NAME': 'tenant_name',
            'OS_USERNAME': 'username',
            'OS_PASSWORD': 'password',
        }
        _old_env, os.environ = os.environ, fake_env.copy()

        # Make a fake shell object, a helping wrapper to call it, and a quick
        # way of asserting that certain API calls were made.
        global shell, _shell, assert_called, assert_called_anytime
        _shell = drstack_shell
        shell = lambda cmd: _shell.main([__file__] + cmd.split())

    def tearDown(self):
        global _old_env
        os.environ = _old_env

    def test_help_unknown_command(self):
        self.assertRaises(exceptions.CommandError, shell, 'foo foo')

    def test_debug(self):
        httplib2.debuglevel = 0
        shell('--debug help')
        assert httplib2.debuglevel == 1
