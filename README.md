# Django Growl Notifier

[![PyPI version](https://badge.fury.io/py/django-growl-notifier.svg)](https://badge.fury.io/py/django-growl-notifier)
[![Python Versions](https://img.shields.io/pypi/pyversions/django-growl-notifier.svg)](https://pypi.org/project/django-growl-notifier/)
[![Django Versions](https://img.shields.io/badge/django-3.2%20%7C%204.0%20%7C%205.0-blue.svg)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://django-growl-notifier.readthedocs.io/)

<p align="center">
  <img src="https://raw.githubusercontent.com/cumulus13/django-growl-notifier/master/django_growl/icon.png" alt="Logo" width="320">
</p>


Send Django development server notifications to Growl (or compatible notification systems like Growl for Windows, Snarl, or prowlnotify).

## ✨ Features

- 🚀 **Automatic notifications** when Django server starts
- 🔥 **Error notifications** with detailed stacktrace
- 🌐 **Multiple Growl hosts** support - broadcast to multiple machines
- 🎨 **Custom icons** support for notifications
- ⚙️ **Easy configuration** - minimal setup required
- 🎯 **Manual notifications** - trigger notifications anywhere in your code
- 🔇 **Silent mode** - disable notifications when needed
- 📝 **Detailed logging** - track notification delivery

## 📦 Installation

### Via pip

```bash
pip install django-growl-notifier
```

### From source

```bash
git clone https://github.com/cumulus13/django-growl-notifier.git
cd django-growl-notifier
pip install -e .
```

## 🚀 Quick Setup

### 1. Add to INSTALLED_APPS

Add `django_growl` to your `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    # ... your other apps
    'django_growl',
]
```

### 2. Configure Growl Hosts

Add Growl configuration to your `settings.py`:

```python
# Required: List of Growl hosts (IP:PORT or just IP)
GROWL_HOSTS = [
    '127.0.0.1:23053',        # Local machine
    '192.168.1.100:23053',    # Remote machine on network
]

# Optional settings
GROWL_APP_NAME = 'My Django App'  # Default: 'Django Server'
GROWL_ENABLED = True              # Default: True
```

### 3. Run Your Server

```bash
# Option 1: Use regular runserver (with auto-notify)
python manage.py runserver

# Option 2: Use custom command with explicit notification
python manage.py runserver_growl

# Option 3: Specify address and port
python manage.py runserver 0.0.0.0:8000
```

You'll see a Growl notification when the server starts! 🎉

## ⚙️ Configuration

### All Available Settings

```python
# settings.py

# ============================================
# REQUIRED SETTINGS
# ============================================

# List of Growl notification hosts
# Format: 'IP:PORT' or 'IP' (defaults to port 23053)
GROWL_HOSTS = [
    '127.0.0.1:23053',
    '192.168.1.50',  # Will use port 23053
]

# ============================================
# OPTIONAL SETTINGS
# ============================================

# Application name displayed in Growl
GROWL_APP_NAME = 'Django Server'  # Default

# Enable or disable all notifications
GROWL_ENABLED = True  # Default

# Custom icon for notifications
# Supports: file path, file:// URI, or http(s):// URL
GROWL_ICON = '/path/to/your/icon.png'

# Enable error notifications via middleware
GROWL_NOTIFY_ERRORS = True  # Default

# Make error notifications sticky (stay visible)
GROWL_STICKY_ERRORS = True  # Default

# Make server start notifications sticky
GROWL_STICKY_SERVER = False  # Default
```

### Icon Configuration

Django Growl Notifier supports custom icons for notifications:

```python
# Use a local file
GROWL_ICON = '/path/to/django-logo.png'

# Use file URI
GROWL_ICON = 'file:///path/to/icon.png'

# Use HTTP URL (if Growl supports it)
GROWL_ICON = 'https://example.com/icon.png'
```

**Icon Priority:**
1. Parameter passed to `send_notification(icon=...)`
2. `GROWL_ICON` environment variable
3. `GROWL_ICON` in settings.py
4. Default `icon.png` in package directory

## 📖 Usage

### Automatic Server Start Notifications

Notifications are sent automatically when you start the Django development server:

```bash
$ python manage.py runserver
System check identified no issues (0 silenced).
December 03, 2025 - 11:35:30
Django version 5.2.8, using settings 'myproject.settings'
Starting development server at http://127.0.0.1:8000/
✓ Growl notification sent to 2 host(s)
Quit the server with CONTROL-C.
```

### Error Notifications with Middleware

Get notified automatically when errors occur in your Django application.

**Setup:**

Add the middleware to your `settings.py`:

```python
MIDDLEWARE = [
    # ... your other middleware
    'django_growl.middleware.GrowlErrorMiddleware',
]

# Optional: Configure error notification behavior
GROWL_NOTIFY_ERRORS = True      # Enable error notifications
GROWL_STICKY_ERRORS = True      # Make error notifications sticky
```

**What you get:**
- Automatic notifications on 500 errors
- Full exception details and stacktrace
- Request path and HTTP method
- Sticky notifications (so you don't miss them)

### Manual Notifications

Send custom notifications from anywhere in your Django code:

```python
from django_growl import send_notification

# Basic notification
send_notification(
    title="Task Complete",
    message="Database backup finished successfully"
)

# With all options
send_notification(
    title="User Registration",
    message="New user: john@example.com",
    note_type='Info',          # 'Info', 'Error', or 'Server Status'
    sticky=True,               # Keep notification visible
    icon='/path/to/icon.png'   # Custom icon for this notification
)
```

**Use Cases:**
- Celery task completion
- Scheduled job notifications
- Custom admin actions
- Database migrations
- Deployment scripts

### Programmatic Control

```python
from django_growl import get_growl_notifier

# Get the notifier instance
notifier = get_growl_notifier()

# Check if enabled
if notifier.enabled:
    notifier.notify(
        title="Custom Alert",
        message="Something important happened",
        note_type='Info',
        sticky=False
    )
```

## 🎨 Examples

### Example 1: Task Completion in Views

```python
from django.shortcuts import render
from django_growl import send_notification
from .models import Report

def generate_report(request):
    # Generate report
    report = Report.objects.create(...)
    
    # Notify via Growl
    send_notification(
        title="Report Generated",
        message=f"Report #{report.id} is ready for download",
        sticky=True
    )
    
    return render(request, 'report.html', {'report': report})
```

### Example 2: Celery Task Notification

```python
from celery import shared_task
from django_growl import send_notification

@shared_task
def process_large_dataset(dataset_id):
    # Process data...
    result = do_processing(dataset_id)
    
    # Notify when complete
    send_notification(
        title="Processing Complete",
        message=f"Dataset {dataset_id} processed: {result.count} records",
        note_type='Info'
    )
    
    return result
```

### Example 3: Management Command

```python
from django.core.management.base import BaseCommand
from django_growl import send_notification

class Command(BaseCommand):
    help = 'Cleanup old data'
    
    def handle(self, *args, **options):
        # Cleanup logic
        deleted_count = cleanup_old_data()
        
        # Notify
        send_notification(
            title="Cleanup Complete",
            message=f"Removed {deleted_count} old records"
        )
        
        self.stdout.write(self.style.SUCCESS('Done!'))
```

### Example 4: Custom Admin Action

```python
from django.contrib import admin
from django_growl import send_notification

@admin.register(MyModel)
class MyModelAdmin(admin.ModelAdmin):
    actions = ['export_selected']
    
    def export_selected(self, request, queryset):
        count = queryset.count()
        # Export logic...
        
        send_notification(
            title="Export Complete",
            message=f"Exported {count} items",
            sticky=True
        )
        
        self.message_user(request, f"Exported {count} items")
    
    export_selected.short_description = "Export selected items"
```

## 🔧 Troubleshooting

### Notifications Not Appearing

1. **Check if Growl is running:**
   ```bash
   # Windows: Check Task Manager for Growl.exe
   # Mac: Check if Growl is running in menu bar
   ```

2. **Verify network connectivity:**
   ```bash
   # Test if port is open
   telnet 192.168.1.100 23053
   ```

3. **Check Django logs:**
   ```python
   # settings.py - Enable debug logging
   LOGGING = {
       'version': 1,
       'handlers': {
           'console': {'class': 'logging.StreamHandler'},
       },
       'loggers': {
           'django_growl': {
               'handlers': ['console'],
               'level': 'DEBUG',
           },
       },
   }
   ```

4. **Verify settings:**
   ```python
   # In Django shell
   from django.conf import settings
   print(settings.GROWL_HOSTS)
   print(settings.GROWL_ENABLED)
   ```

### Common Issues

**Issue:** "Failed to register Growl notifier"
- **Solution:** Check if Growl is accepting network notifications. Enable "Listen for incoming notifications" in Growl settings.

**Issue:** Notifications work locally but not on remote hosts
- **Solution:** Check firewall settings. Port 23053 must be open on remote machines.

**Issue:** Icons not showing
- **Solution:** Verify icon path exists and is accessible. Use absolute paths or URIs.

**Issue:** Too many notifications during development
- **Solution:** Temporarily disable:
  ```python
  GROWL_ENABLED = False
  ```

## 🔍 Advanced Usage

### Environment Variable Override

You can override settings using environment variables:

```bash
# Disable notifications temporarily
export GROWL_ENABLED=false
python manage.py runserver

# Use custom icon
export GROWL_ICON=/path/to/custom-icon.png
python manage.py runserver
```

### Multiple Notification Types

```python
from django_growl import send_notification

# Info notification (default)
send_notification("Task Done", "Completed successfully", note_type='Info')

# Error notification
send_notification("Task Failed", "Error occurred", note_type='Error')

# Server status notification
send_notification("Server Event", "Config reloaded", note_type='Server Status')
```

### Conditional Notifications

```python
from django.conf import settings
from django_growl import send_notification

def my_view(request):
    # Only notify in development
    if settings.DEBUG:
        send_notification("Debug", "View accessed")
    
    # Only notify for specific users
    if request.user.is_staff:
        send_notification("Admin Action", f"{request.user} performed action")
```

## 🧪 Testing

```bash
# Install dev dependencies
pip install -e .[dev]

# Run tests
python -m pytest

# With coverage
python -m pytest --cov=django_growl
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📋 Requirements

- Python >= 3.8
- Django >= 3.2
- gntp >= 1.0.3
- version_get
- Growl for Windows, Growl (macOS), or compatible notification system use GNTP 

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Hadi Cahyadi**
- Email: [cumulus13@gmail.com](mailto:cumulus13@gmail.com)
- GitHub: [@cumulus13](https://github.com/cumulus13)

## 💖 Support

If you find this project helpful, please consider supporting:

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/cumulus13)
[![Donate via Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/cumulus13)
[![Support on Patreon](https://img.shields.io/badge/Patreon-Support-red.svg)](https://www.patreon.com/cumulus13)

## 🙏 Acknowledgments

- Thanks to the [Growl](https://growl.github.io/growl/) team for the notification system
- Thanks to the Django community for the excellent web framework
- Built with ❤️ by developers, for developers

## 📚 Related Projects

- [gntp](https://github.com/kfdm/gntp) - Growl Notification Transport Protocol library
- [django-notifications](https://github.com/django-notifications/django-notifications) - Generic notification system for Django
- [Growl for Windows](http://www.growlforwindows.com/) - Windows implementation of Growl

---

**Star ⭐ this repo if you find it useful!**