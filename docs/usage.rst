Usage Guide
===========

This guide covers different ways to use Django Growl Notifier.

Automatic Notifications
-----------------------

Server Start Notifications
~~~~~~~~~~~~~~~~~~~~~~~~~~

Notifications are sent automatically when you start the Django development server:

.. code-block:: bash

   $ python manage.py runserver
   System check identified no issues (0 silenced).
   December 03, 2025 - 11:35:30
   Django version 5.2.8, using settings 'myproject.settings'
   Starting development server at http://127.0.0.1:8000/
   ✓ Growl notification sent to 2 host(s)
   Quit the server with CONTROL-C.

You can also use the explicit command:

.. code-block:: bash

   python manage.py runserver_growl

Error Notifications
~~~~~~~~~~~~~~~~~~~

Configure middleware in ``settings.py``:

.. code-block:: python

   MIDDLEWARE = [
       # ... other middleware
       'django_growl.middleware.GrowlErrorMiddleware',
   ]
   
   GROWL_NOTIFY_ERRORS = True
   GROWL_STICKY_ERRORS = True

Now you'll receive notifications for all 500 errors with:

* Full exception details
* Stack trace
* Request path and method
* Sticky notifications (won't disappear)

Manual Notifications
--------------------

Basic Notification
~~~~~~~~~~~~~~~~~~

Send a simple notification:

.. code-block:: python

   from django_growl import send_notification
   
   send_notification(
       title="Task Complete",
       message="Your data has been processed successfully"
   )

With All Options
~~~~~~~~~~~~~~~~

Use all available options:

.. code-block:: python

   from django_growl import send_notification
   
   send_notification(
       title="User Registration",
       message="New user registered: john@example.com",
       note_type='Info',          # 'Info', 'Error', 'Server Status'
       sticky=True,               # Keep notification visible
       icon='/path/to/icon.png'   # Custom icon
   )

Notification Types
~~~~~~~~~~~~~~~~~~

Three types of notifications are available:

.. code-block:: python

   # Info notification (default)
   send_notification(
       title="Information",
       message="Task completed",
       note_type='Info'
   )
   
   # Error notification
   send_notification(
       title="Error Occurred",
       message="Failed to process data",
       note_type='Error'
   )
   
   # Server status notification
   send_notification(
       title="Server Event",
       message="Configuration reloaded",
       note_type='Server Status'
   )

Programmatic Control
--------------------

Get Notifier Instance
~~~~~~~~~~~~~~~~~~~~~

Access the notifier directly:

.. code-block:: python

   from django_growl import get_growl_notifier
   
   notifier = get_growl_notifier()
   
   # Check if enabled
   if notifier.enabled:
       notifier.notify(
           title="Custom Alert",
           message="Something important happened",
           note_type='Info',
           sticky=False
       )

Check Configuration
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from django_growl import get_growl_notifier
   
   notifier = get_growl_notifier()
   
   print(f"Enabled: {notifier.enabled}")
   print(f"App Name: {notifier.app_name}")
   print(f"Hosts: {notifier.growl_hosts}")
   print(f"Registered: {len(notifier.notifiers)} host(s)")

Conditional Notifications
--------------------------

Based on Environment
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from django.conf import settings
   from django_growl import send_notification
   
   def my_task():
       result = do_something()
       
       # Only notify in development
       if settings.DEBUG:
           send_notification(
               title="Task Result",
               message=f"Processed {result.count} items"
           )

Based on User
~~~~~~~~~~~~~

.. code-block:: python

   def admin_action(request):
       # Process something
       
       # Notify only for staff users
       if request.user.is_staff:
           send_notification(
               title="Admin Action",
               message=f"{request.user.username} performed action"
           )

Integration Examples
--------------------

With Django Views
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from django.shortcuts import render
   from django_growl import send_notification
   
   def generate_report(request):
       # Generate report
       report = Report.objects.create(
           title="Monthly Report",
           data=get_report_data()
       )
       
       # Notify
       send_notification(
           title="Report Generated",
           message=f"Report '{report.title}' is ready",
           sticky=True
       )
       
       return render(request, 'report.html', {
           'report': report
       })

With Celery Tasks
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from celery import shared_task
   from django_growl import send_notification
   
   @shared_task
   def process_large_dataset(dataset_id):
       try:
           # Process data
           result = do_heavy_processing(dataset_id)
           
           # Notify success
           send_notification(
               title="Processing Complete",
               message=f"Dataset {dataset_id}: {result.count} records",
               note_type='Info'
           )
           
       except Exception as e:
           # Notify error
           send_notification(
               title="Processing Failed",
               message=f"Dataset {dataset_id}: {str(e)}",
               note_type='Error',
               sticky=True
           )
           raise

With Management Commands
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from django.core.management.base import BaseCommand
   from django_growl import send_notification
   
   class Command(BaseCommand):
       help = 'Cleanup old data'
       
       def handle(self, *args, **options):
           deleted_count = cleanup_old_data()
           
           send_notification(
               title="Cleanup Complete",
               message=f"Removed {deleted_count} old records"
           )
           
           self.stdout.write(
               self.style.SUCCESS(f'Cleaned up {deleted_count} records')
           )

With Django Signals
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from django.db.models.signals import post_save
   from django.dispatch import receiver
   from django_growl import send_notification
   from .models import Order
   
   @receiver(post_save, sender=Order)
   def order_created(sender, instance, created, **kwargs):
       if created and instance.total > 1000:
           send_notification(
               title="Large Order Created",
               message=f"Order #{instance.id}: ${instance.total}",
               sticky=True
           )

Best Practices
--------------

1. **Use appropriate notification types**
   
   * ``'Info'`` for general notifications
   * ``'Error'`` for errors and failures
   * ``'Server Status'`` for server events

2. **Use sticky notifications wisely**
   
   * Sticky for important errors
   * Non-sticky for routine updates

3. **Don't spam notifications**
   
   * Aggregate similar notifications
   * Use conditions to filter unnecessary alerts

4. **Test in development first**
   
   * Verify notifications work before production
   * Use environment-specific settings

5. **Handle exceptions**
   
   * Notification failures shouldn't break your app
   * The library handles this automatically

Next Steps
----------

* See more examples: :doc:`examples1`
* API reference: :doc:`api/notifier`
* Troubleshooting: :doc:`troubleshooting`
