Examples 2
==========

This page provides practical examples of using Django Growl Notifier.

Basic Examples
--------------

Simple Notification
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from django_growl import send_notification
   
   send_notification(
       title="Hello",
       message="This is a test notification"
   )

With Custom Icon
~~~~~~~~~~~~~~~~

.. code-block:: python

   from django_growl import send_notification
   
   send_notification(
       title="Custom Icon",
       message="This notification has a custom icon",
       icon="/path/to/custom-icon.png"
   )

Sticky Notification
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from django_growl import send_notification
   
   send_notification(
       title="Important",
       message="This will stay visible until dismissed",
       sticky=True
   )

Django Integration
------------------

In Views
~~~~~~~~

**Example 1: Simple View Notification**

.. code-block:: python

   from django.shortcuts import render, redirect
   from django_growl import send_notification
   from .forms import ContactForm
   
   def contact_view(request):
       if request.method == 'POST':
           form = ContactForm(request.POST)
           if form.is_valid():
               form.save()
               
               send_notification(
                   title="New Contact Form",
                   message=f"From: {form.cleaned_data['email']}"
               )
               
               return redirect('thank_you')
       else:
           form = ContactForm()
       
       return render(request, 'contact.html', {'form': form})

**Example 2: File Upload Notification**

.. code-block:: python

   from django.views.generic import CreateView
   from django_growl import send_notification
   from .models import Document
   
   class DocumentUploadView(CreateView):
       model = Document
       fields = ['title', 'file']
       
       def form_valid(self, form):
           response = super().form_valid(form)
           
           send_notification(
               title="Document Uploaded",
               message=f"{self.object.title} ({self.object.file.size} bytes)",
               sticky=True
           )
           
           return response

**Example 3: Bulk Action Notification**

.. code-block:: python

   from django.contrib import messages
   from django.shortcuts import render, redirect
   from django_growl import send_notification
   from .models import Product
   
   def bulk_update_prices(request):
       if request.method == 'POST':
           selected_ids = request.POST.getlist('selected')
           increase_percent = int(request.POST.get('increase', 0))
           
           products = Product.objects.filter(id__in=selected_ids)
           count = products.update(
               price=F('price') * (1 + increase_percent / 100)
           )
           
           send_notification(
               title="Prices Updated",
               message=f"Updated {count} products by {increase_percent}%",
               note_type='Info'
           )
           
           messages.success(request, f"Updated {count} products")
           return redirect('product_list')
       
       return render(request, 'bulk_update.html')

With Celery
~~~~~~~~~~~

**Example 1: Long Running Task**

.. code-block:: python

   from celery import shared_task
   from django_growl import send_notification
   import time
   
   @shared_task
   def process_video(video_id):
       try:
           video = Video.objects.get(id=video_id)
           
           # Notify start
           send_notification(
               title="Video Processing Started",
               message=f"Processing: {video.title}"
           )
           
           # Process video (long operation)
           result = encode_video(video)
           
           # Notify completion
           send_notification(
               title="Video Processing Complete",
               message=f"{video.title} - Duration: {result.duration}s",
               sticky=True
           )
           
           return result
           
       except Exception as e:
           send_notification(
               title="Video Processing Failed",
               message=f"Error: {str(e)}",
               note_type='Error',
               sticky=True
           )
           raise

**Example 2: Scheduled Task**

.. code-block:: python

   from celery import shared_task
   from django_growl import send_notification
   from django.utils import timezone
   from .models import Backup
   
   @shared_task
   def daily_backup():
       try:
           backup = Backup.objects.create(
               timestamp=timezone.now()
           )
           
           # Perform backup
           files_backed_up = backup.execute()
           
           send_notification(
               title="Daily Backup Complete",
               message=f"Backed up {files_backed_up} files at {backup.timestamp}",
               note_type='Info'
           )
           
       except Exception as e:
           send_notification(
               title="Backup Failed",
               message=f"Daily backup error: {str(e)}",
               note_type='Error',
               sticky=True
           )

**Example 3: Chain of Tasks**

