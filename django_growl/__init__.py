from .notifier import send_notification, get_growl_notifier
from version_get import VersionGet as vget

__version__ = vget().get(True)
__all__ = ['send_notification', 'get_growl_notifier']
