# Django Growl Notifier

Send Django development server notifications to Growl (or compatible notification systems).

## Features

- 🚀 Automatic notifications when Django server starts
- 🔥 Error notifications with stacktrace
- 🌐 Multiple Growl hosts support
- ⚙️ Easy configuration
- 🎯 Custom notifications in your code

## Installation

```bash
pip install django-growl-notifier
```

## Quick Setup

1. Add to `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    # ... your apps
    'django_growl',
]
```

2. Configure Growl hosts in `settings.py`:

```python
GROWL_HOSTS = [
    '127.0.0.1:23053',
    '192.168.1.100:23053',
]

GROWL_APP_NAME = 'My Django App'  # Optional
GROWL_ENABLED = True  # Optional, default True
```

3. Run server with Growl notifications:

```bash
python manage.py runserver_growl
```

Or use regular runserver with auto-notify:

```bash
python manage.py runserver
```

## Configuration

### Available Settings

```python
# Required: List of Growl hosts
GROWL_HOSTS = ['127.0.0.1:23053']

# Optional: Application name shown in Growl
GROWL_APP_NAME = 'Django Server'

# Optional: Enable/disable notifications
GROWL_ENABLED = True

# Optional: Enable error notifications
GROWL_NOTIFY_ERRORS = True

# Optional: Sticky notifications
GROWL_STICKY_ERRORS = True
GROWL_STICKY_SERVER = False
```

## Usage

### Automatic Notifications

Server start notifications are sent automatically when you run the server.

### Error Notifications

Add middleware to `settings.py`:

```python
MIDDLEWARE = [
    # ... other middleware
    'django_growl.middleware.GrowlErrorMiddleware',
]
```

### Manual Notifications

```python
from django_growl import send_notification

send_notification(
    title="Task Complete",
    message="Database backup finished successfully",
    sticky=False
)
```

## Requirements

- Python >= 3.8
- Django >= 3.2
- gntp >= 1.0.3
- Growl or compatible notification system

## License

(MIT License)[LICENSE]

## author
[Hadi Cahyadi](mailto:cumulus13@gmail.com)
    

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/cumulus13)

[![Donate via Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/cumulus13)
 
[Support me on Patreon](https://www.patreon.com/cumulus13)

