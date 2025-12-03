Quick Start Guide
=================

This guide will help you get started with Django Growl Notifier in minutes.

Step 1: Install
---------------

.. code-block:: bash

   pip install django-growl-notifier

Step 2: Configure Django
-------------------------

Add to ``INSTALLED_APPS`` in your ``settings.py``:

.. code-block:: python

   INSTALLED_APPS = [
       # ... your other apps
       'django_growl',
   ]

Step 3: Configure Growl Hosts
------------------------------

Add Growl configuration to ``settings.py``:

.. code-block:: python

   # Required: List of Growl hosts
   GROWL_HOSTS = [
       '127.0.0.1:23053',        # Local machine
       '192.168.1.100:23053',    # Remote machine
   ]

   # Optional: Customize app name
   GROWL_APP_NAME = 'My Django Project'

   # Optional: Enable/disable notifications
   GROWL_ENABLED = True

Step 4: Run Your Server
------------------------

Start your Django development server:

.. code-block:: bash

   python manage.py runserver

You should see a Growl notification when the server starts!

What's Next?
------------

* **Configure error notifications**: See :doc:`configuration`
* **Send custom notifications**: See :doc:`usage`
* **View examples**: See :doc:`examples1`
* **Troubleshooting**: See :doc:`troubleshooting`

Basic Usage Example
-------------------

Send a custom notification from your code:

.. code-block:: python

   from django_growl import send_notification

   def my_view(request):
       # Your view logic here
       
       send_notification(
           title="Task Complete",
           message="Data processing finished successfully"
       )
       
       return render(request, 'success.html')

That's it! You're ready to use Django Growl Notifier.