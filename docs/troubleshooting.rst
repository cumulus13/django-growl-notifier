Troubleshooting
===============

This page helps you diagnose and fix common issues with Django Growl Notifier.

Common Issues
-------------

Notifications Not Appearing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptom:** No Growl notifications are shown.

**Solutions:**

1. **Check if Growl is running**

   * Windows: Check Task Manager for ``Growl.exe``
   * macOS: Check menu bar for Growl icon
   * Linux: Verify GNTP-compatible daemon is running

2. **Verify Growl is listening for network notifications**

   * Open Growl settings/preferences
   * Enable "Listen for incoming notifications"
   * Check "Allow remote application registration"

3. **Test network connectivity**

   .. code-block:: bash
   
      # Test if port is open
      telnet 192.168.1.100 23053
      
      # Or using netcat
      nc -zv 192.168.1.100 23053

4. **Check Django settings**

   .. code-block:: python
   
      # In Django shell
      from django.conf import settings
      
      print("GROWL_ENABLED:", getattr(settings, 'GROWL_ENABLED', 'Not set'))
      print("GROWL_HOSTS:", getattr(settings, 'GROWL_HOSTS', 'Not set'))
      print("App installed:", 'django_growl' in settings.INSTALLED_APPS)

5. **Enable debug logging**

   .. code-block:: python
   
      # settings.py
      LOGGING = {
          'version': 1,
          'disable_existing_loggers': False,
          'handlers': {
              'console': {
                  'class': 'logging.StreamHandler',
              },
          },
          'loggers': {
              'django_growl': {
                  'handlers': ['console'],
                  'level': 'DEBUG',
                  'propagate': False,
              },
          },
      }

Notifications Work Locally But Not on Remote Hosts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptom:** Local notifications work, but remote hosts don't receive them.

**Solutions:**

1. **Check firewall settings**

   * Port 23053 must be open on remote machines
   * Both incoming and outgoing traffic
   * Check both OS firewall and network firewall

   .. code-block:: bash
   
      # Windows: Allow port in Windows Firewall
      netsh advfirewall firewall add rule name="Growl" dir=in action=allow protocol=TCP localport=23053
      
      # Linux: Using ufw
      sudo ufw allow 23053/tcp
      
      # Linux: Using iptables
      sudo iptables -A INPUT -p tcp --dport 23053 -j ACCEPT

2. **Verify Growl network settings on remote machine**

   * Enable "Listen for incoming notifications"
   * Check allowed hosts/networks
   * Verify password settings (if any)

3. **Test with command line**

   .. code-block:: python
   
      # Test script to verify connectivity
      import gntp.notifier
      
      growl = gntp.notifier.GrowlNotifier(
          applicationName='Test',
          notifications=['Test'],
          defaultNotifications=['Test'],
          hostname='192.168.1.100',
          port=23053
      )
      
      try:
          growl.register()
          growl.notify(
              noteType='Test',
              title='Test Notification',
              description='Testing connectivity'
          )
          print("Success!")
      except Exception as e:
          print(f"Error: {e}")

Icons Not Showing
~~~~~~~~~~~~~~~~~

**Symptom:** Notifications appear but without icons.

**Solutions:**

1. **Verify icon file exists**

   .. code-block:: python
   
      # In Django shell
      from pathlib import Path
      from django.conf import settings
      
      icon_path = Path(settings.GROWL_ICON)
      print(f"Icon exists: {icon_path.is_file()}")
      print(f"Icon path: {icon_path}")

2. **Check icon format**

   * Supported formats: PNG, JPG, GIF
   * Recommended: PNG with transparency
   * Size: 48x48 to 128x128 pixels

3. **Use absolute paths or URIs**

   .. code-block:: python
   
      # Good
      GROWL_ICON = '/absolute/path/to/icon.png'
      GROWL_ICON = Path(BASE_DIR) / 'static' / 'logo.png'
      
      # Bad
      GROWL_ICON = 'icon.png'  # Relative path may not work

4. **Test with default icon**

   .. code-block:: python
   
      # Temporarily remove custom icon
      # GROWL_ICON = ...  # Comment this out
      
      # Restart server and test

Error Notifications Not Working
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptom:** Server start notifications work, but error notifications don't appear.

**Solutions:**

1. **Verify middleware is installed**

   .. code-block:: python
   
      # settings.py
      MIDDLEWARE = [
          # ... other middleware
          'django_growl.middleware.GrowlErrorMiddleware',  # Must be here
      ]

2. **Check error notification is enabled**

   .. code-block:: python
   
      # settings.py
      GROWL_NOTIFY_ERRORS = True  # Must be True

3. **Test with intentional error**

   .. code-block:: python
   
      # Create a test view
      def test_error(request):
          raise Exception("Test error for Growl notification")

