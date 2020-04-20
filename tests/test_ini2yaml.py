#!/usr/bin/env python3

import os
import six
import subprocess
import yaml

def remove_keys(adict, keys):
    for key in keys:
        adict.pop(key, None)

def normalize(hostvars_ini, hostvars_yaml):
    ignored_keys = ('inventory_dir', 'inventory_file', 'omit', 'groups')
    remove_keys(hostvars_ini, ignored_keys)
    remove_keys(hostvars_yaml, ignored_keys)

    for key, value in hostvars_yaml.items():
        if isinstance(value, bool) and isinstance(hostvars_ini[key], six.string_types):
            hostvars_ini[key] = yaml.load("value: " + hostvars_ini[key])['value']  # Convert to boolean according to YAML if boolean in YAML inventory
        elif isinstance(value, dict) and isinstance(hostvars_ini[key], six.string_types):
            hostvars_ini[key] = yaml.load("value: " + hostvars_ini[key])['value']  # Unwrap nested dicts if unwrapped in YAML inventory
        elif isinstance(value, list) and isinstance(hostvars_ini[key], six.string_types):
            hostvars_ini[key] = yaml.load("value: " + hostvars_ini[key])['value']  # Unwrap nested lists if unwrapped in YAML inventory

def test_hostvars(request, tmpdir, ansible_adhoc):
    ini_inventory_filename = os.path.join(request.fspath.dirname, 'inventory.ini')
    yaml_inventory_filename = str(tmpdir.join('inventory.yaml'))

    with open(ini_inventory_filename, 'r') as ini_inventory_file, open(yaml_inventory_filename, 'w') as yaml_inventory_file:
        process = subprocess.Popen(os.path.join(request.fspath.dirname, "../ini2yaml"), stdin=ini_inventory_file, stdout=yaml_inventory_file)
        process.communicate()
        assert process.returncode == 0

    ini_hostvars = yaml.load(ansible_adhoc(inventory=ini_inventory_filename).localhost.debug(msg='{{ hostvars.localhost | to_yaml }}').values()[0]['msg']) #['hostvars']['localhost']
    yaml_hostvars = yaml.load(ansible_adhoc(inventory=yaml_inventory_filename).localhost.debug(msg='{{ hostvars.localhost | to_yaml }}').values()[0]['msg']) #['hostvars']['localhost']
    normalize(ini_hostvars, yaml_hostvars)

    assert ini_hostvars == yaml_hostvars
