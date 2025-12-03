#!/usr/bin/env python3
# File: django_growl/notifier.py
# Author: Hadi Cahyadi <cumulus13@gmail.com>
# Date: 2025-12-03
# Description: 
# License: MIT

import gntp.notifier
from django.conf import settings
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


class GrowlNotifier:
    def __init__(self):
        self.growl_hosts = getattr(settings, 'GROWL_HOSTS', [])
        
        # Setup default icon
        default_icon_path = Path(__file__).parent / 'icon.png'
        
        # Check the icon from settings or use the default
        custom_icon = getattr(settings, 'GROWL_ICON', None)
        
        if custom_icon and Path(custom_icon).is_file():
            self.icon = Path(custom_icon).as_uri()
        elif default_icon_path.is_file():
            self.icon = default_icon_path.as_uri()
        else:
            self.icon = None  # No icon available
            
        self.app_name = getattr(settings, 'GROWL_APP_NAME', 'Django Server')
        self.enabled = getattr(settings, 'GROWL_ENABLED', True)
        self.notifiers = []
        
        if not self.enabled:
            logger.info("Growl notifications are disabled")
            return
        
        if not self.growl_hosts:
            logger.warning("GROWL_HOSTS is not configured in settings.py")
            return
        
        # Initialize notifiers for each host
        for host_config in self.growl_hosts:
            try:
                if ':' in str(host_config):
                    host, port = str(host_config).split(':')
                    port = int(port)
                else:
                    host = str(host_config)
                    port = 23053  # default Growl port
                
                notifier = gntp.notifier.GrowlNotifier(
                    applicationName=self.app_name,
                    notifications=['Server Status', 'Error', 'Info'],
                    defaultNotifications=['Server Status', 'Error', 'Info'],
                    hostname=host,
                    port=port
                )
                
                # Register with Growl
                notifier.register()
                self.notifiers.append({
                    'notifier': notifier,
                    'host': host,
                    'port': port
                })
                logger.info(f"Growl notifier registered for {host}:{port}")
                
            except Exception as e:
                logger.error(f"Failed to register Growl notifier for {host_config}: {e}")
    
    def notify(self, title, message, note_type='Info', sticky=False, icon=None):
        """Send notification to all Growl hosts"""
        if not self.enabled:
            return
        
        # Use the given or default icon of the instance
        notification_icon = icon or self.icon
        
        success_count = 0
        for item in self.notifiers:
            try:
                kwargs = {
                    'noteType': note_type,
                    'title': title,
                    'description': message,
                    'sticky': sticky,
                }
                
                # Add icon if available
                if notification_icon:
                    kwargs['icon'] = notification_icon
                
                item['notifier'].notify(**kwargs)
                success_count += 1
                logger.debug(f"Notification sent to {item['host']}:{item['port']}")
            except Exception as e:
                logger.error(f"Failed to send notification to {item['host']}:{item['port']}: {e}")
        
        if success_count > 0:
            logger.info(f"Notification sent to {success_count}/{len(self.notifiers)} host(s)")


# Singleton instance
_growl_notifier = None


def get_growl_notifier():
    global _growl_notifier
    if _growl_notifier is None:
        _growl_notifier = GrowlNotifier()
    return _growl_notifier


def send_notification(title, message, note_type='Info', sticky=False, icon=None):
    '''Helper function to send notifications
    
    Args:
        title: Notification title
        message: Message content
        note_type: Notification type ('Info', 'Error', 'Server Status')
        sticky: Whether the notification stays visible (True/False)
        icon: Icon file path or URI (file://, http[s]://)
    '''
    notifier = get_growl_notifier()
    
    # Cek icon priority: parameter > env > default
    if icon is None:
        # Cek dari environment variable
        env_icon = os.getenv('GROWL_ICON')
        if env_icon and Path(env_icon).is_file():
            icon = Path(env_icon).as_uri()
        # Jika tidak ada, akan gunakan default dari notifier instance
    elif isinstance(icon, (str, Path)):
        # Convert ke URI jika belum
        icon_path = Path(icon)
        if icon_path.is_file():
            icon = icon_path.as_uri()
    
    notifier.notify(title, message, note_type, sticky, icon=icon)