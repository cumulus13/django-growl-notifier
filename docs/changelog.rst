Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

[1.0.4] - 2025-12-03
--------------------

Added
~~~~~

* Initial release
* Core notification functionality
* Support for multiple Growl hosts
* Custom icon support
* Automatic server start notifications
* Error notification middleware
* ``runserver_growl`` management command
* Comprehensive configuration options
* Full documentation
* Examples and troubleshooting guide

Features
~~~~~~~~

* Send notifications to multiple Growl hosts simultaneously
* Customize notification icons
* Sticky notifications support
* Three notification types: Info, Error, Server Status
* Environment variable overrides
* Detailed logging
* Django 3.2+ support
* Python 3.8+ support

[Unreleased]
------------

Planned features for future releases:

* Notification templates
* Rich notification formatting
* Notification history
* Web dashboard for notification management
* Support for additional notification systems (ntfy, Pushover)
* Async notification support
* Notification queuing
* Rate limiting