.. code-block:: python

   from celery import chain, shared_task
   from django_growl import send_notification
   
   @shared_task
   def fetch_data():
       data = external_api.fetch()
       send_notification("Data Fetched", f"Got {len(data)} records")
       return data
   
   @shared_task
   def process_data(data):
       processed = transform(data)
       send_notification("Data Processed", f"Processed {len(processed)} records")
       return processed
   
   @shared_task
   def save_data(processed):
       Model.objects.bulk_create(processed)
       send_notification(
           "Data Saved",
           f"Saved {len(processed)} records",
           sticky=True
       )
   
   # Run chain
   workflow = chain(fetch_data.s(), process_data.s(), save_data.s())
   workflow.apply_async()

Management Commands
~~~~~~~~~~~~~~~~~~~

**Example 1: Data Cleanup Command**

.. code-block:: python

   from django.core.management.base import BaseCommand
   from django.utils import timezone
   from django_growl import send_notification
   from datetime import timedelta
   
   class Command(BaseCommand):
       help = 'Clean up old data'
       
       def add_arguments(self, parser):
           parser.add_argument(
               '--days',
               type=int,
               default=30,
               help='Days to keep'
           )
       
       def handle(self, *args, **options):
           days = options['days']
           cutoff = timezone.now() - timedelta(days=days)
           
           # Delete old records
           deleted = OldData.objects.filter(
               created_at__lt=cutoff
           ).delete()
           
           count = deleted[0]
           
           send_notification(
               title="Cleanup Complete",
               message=f"Removed {count} records older than {days} days"
           )
           
           self.stdout.write(
               self.style.SUCCESS(f'Deleted {count} records')
           )

**Example 2: Import Command**

.. code-block:: python

   from django.core.management.base import BaseCommand
   from django_growl import send_notification
   import csv
   
   class Command(BaseCommand):
       help = 'Import data from CSV'
       
       def add_arguments(self, parser):
           parser.add_argument('csv_file', type=str)
       
       def handle(self, *args, **options):
           csv_file = options['csv_file']
           
           try:
               with open(csv_file, 'r') as f:
                   reader = csv.DictReader(f)
                   records = [Record(**row) for row in reader]
                   
               Record.objects.bulk_create(records)
               
               send_notification(
                   title="Import Complete",
                   message=f"Imported {len(records)} records from {csv_file}",
                   sticky=True
               )
               
               self.stdout.write(
                   self.style.SUCCESS(f'Imported {len(records)} records')
               )
               
           except Exception as e:
               send_notification(
                   title="Import Failed",
                   message=str(e),
                   note_type='Error',
                   sticky=True
               )
               raise

Django Admin
~~~~~~~~~~~~

**Example 1: Custom Admin Action**

.. code-block:: python

   from django.contrib import admin
   from django_growl import send_notification
   
   @admin.register(Product)
   class ProductAdmin(admin.ModelAdmin):
       list_display = ['name', 'price', 'stock']
       actions = ['mark_as_featured', 'export_to_csv']
       
       def mark_as_featured(self, request, queryset):
           count = queryset.update(featured=True)
           
           send_notification(
               title="Products Featured",
               message=f"Marked {count} products as featured",
               sticky=True
           )
           
           self.message_user(
               request,
               f"{count} products marked as featured"
           )
       
       mark_as_featured.short_description = "Mark as featured"
       
       def export_to_csv(self, request, queryset):
           # Export logic
           filename = export_products_to_csv(queryset)
           
           send_notification(
               title="Export Complete",
               message=f"Exported to {filename}"
           )

**Example 2: ModelAdmin Save Notification**

.. code-block:: python

   from django.contrib import admin
   from django_growl import send_notification
   
   @admin.register(Order)
   class OrderAdmin(admin.ModelAdmin):
       def save_model(self, request, obj, form, change):
           super().save_model(request, obj, form, change)
           
           if not change:  # New order
               send_notification(
                   title="New Order Created",
                   message=f"Order #{obj.id} - ${obj.total}",
                   sticky=True
               )
           elif 'status' in form.changed_data:
               send_notification(
                   title="Order Status Changed",
                   message=f"Order #{obj.id} → {obj.get_status_display()}"
               )

Django Signals
~~~~~~~~~~~~~~

