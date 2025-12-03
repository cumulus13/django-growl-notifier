from django.core.management.commands.runserver import Command as RunserverCommand
from django.conf import settings
from django_growl import send_notification
import django


class Command(RunserverCommand):
    help = 'Starts Django development server with Growl notifications.'
    
    def inner_run(self, *args, **options):
        # Send notification when server starts
        try:
            django_version = django.get_version()
            settings_module = settings.SETTINGS_MODULE
            
            # Parse address
            if options.get('addrport'):
                addr = options['addrport']
            else:
                addr = f"{self.addr}:{self.port}"
            
            message = (
                f"Django version {django_version}\n"
                f"Settings: {settings_module}\n"
                f"Starting server at http://{addr}/"
            )
            
            sticky = getattr(settings, 'GROWL_STICKY_SERVER', False)
            
            send_notification(
                title="Django Server Started",
                message=message,
                note_type='Server Status',
                sticky=sticky
            )
            
            growl_hosts = getattr(settings, 'GROWL_HOSTS', [])
            self.stdout.write(
                self.style.SUCCESS(
                    f"✓ Growl notification sent to {len(growl_hosts)} host(s)"
                )
            )
            
        except Exception as e:
            self.stderr.write(
                self.style.WARNING(f"Failed to send Growl notification: {e}")
            )
        
        # Run the normal runserver
        return super().inner_run(*args, **options)
        