import os
import sys
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "python-drstack",
    version = "0.1.0",
    description = "OpenStack command-line client",
    long_description = read('README.rst'),
    author = "Dean Troyer",
    author_email = "dtroyer@gmail.com",
    packages = ['drstack'],
    scripts = ['bin/dr.py'],
    url = "https://github.com/dtroyer/python-drstack",
    license = "Apache",
    install_requires = [
        "python-keystoneclient >= 0.0.0",
        "python-novaclient >= 0.0.0",
    ],
)

