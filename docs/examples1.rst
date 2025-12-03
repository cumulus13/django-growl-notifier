Examples 1
==========

This page provides practical examples of using Django Growl Notifier in real-world scenarios.

Example 1: View Notifications
------------------------------

Notify when a user completes an action:

.. code-block:: python

   # views.py
   from django.shortcuts import render, redirect
   from django.contrib import messages
   from django_growl import send_notification
   from .models import Report
   from .forms import ReportForm
   
   def create_report(request):
       if request.method == 'POST':
           form = ReportForm(request.POST)
           if form.is_valid():
               report = form.save()
               
               # Send Growl notification
               send_notification(
                   title="Report Created",
                   message=f"Report '{report.title}' created by {request.user.username}",
                   sticky=True
               )
               
               messages.success(request, 'Report created successfully!')
               return redirect('report_detail', pk=report.pk)
       else:
           form = ReportForm()
       
       return render(request, 'create_report.html', {'form': form})

Example 2: Celery Task Monitoring
----------------------------------

Monitor long-running Celery tasks:

.. code-block:: python

   # tasks.py
   from celery import shared_task
   from django_growl import send_notification
   import time
   
   @shared_task
   def export_large_dataset(user_id, dataset_id):
       try:
           # Start notification
           send_notification(
               title="Export Started",
               message=f"Exporting dataset {dataset_id}...",
               note_type='Info'
           )
           
           # Process data (simulation)
           data = Dataset.objects.get(id=dataset_id)
           records = data.export()
           
           # Success notification
           send_notification(
               title="Export Complete",
               message=f"Dataset {dataset_id}: {len(records)} records exported",
               note_type='Info',
               sticky=True
           )
           
           return {'status': 'success', 'count': len(records)}
           
       except Exception as e:
           # Error notification
           send_notification(
               title="Export Failed",
               message=f"Dataset {dataset_id}: {str(e)}",
               note_type='Error',
               sticky=True
           )
           raise

Example 3: Custom Management Command
-------------------------------------

Create a management command with progress notifications:

.. code-block:: python

   # management/commands/sync_data.py
   from django.core.management.base import BaseCommand
   from django_growl import send_notification
   from myapp.models import DataSource
   
   class Command(BaseCommand):
       help = 'Synchronize data from external sources'
       
       def add_arguments(self, parser):
           parser.add_argument(
               '--source',
               type=str,
               help='Specific source to sync',
           )
       
       def handle(self, *args, **options):
           source_name = options.get('source')
           
           if source_name:
               sources = DataSource.objects.filter(name=source_name)
           else:
               sources = DataSource.objects.filter(active=True)
           
           total = sources.count()
           success = 0
           failed = 0
           
           # Start notification
           send_notification(
               title="Data Sync Started",
               message=f"Syncing {total} data source(s)..."
           )
           
           for source in sources:
               try:
                   self.stdout.write(f"Syncing {source.name}...")
                   records = source.sync()
                   success += 1
                   
                   self.stdout.write(
                       self.style.SUCCESS(
                           f"✓ {source.name}: {records} records"
                       )
                   )
               except Exception as e:
                   failed += 1
                   self.stdout.write(
                       self.style.ERROR(f"✗ {source.name}: {e}")
                   )
           
           # Completion notification
           send_notification(
               title="Data Sync Complete",
               message=f"Success: {success}, Failed: {failed}",
               note_type='Error' if failed > 0 else 'Info',
               sticky=failed > 0
           )
           
           self.stdout.write(
               self.style.SUCCESS(
                   f"\nSync complete: {success} succeeded, {failed} failed"
               )
           )

Example 4: Django Admin Actions
--------------------------------

Add notifications to custom admin actions:

