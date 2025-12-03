Configuration
=============

This page describes all available configuration options for Django Growl Notifier.

Required Settings
-----------------

GROWL_HOSTS
~~~~~~~~~~~

List of Growl notification hosts. This is the only required setting.

**Type:** ``list``

**Format:** Each entry can be:

* ``'IP:PORT'`` - Explicit IP and port
* ``'IP'`` - IP only (uses default port 23053)
* ``'hostname:PORT'`` - Hostname with port
* ``'hostname'`` - Hostname only

**Example:**

.. code-block:: python

   GROWL_HOSTS = [
       '127.0.0.1:23053',
       '192.168.1.100',
       'server.local:23053',
   ]

Optional Settings
-----------------

GROWL_APP_NAME
~~~~~~~~~~~~~~

Application name displayed in Growl notifications.

**Type:** ``str``

**Default:** ``'Django Server'``

**Example:**

.. code-block:: python

   GROWL_APP_NAME = 'My Django Application'

GROWL_ENABLED
~~~~~~~~~~~~~

Enable or disable all Growl notifications globally.

**Type:** ``bool``

**Default:** ``True``

**Example:**

.. code-block:: python

   # Disable in production
   GROWL_ENABLED = not PRODUCTION

GROWL_ICON
~~~~~~~~~~

Custom icon for notifications. Supports file paths, file URIs, or HTTP URLs.

**Type:** ``str`` or ``pathlib.Path``

**Default:** Package default icon

**Supported formats:**

* Absolute file path: ``/path/to/icon.png``
* File URI: ``file:///path/to/icon.png``
* HTTP URL: ``https://example.com/icon.png``

**Example:**

.. code-block:: python

   GROWL_ICON = '/var/www/myapp/static/images/logo.png'
   
   # Or using Django's BASE_DIR
   GROWL_ICON = BASE_DIR / 'static' / 'logo.png'

GROWL_NOTIFY_ERRORS
~~~~~~~~~~~~~~~~~~~

Enable automatic error notifications via middleware.

**Type:** ``bool``

**Default:** ``True``

**Example:**

.. code-block:: python

   # Disable error notifications
   GROWL_NOTIFY_ERRORS = False

GROWL_STICKY_ERRORS
~~~~~~~~~~~~~~~~~~~

Make error notifications sticky (remain visible until dismissed).

**Type:** ``bool``

**Default:** ``True``

**Example:**

.. code-block:: python

   GROWL_STICKY_ERRORS = True

GROWL_STICKY_SERVER
~~~~~~~~~~~~~~~~~~~

Make server start notifications sticky.

**Type:** ``bool``

**Default:** ``False``

**Example:**

.. code-block:: python

   GROWL_STICKY_SERVER = True

Complete Configuration Example
-------------------------------

Here's a complete example configuration:

.. code-block:: python

   # settings.py
   
   from pathlib import Path
   
   BASE_DIR = Path(__file__).resolve().parent.parent
   
   INSTALLED_APPS = [
       # ... other apps
       'django_growl',
   ]
   
   # Growl Configuration
   GROWL_HOSTS = [
       '127.0.0.1:23053',
       '192.168.1.100:23053',
   ]
   
   GROWL_APP_NAME = 'My Django Project'
   GROWL_ENABLED = True
   GROWL_ICON = BASE_DIR / 'static' / 'images' / 'logo.png'
   
   # Error Notifications
   GROWL_NOTIFY_ERRORS = True
   GROWL_STICKY_ERRORS = True
   GROWL_STICKY_SERVER = False
   
   # Middleware (for error notifications)
   MIDDLEWARE = [
       # ... other middleware
       'django_growl.middleware.GrowlErrorMiddleware',
   ]

Environment-Specific Configuration
-----------------------------------

Different settings for different environments:

.. code-block:: python

   # settings.py
   
   import os
   
   # Base configuration
   GROWL_APP_NAME = 'My App'
   
   if os.getenv('ENVIRONMENT') == 'production':
       # Disable in production
       GROWL_ENABLED = False
   elif os.getenv('ENVIRONMENT') == 'staging':
       # Only notify staging server
       GROWL_ENABLED = True
       GROWL_HOSTS = ['staging-monitor.local:23053']
   else:
       # Development: notify locally
       GROWL_ENABLED = True
       GROWL_HOSTS = ['127.0.0.1:23053']

Environment Variables
---------------------

You can override settings using environment variables:

.. code-block:: bash

   # Disable notifications
   export GROWL_ENABLED=false
   
   # Custom icon
   export GROWL_ICON=/path/to/custom-icon.png
   
   python manage.py runserver

Next Steps
----------

* Learn how to use notifications: :doc:`usage`
* See practical examples: :doc:`examples1`
* API reference: :doc:`api/notifier`