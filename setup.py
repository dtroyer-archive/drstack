import os
import sys
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

requirements = [
        'httplib2', 
        'prettytable',
        "python-keystoneclient >= 2012.1",
        "python-novaclient >= 2012.1",
]

if sys.version_info < (2, 6):
    requirements.append('simplejson')
if sys.version_info < (2, 7):
    requirements.append("argparse")

setup(
    name = "drstack",
    version = "0.1.0",
    description = "OpenStack command-line client",
    long_description = read('README.rst'),
    author = "Dean Troyer",
    author_email = "dtroyer@gmail.com",
    packages=find_packages(exclude=['bin']),
    #packages = ['drstack'],
    scripts = ['bin/dr'],
    url = "https://github.com/dtroyer/drstack",
    license = "Apache",
    install_requires=requirements,

    tests_require = ["nose", "mock", "mox"],
    test_suite = "nose.collector",

    #entry_points = {
    #    'console_scripts': ['dr = drstack.shell:main']
    #}
)

