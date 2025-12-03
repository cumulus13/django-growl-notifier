from django.apps import AppConfig
import sys


class DjangoGrowlConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_growl'
    verbose_name = 'Django Growl Notifier'
    
    def ready(self):
        # Only run on runserver and not on reload
        if 'runserver' in sys.argv and not hasattr(self.__class__, '_notified'):
            from django.conf import settings
            from .notifier import send_notification
            import django
            
            # Check whether Growl is enabled
            if not getattr(settings, 'GROWL_ENABLED', True):
                return
            
            # Mark as notified to avoid duplicates
            self.__class__._notified = True
            
            try:
                django_version = django.get_version()
                settings_module = settings.SETTINGS_MODULE
                
                # Find the address and port from argv
                addr = '127.0.0.1:8000'  # default
                for i, arg in enumerate(sys.argv):
                    if arg == 'runserver' and i + 1 < len(sys.argv):
                        next_arg = sys.argv[i + 1]
                        if ':' in next_arg or next_arg.replace('.', '').isdigit():
                            addr = next_arg if ':' in next_arg else f'127.0.0.1:{next_arg}'
                            break
                
                message = (
                    f"Django version {django_version}\n"
                    f"Settings: {settings_module}\n"
                    f"Server at http://{addr}/"
                )
                
                sticky = getattr(settings, 'GROWL_STICKY_SERVER', False)
                
                send_notification(
                    title="Django Server Started",
                    message=message,
                    sticky=sticky
                )
            except Exception as e:
                # Don't crash the app if notification fails
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"Growl notification failed: {e}")