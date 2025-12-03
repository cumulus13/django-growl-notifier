from django.conf import settings
from .notifier import send_notification
import traceback
import logging

logger = logging.getLogger(__name__)


class GrowlErrorMiddleware:
    '''Middleware to send error notifications to Growl'''
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.notify_errors = getattr(settings, 'GROWL_NOTIFY_ERRORS', True)
        self.sticky_errors = getattr(settings, 'GROWL_STICKY_ERRORS', True)
    
    def __call__(self, request):
        return self.get_response(request)
    
    def process_exception(self, request, exception):
        if not self.notify_errors:
            return None
        
        try:
            error_trace = ''.join(traceback.format_exception(
                type(exception),
                exception,
                exception.__traceback__
            ))
            
            # Limit traceback length for Growl
            if len(error_trace) > 500:
                error_trace = error_trace[:500] + "\n... (truncated)"
            
            message = (
                f"Error: {str(exception)}\n"
                f"Path: {request.path}\n"
                f"Method: {request.method}\n"
                f"\nTraceback:\n{error_trace}"
            )
            
            send_notification(
                title=f"Django Error: {type(exception).__name__}",
                message=message,
                note_type='Error',
                sticky=self.sticky_errors
            )
        except Exception as e:
            logger.error(f"Failed to send error notification: {e}")
        
        return None
        