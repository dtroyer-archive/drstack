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
Utility functions for DrParse
"""

import prettytable

from novaclient import utils


# lifted from glance/common/utils.py
def bool_from_string(subject):
    """
    Interpret a string as a boolean.

    Any string value in:
        ('True', 'true', 'On', 'on', '1')
    is interpreted as a boolean True.

    Useful for JSON-decoded stuff and config file parsing
    """
    if isinstance(subject, bool):
        return subject
    elif isinstance(subject, int):
        return subject == 1
    if hasattr(subject, 'startswith'):  # str or unicode...
        if subject.strip().lower() in ('true', 'on', '1'):
            return True
    return False


def show_object(manager, id, fields=None):
    """Check id, lookup object, display result fields"""
    if not id:
        print "no id specified"
        return
    obj = manager.get(id)
    print_dict_fields(obj, fields)


def print_obj_fields(obj, fields=[]):
    """Print specified object fields"""
    # Select the fields to print, then passthrough to novaclient
    a = {name: getattr(obj, name, '') for name in fields}
    utils.print_dict(a)


def print_dict_fields(obj, fields=[]):
    """Print specified object fields"""
    # Select the fields to print, then passthrough to novaclient
    a = {name: obj[name] for name in fields}
    utils.print_dict(a)


def print_dict_list(objs, fields, formatters={}):
    """Print list of dicts"""
    mixed_case_fields = []
    pt = prettytable.PrettyTable([f for f in fields], caching=False)
    pt.aligns = ['l' for f in fields]

    for o in objs:
        row = []
        for field in fields:
            if field in formatters:
                row.append(formatters[field](o))
            else:
                if field in mixed_case_fields:
                    field_name = field.replace(' ', '_')
                else:
                    field_name = field.lower().replace(' ', '_')
                data = o[field_name]
                row.append(data)
        pt.add_row(row)

    pt.printt(sortby=fields[0])


def print_list(objs, fields, formatters={}):
    """Print list of objects"""
    # Passthrough to novaclient
    utils.print_list(objs, fields, formatters=formatters)
