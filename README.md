# Django Auth Manager

This is a django extension that extends `manage.py` commands and provide the ability to retrieve information about users, groups and their permissions

## Installation

Install using PIP:

```bash
pip install django-auth-manager
```

Add django\_auth\_manager to INSTALLED\_APPS:

```
INSTALLED_APPS += ["django_auth_manager"]
```

## Usage

Currently, the following commands are supported (use `--help` to get more information):

* `python3 manage.py fetch_users --help`
* `python3 manage.py fetch_groups --help`
