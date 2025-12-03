Installation
============

Requirements
------------

* Python >= 3.8
* Django >= 3.2
* gntp >= 1.0.3
* version_get
* Growl or compatible notification system

Via pip
-------

Install the latest stable version from PyPI:

.. code-block:: bash

   pip install django-growl-notifier

From Source
-----------

Install from GitHub repository:

.. code-block:: bash

   git clone https://github.com/cumulus13/django-growl-notifier.git
   cd django-growl-notifier
   pip install -e .

Development Installation
------------------------

For development with all dependencies:

.. code-block:: bash

   git clone https://github.com/cumulus13/django-growl-notifier.git
   cd django-growl-notifier
   pip install -e .[dev]

This installs additional packages for testing and documentation.

Growl Setup
-----------

Windows
~~~~~~~

1. Download `Growl for Windows <http://www.growlforwindows.com/>`_
2. Install and run Growl
3. Enable "Listen for incoming notifications" in Growl settings
4. Configure network security settings if needed

macOS
~~~~~

1. Download `Growl <https://growl.github.io/growl/>`_
2. Install and run Growl
3. Enable "Listen for incoming notifications" in preferences
4. Configure network settings if receiving from remote hosts

Linux
~~~~~

Use compatible notification systems like:

* `notify-send` with GNTP bridge
* `Snarl`
* Custom GNTP-compatible notification daemon

Verifying Installation
----------------------

Check if the package is installed correctly:

.. code-block:: python

   >>> import django_growl
   >>> django_growl.__version__
   '0.1.0'

Next Steps
----------

Continue to :doc:`quickstart` for configuration and basic usage.