.. code-block:: python

   # admin.py
   from django.contrib import admin
   from django.http import HttpResponse
   from django_growl import send_notification
   from .models import Product
   import csv
   
   @admin.register(Product)
   class ProductAdmin(admin.ModelAdmin):
       list_display = ['name', 'price', 'stock', 'active']
       actions = ['export_to_csv', 'mark_inactive']
       
       def export_to_csv(self, request, queryset):
           # Create CSV
           response = HttpResponse(content_type='text/csv')
           response['Content-Disposition'] = 'attachment; filename="products.csv"'
           
           writer = csv.writer(response)
           writer.writerow(['Name', 'Price', 'Stock', 'Active'])
           
           count = 0
           for product in queryset:
               writer.writerow([
                   product.name,
                   product.price,
                   product.stock,
                   product.active
               ])
               count += 1
           
           # Send notification
           send_notification(
               title="Products Exported",
               message=f"{count} products exported to CSV by {request.user.username}",
               sticky=True
           )
           
           self.message_user(request, f"{count} products exported successfully.")
           return response
       
       export_to_csv.short_description = "Export selected to CSV"
       
       def mark_inactive(self, request, queryset):
           updated = queryset.update(active=False)
           
           # Send notification
           send_notification(
               title="Products Deactivated",
               message=f"{updated} products marked as inactive",
               note_type='Info'
           )
           
           self.message_user(request, f"{updated} products marked as inactive.")
       
       mark_inactive.short_description = "Mark selected as inactive"

Example 5: Django Signals
--------------------------

Use signals to trigger notifications:

.. code-block:: python

   # signals.py
   from django.db.models.signals import post_save, pre_delete
   from django.dispatch import receiver
   from django.contrib.auth.models import User
   from django_growl import send_notification
   from .models import Order, Product
   
   @receiver(post_save, sender=Order)
   def notify_new_order(sender, instance, created, **kwargs):
       if created:
           # New order notification
           send_notification(
               title="New Order Received",
               message=f"Order #{instance.id} - ${instance.total} - {instance.customer.email}",
               note_type='Info',
               sticky=instance.total > 500  # Sticky for large orders
           )
   
   @receiver(post_save, sender=User)
   def notify_user_registration(sender, instance, created, **kwargs):
       if created:
           send_notification(
               title="New User Registered",
               message=f"{instance.username} ({instance.email})",
               note_type='Info'
           )
   
   @receiver(pre_delete, sender=Product)
   def notify_product_deletion(sender, instance, **kwargs):
       send_notification(
           title="Product Deleted",
           message=f"Product '{instance.name}' is being deleted",
           note_type='Error',
           sticky=True
       )
   
   # Don't forget to import signals in apps.py:
   # def ready(self):
   #     import myapp.signals

Example 6: REST API Integration
--------------------------------

Notify on API events:

.. code-block:: python

   # api/views.py
   from rest_framework import viewsets, status
   from rest_framework.decorators import action
   from rest_framework.response import Response
   from django_growl import send_notification
   from .models import Task
   from .serializers import TaskSerializer
   
   class TaskViewSet(viewsets.ModelViewSet):
       queryset = Task.objects.all()
       serializer_class = TaskSerializer
       
       def create(self, request, *args, **kwargs):
           response = super().create(request, *args, **kwargs)
           
           if response.status_code == status.HTTP_201_CREATED:
               task = Task.objects.get(id=response.data['id'])
               send_notification(
                   title="Task Created via API",
                   message=f"Task: {task.title} by {request.user.username}"
               )
           
           return response
       
       @action(detail=True, methods=['post'])
       def complete(self, request, pk=None):
           task = self.get_object()
           task.status = 'completed'
           task.save()
           
           send_notification(
               title="Task Completed",
               message=f"Task '{task.title}' marked as complete",
               note_type='Info',
               sticky=True
           )
           
           return Response({'status': 'task completed'})

Example 7: Scheduled Tasks (Cron)
----------------------------------

Notify on scheduled task execution:

