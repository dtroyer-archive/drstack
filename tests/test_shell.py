# vim: tabstop=4 shiftwidth=4 softtabstop=4

import os
import mock
import httplib2

from drstack import shell as drstack_shell
from novaclient import exceptions
from tests import utils


DEFAULT_AUTH_URL = 'http://127.0.0.1:5000/v2.0/'
DEFAULT_TENANT_NAME = 'tenant_name'
DEFAULT_USERNAME = 'username'
DEFAULT_PASSWORD = 'password'

AUTH_ARGS = {
    'auth_url': DEFAULT_AUTH_URL,
    'auth_token': '',
    'tenant_name': DEFAULT_TENANT_NAME,
    'username': DEFAULT_USERNAME,
    'password': DEFAULT_PASSWORD}


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

    def tearDown(self):
        global _old_env
        os.environ = _old_env
        self.kc_patch.stop()
        self.nc_patch.stop()

    def test_help_unknown_command(self):
        self.assertRaises(exceptions.CommandError, shell, 'foo foo')

    def test_debug(self):
        httplib2.debuglevel = 0
        shell('--debug help')
        assert httplib2.debuglevel == 1

    def test_shell_args(self):

        def test_args(desc, default_args):
            onecmd_mock = mock.Mock(desc)
            with mock.patch('drstack.shell.DrStack.onecmd', onecmd_mock):
                shell('list user')
                onecmd_mock.assert_called_with(('list user'))
                auth_mock = mock.Mock(desc)
                with mock.patch('drstack.shell.DrStack.set_auth', auth_mock):
                    shell('list user')
                    assert auth_mock.call_args == ((), default_args)
                    shell('--auth_url http://0.0.0.0:5000/ --tenant_name fred '
                          '--username barney --password xyzpdq '
                          'list user')
                    assert auth_mock.call_args == ((), {
                        'auth_url': 'http://0.0.0.0:5000/',
                        'auth_token': '',
                        'tenant_name': 'fred',
                        'username': 'barney',
                        'password': 'xyzpdq'})

        test_args('default environment', AUTH_ARGS)
        save_env, os.environ = os.environ, {}
        test_args('no environment', {'auth_url': '', 'auth_token': '',
                'tenant_name': '', 'username': '', 'password': ''})
        os.environ = save_env
