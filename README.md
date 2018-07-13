Ansible INI to YAML inventory converter
=======================================

This repository contains a Python script for converting Ansible inventories in INI format to YAML format.

Usage
-----

The script is implemented as a filter:

    ini2yaml <inventory >inventory.yaml

Ansible 2.4.1 or later automatically recognizes the inventory format so the `.yaml` file extension can be omitted,
also allowing the default `/etc/ansible/hosts` inventory to be in YAML format.

Dependencies
------------
You may need the following dependencies:
```
pip install pyyaml