.. code-block:: python

   # cron.py (using django-crontab or similar)
   from django_growl import send_notification
   from django.core.management import call_command
   from datetime import datetime
   
   def daily_backup():
       try:
           # Start notification
           send_notification(
               title="Backup Started",
               message=f"Daily backup started at {datetime.now()}"
           )
           
           # Perform backup
           call_command('dbbackup')
           call_command('mediabackup')
           
           # Success notification
           send_notification(
               title="Backup Complete",
               message="Database and media backup completed successfully",
               sticky=True
           )
           
       except Exception as e:
           # Error notification
           send_notification(
               title="Backup Failed",
               message=f"Backup error: {str(e)}",
               note_type='Error',
               sticky=True
           )
           raise

Example 8: Conditional Notifications
-------------------------------------

Send notifications based on conditions:

.. code-block:: python

   # utils.py
   from django.conf import settings
   from django_growl import send_notification
   
   def notify_if_important(title, message, importance='normal'):
       '''Only notify for important events'''
       if importance == 'high':
           send_notification(
               title=title,
               message=message,
               sticky=True
           )
       elif importance == 'normal' and settings.DEBUG:
           # Only in development for normal importance
           send_notification(
               title=title,
               message=message,
               sticky=False
           )
       # Skip 'low' importance notifications
   
   def notify_admin_only(request, title, message):
       '''Only notify for admin users'''
       if request.user.is_staff or request.user.is_superuser:
           send_notification(
               title=f"[ADMIN] {title}",
               message=message,
               sticky=True
           )
   
   # Usage
   notify_if_important(
       "Critical Error",
       "Database connection lost",
       importance='high'
   )

Example 9: Progress Monitoring
-------------------------------

Monitor long-running operations:

.. code-block:: python

   # processors.py
   from django_growl import send_notification
   from .models import LargeDataset
   
   def process_large_dataset(dataset_id):
       dataset = LargeDataset.objects.get(id=dataset_id)
       total_items = dataset.items.count()
       
       # Start notification
       send_notification(
           title="Processing Started",
           message=f"Processing {total_items} items..."
       )
       
       processed = 0
       errors = []
       
       for item in dataset.items.all():
           try:
               process_item(item)
               processed += 1
               
               # Progress notification every 100 items
               if processed % 100 == 0:
                   send_notification(
                       title="Processing Progress",
                       message=f"{processed}/{total_items} items processed"
                   )
           except Exception as e:
               errors.append(f"{item.id}: {str(e)}")
       
       # Final notification
       if errors:
           send_notification(
               title="Processing Complete with Errors",
               message=f"Processed: {processed}, Errors: {len(errors)}",
               note_type='Error',
               sticky=True
           )
       else:
           send_notification(
               title="Processing Complete",
               message=f"All {processed} items processed successfully",
               note_type='Info',
               sticky=True
           )

Example 10: Multi-Environment Setup
------------------------------------

Different notification behavior per environment:

.. code-block:: python

   # settings/base.py
   GROWL_APP_NAME = 'My Django App'
   GROWL_ENABLED = True
   
   # settings/development.py
   from .base import *
   
   GROWL_HOSTS = ['127.0.0.1:23053']
   GROWL_STICKY_SERVER = False
   GROWL_NOTIFY_ERRORS = True
   
   # settings/staging.py
   from .base import *
   
   GROWL_HOSTS = ['staging-monitor.local:23053']
   GROWL_APP_NAME = 'My App [STAGING]'
   GROWL_STICKY_SERVER = True
   GROWL_NOTIFY_ERRORS = True
   
   # settings/production.py
   from .base import *
   
   # Disable in production, or only for critical errors
   GROWL_ENABLED = False
   
   # Or notify only critical production server
   # GROWL_HOSTS = ['prod-monitor.internal:23053']
   # GROWL_NOTIFY_ERRORS = True
   # GROWL_STICKY_ERRORS = True

More Examples
-------------

For more examples and use cases, check out:

* :doc:`usage` - General usage patterns
* :doc:`api/notifier` - API reference
* `GitHub Repository Examples <https://github.com/cumulus13/django-growl-notifier/tree/main/examples>`_