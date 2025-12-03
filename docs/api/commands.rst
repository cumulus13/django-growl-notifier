Management Commands
===================

Django management commands provided by django-growl-notifier.

runserver_growl
---------------

An enhanced version of Django's ``runserver`` command with explicit Growl notifications.

Usage
~~~~~

.. code-block:: bash

   python manage.py runserver_growl [addrport]

**Arguments:**

* ``addrport`` - Optional address and port (default: 127.0.0.1:8000)

**Examples:**

.. code-block:: bash

   # Default address and port
   python manage.py runserver_growl

   # Custom port
   python manage.py runserver_growl 8080

   # Custom address and port
   python manage.py runserver_growl 0.0.0.0:8000

   # IPv6
   python manage.py runserver_growl [::1]:8000

Features
~~~~~~~~

* All standard ``runserver`` features
* Explicit Growl notification when server starts
* Notification includes:
  
  * Django version
  * Settings module
  * Server address and port
  * Success/failure status

* Console output showing notification status

Notification Details
~~~~~~~~~~~~~~~~~~~~

When you run the command, you'll see:

.. code-block:: text

   System check identified no issues (0 silenced).
   December 03, 2025 - 11:35:30
   Django version 5.2.8, using settings 'myproject.settings'
   Starting development server at http://0.0.0.0:8000/
   ✓ Growl notification sent to 2 host(s)
   Quit the server with CONTROL-C.

The Growl notification shows:

.. code-block:: text

   Title: Django Server Started
   
   Message:
   Django version 5.2.8
   Settings: myproject.settings
   Starting server at http://0.0.0.0:8000/

Command Class
~~~~~~~~~~~~~

.. code-block:: python

   from django.core.management.commands.runserver import Command as RunserverCommand
   from django_growl import send_notification
   
   class Command(RunserverCommand):
       '''Enhanced runserver with Growl notifications'''
       
       help = 'Starts Django development server with Growl notifications.'

Comparison with Standard runserver
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Standard runserver:**

* Relies on AppConfig.ready() for notifications
* May send duplicate notifications on reload
* Notification timing depends on app loading

**runserver_growl:**

* Explicit notification in command
* Clear notification timing
* Better control over notification content
* Shows notification status in console

When to Use
~~~~~~~~~~~

Use ``runserver_growl`` when you want:

* Explicit control over notification timing
* Clear console output about notification status
* Consistent notification behavior
* To avoid duplicate notifications from auto-reload

Use standard ``runserver`` when you want:

* Standard Django behavior
* Automatic notifications via AppConfig
* Fewer commands to remember

Implementation
~~~~~~~~~~~~~~

The command is a thin wrapper around Django's built-in ``runserver``:

.. code-block:: python

   from django.core.management.commands.runserver import Command as RunserverCommand
   from django.conf import settings
   from django_growl import send_notification
   import django

   class Command(RunserverCommand):
       help = 'Starts development server with Growl notifications.'
       
       def inner_run(self, *args, **options):
           try:
               # Send notification
               django_version = django.get_version()
               settings_module = settings.SETTINGS_MODULE
               addr = options.get('addrport', f"{self.addr}:{self.port}")
               
               message = (
                   f"Django version {django_version}\\n"
                   f"Settings: {settings_module}\\n"
                   f"Starting server at http://{addr}/"
               )
               
               send_notification(
                   title="Django Server Started",
                   message=message,
                   note_type='Server Status',
                   sticky=getattr(settings, 'GROWL_STICKY_SERVER', False)
               )
               
               # Show success in console
               growl_hosts = getattr(settings, 'GROWL_HOSTS', [])
               self.stdout.write(
                   self.style.SUCCESS(
                       f"✓ Growl notification sent to {len(growl_hosts)} host(s)"
                   )
               )
               
           except Exception as e:
               # Show error but don't fail
               self.stderr.write(
                   self.style.WARNING(
                       f"Failed to send Growl notification: {e}"
                   )
               )
           
           # Run standard server
           return super().inner_run(*args, **options)

See Also
~~~~~~~~

* :doc:`../usage` - General usage guide
* :doc:`../configuration` - Configuration options
* :doc:`notifier` - Notifier API reference