4. **Check error logs**

   .. code-block:: python
   
      # Enable logging for middleware
      LOGGING = {
          'loggers': {
              'django_growl.middleware': {
                  'handlers': ['console'],
                  'level': 'DEBUG',
              },
          },
      }

Duplicate Notifications
~~~~~~~~~~~~~~~~~~~~~~~

**Symptom:** Receiving multiple identical notifications.

**Cause:** Usually due to Django auto-reloader in development.

**Solutions:**

1. **This is expected behavior in development** - Django's runserver reloads code automatically

2. **Disable auto-reload for testing**

   .. code-block:: bash
   
      python manage.py runserver --noreload

3. **Won't occur in production** (using gunicorn, uwsgi, etc.)

Connection Timeout
~~~~~~~~~~~~~~~~~~

**Symptom:** Error messages about connection timeout.

**Solutions:**

1. **Increase timeout** (if using custom code)

   .. code-block:: python
   
      import gntp.notifier
      
      growl = gntp.notifier.GrowlNotifier(
          # ... other params
          timeout=5  # Increase timeout to 5 seconds
      )

2. **Check network latency**

   .. code-block:: bash
   
      ping 192.168.1.100

3. **Verify Growl is responding**

   * Restart Growl application
   * Check Growl logs for errors

Package Import Errors
~~~~~~~~~~~~~~~~~~~~~

**Symptom:** ``ImportError`` or ``ModuleNotFoundError``.

**Solutions:**

1. **Verify installation**

   .. code-block:: bash
   
      pip show django-growl-notifier

2. **Check Python path**

   .. code-block:: python
   
      import sys
      print(sys.path)

3. **Reinstall package**

   .. code-block:: bash
   
      pip uninstall django-growl-notifier
      pip install django-growl-notifier

4. **Verify Django detects the app**

   .. code-block:: bash
   
      python manage.py shell
      >>> from django.apps import apps
      >>> apps.get_app_config('django_growl')

Debugging Tips
--------------

Enable Verbose Logging
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # settings.py
   LOGGING = {
       'version': 1,
       'disable_existing_loggers': False,
       'formatters': {
           'verbose': {
               'format': '{levelname} {asctime} {module} {message}',
               'style': '{',
           },
       },
       'handlers': {
           'console': {
               'class': 'logging.StreamHandler',
               'formatter': 'verbose',
           },
       },
       'loggers': {
           'django_growl': {
               'handlers': ['console'],
               'level': 'DEBUG',
               'propagate': False,
           },
       },
   }

Test Notification Manually
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # In Django shell
   from django_growl import send_notification
   
   send_notification(
       title="Test",
       message="Testing notification system",
       sticky=True
   )

Check Notifier Status
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # In Django shell
   from django_growl import get_growl_notifier
   
   notifier = get_growl_notifier()
   print(f"Enabled: {notifier.enabled}")
   print(f"Hosts configured: {len(notifier.growl_hosts)}")
   print(f"Notifiers registered: {len(notifier.notifiers)}")
   
   for item in notifier.notifiers:
       print(f"  - {item['host']}:{item['port']}")

Performance Issues
------------------

Notifications Slowing Down Application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptom:** Application feels slow when notifications are enabled.

**Solutions:**

1. **Use async/background tasks** for notifications

   .. code-block:: python
   
      from django_growl import send_notification
      from celery import shared_task
      
      @shared_task
      def send_async_notification(title, message):
          send_notification(title, message)
      
      # Use in views
      send_async_notification.delay("Task Done", "Processing complete")

2. **Reduce notification frequency**

   * Don't send notification on every request
   * Aggregate multiple events into one notification

3. **Disable in production**

   .. code-block:: python
   
      # settings/production.py
      GROWL_ENABLED = False

Getting Help
------------

If you're still experiencing issues:

1. **Check the logs** - Enable DEBUG logging as shown above

2. **Search existing issues** - `GitHub Issues <https://github.com/cumulus13/django-growl-notifier/issues>`_

3. **Create a new issue** with:
   
   * Django version
   * Python version
   * django-growl-notifier version
   * Full error traceback
   * Relevant configuration

4. **Contact support**:
   
   * Email: cumulus13@gmail.com
   * GitHub: @cumulus13

Useful Commands
---------------

.. code-block:: bash

   # Check installed version
   pip show django-growl-notifier
   
   # Test Growl connectivity
   telnet localhost 23053
   
   # Check Django settings
   python manage.py shell -c "from django.conf import settings; print(settings.GROWL_HOSTS)"
   
   # Test notification
   python manage.py shell -c "from django_growl import send_notification; send_notification('Test', 'Testing')"
   
   # View logs in real-time
   python manage.py runserver 2>&1 | grep django_growl

Next Steps
----------

* Back to :doc:`usage`
* Check :doc:`examples1`
* View :doc:`api/notifier`
