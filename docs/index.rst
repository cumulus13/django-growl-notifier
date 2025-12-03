Django Growl Notifier
=====================

.. image:: https://badge.fury.io/py/django-growl-notifier.svg
   :target: https://badge.fury.io/py/django-growl-notifier
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/django-growl-notifier.svg
   :target: https://pypi.org/project/django-growl-notifier/
   :alt: Python Versions

.. image:: https://img.shields.io/badge/django-3.2%20%7C%204.0%20%7C%205.0-blue.svg
   :target: https://www.djangoproject.com/
   :alt: Django Versions

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License: MIT

.. image:: _static/logo.png
   :alt: Django Growl Notifier Logo
   :width: 350
   :align: center

Send Django development server notifications to Growl (or compatible notification systems).

Features
--------

* 🚀 Automatic notifications when Django server starts
* 🔥 Error notifications with detailed stacktrace
* 🌐 Multiple Growl hosts support
* 🎨 Custom icons support
* ⚙️ Easy configuration
* 🎯 Manual notifications anywhere in your code

Quick Start
-----------

Installation
~~~~~~~~~~~~

.. code-block:: bash

   pip install django-growl-notifier

Configuration
~~~~~~~~~~~~~

Add to your ``settings.py``:

.. code-block:: python

   INSTALLED_APPS = [
       # ... your other apps
       'django_growl',
   ]

   GROWL_HOSTS = [
       '127.0.0.1:23053',
       '192.168.1.100:23053',
   ]

   GROWL_APP_NAME = 'My Django App'

Usage
~~~~~

.. code-block:: bash

   python manage.py runserver

That's it! You'll receive notifications when your server starts.

Documentation Contents
----------------------

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   installation
   quickstart
   configuration
   usage
   examples1
   examples2

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/notifier
   api/middleware
   api/commands

.. toctree::
   :maxdepth: 1
   :caption: Additional Information

   troubleshooting
   changelog
   contributing
   license

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`