**Example 1: Post-Save Signal**

.. code-block:: python

   from django.db.models.signals import post_save
   from django.dispatch import receiver
   from django_growl import send_notification
   from .models import Order
   
   @receiver(post_save, sender=Order)
   def order_notification(sender, instance, created, **kwargs):
       if created:
           if instance.total > 1000:
               send_notification(
                   title="High Value Order",
                   message=f"Order #{instance.id}: ${instance.total}",
                   sticky=True
               )
       else:
           if instance.status == 'shipped':
               send_notification(
                   title="Order Shipped",
                   message=f"Order #{instance.id} has been shipped"
               )

**Example 2: Pre-Delete Signal**

.. code-block:: python

   from django.db.models.signals import pre_delete
   from django.dispatch import receiver
   from django_growl import send_notification
   from .models import ImportantDocument
   
   @receiver(pre_delete, sender=ImportantDocument)
   def document_deletion_warning(sender, instance, **kwargs):
       send_notification(
           title="Document Being Deleted",
           message=f"Warning: {instance.title} is being deleted",
           note_type='Error',
           sticky=True
       )

**Example 3: User Login Signal**

.. code-block:: python

   from django.contrib.auth.signals import user_logged_in
   from django.dispatch import receiver
   from django_growl import send_notification
   
   @receiver(user_logged_in)
   def user_login_notification(sender, request, user, **kwargs):
       if user.is_staff:
           send_notification(
               title="Staff Login",
               message=f"{user.username} logged in from {request.META.get('REMOTE_ADDR')}"
           )

Advanced Examples
-----------------

Conditional Notifications
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from django.conf import settings
   from django_growl import send_notification
   
   def notify_if_important(title, message, condition):
       """Only send notification if condition is met"""
       if condition and settings.DEBUG:
           send_notification(title, message, sticky=True)
   
   # Usage
   notify_if_important(
       "Database Query",
       f"Slow query: {query.execution_time}s",
       condition=query.execution_time > 5.0
   )

Rate-Limited Notifications
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from django.core.cache import cache
   from django_growl import send_notification
   import hashlib
   
   def rate_limited_notification(title, message, seconds=60):
       """Prevent duplicate notifications within time window"""
       key = f"growl_{hashlib.md5(f'{title}{message}'.encode()).hexdigest()}"
       
       if not cache.get(key):
           send_notification(title, message)
           cache.set(key, True, seconds)
   
   # Usage - will only notify once per minute
   rate_limited_notification(
       "API Error",
       "External API is down",
       seconds=60
   )

Notification Queue
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from collections import deque
   from django_growl import send_notification
   
   class NotificationQueue:
       def __init__(self, max_size=10):
           self.queue = deque(maxlen=max_size)
       
       def add(self, title, message):
           self.queue.append((title, message))
       
       def flush(self):
           """Send all queued notifications"""
           while self.queue:
               title, message = self.queue.popleft()
               send_notification(title, message)
   
   # Usage
   queue = NotificationQueue()
   queue.add("Task 1", "Complete")
   queue.add("Task 2", "Complete")
   queue.flush()  # Send all at once

Testing Examples
----------------

Unit Testing with Notifications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from django.test import TestCase
   from unittest.mock import patch
   from myapp.views import my_view
   
   class NotificationTestCase(TestCase):
       @patch('django_growl.send_notification')
       def test_notification_sent(self, mock_notify):
           # Test your code
           response = self.client.post('/action/')
           
           # Verify notification was sent
           mock_notify.assert_called_once()
           call_args = mock_notify.call_args
           self.assertEqual(call_args[1]['title'], "Action Complete")

Integration Testing
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from django.test import TestCase
   from django_growl import get_growl_notifier
   
   class GrowlIntegrationTest(TestCase):
       def test_notifier_configured(self):
           notifier = get_growl_notifier()
           self.assertTrue(notifier.enabled)
           self.assertGreater(len(notifier.growl_hosts), 0)

More Examples
-------------

For more examples, check out:

* `GitHub Examples <https://github.com/cumulus13/django-growl-notifier/tree/main/examples>`_
* :doc:`usage` - Usage guide
* :doc:`api/notifier` - API reference