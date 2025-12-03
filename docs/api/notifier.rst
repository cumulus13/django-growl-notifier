Notifier API
============

This module contains the core notification functionality.

.. automodule:: django_growl.notifier
   :members:
   :undoc-members:
   :show-inheritance:

Classes
-------

GrowlNotifier
~~~~~~~~~~~~~

.. autoclass:: django_growl.notifier.GrowlNotifier
   :members:
   :special-members: __init__
   :undoc-members:
   :no-index:

   Main class for managing Growl notifications.

   **Attributes:**

   .. attribute:: growl_hosts
      
      List of configured Growl host addresses.
      
      :type: list

   .. attribute:: app_name
      
      Application name shown in Growl.
      
      :type: str

   .. attribute:: enabled
      
      Whether notifications are enabled.
      
      :type: bool

   .. attribute:: icon
      
      Path/URI to the notification icon.
      
      :type: pathlib.Path

   .. attribute:: notifiers
      
      List of registered GNTP notifiers.
      
      :type: list

   **Methods:**

   .. automethod:: __init__
      :no-index:

      Initialize the GrowlNotifier with settings from Django configuration.

      Reads the following settings:
      
      * ``GROWL_HOSTS`` - Required list of hosts
      * ``GROWL_APP_NAME`` - Optional application name
      * ``GROWL_ENABLED`` - Optional enable/disable flag
      * ``GROWL_ICON`` - Optional icon path

      Automatically registers with all configured Growl hosts.

   .. automethod:: notify
      :no-index:

      Send a notification to all registered Growl hosts.

      :param str title: Notification title
      :param str message: Notification message body
      :param str note_type: Type of notification ('Info', 'Error', 'Server Status')
      :param bool sticky: Whether notification should stay visible until dismissed
      :param icon: Custom icon for this notification (overrides default)
      :type icon: str or None
      :return: None

      **Example:**

      .. code-block:: python

         notifier = GrowlNotifier()
         notifier.notify(
             title="Task Complete",
             message="Processing finished",
             note_type='Info',
             sticky=False,
             icon='/path/to/icon.png'
         )

Functions
---------

get_growl_notifier
~~~~~~~~~~~~~~~~~~

.. autofunction:: django_growl.notifier.get_growl_notifier
   :no-index:

   Get or create the singleton GrowlNotifier instance.

   :return: Singleton GrowlNotifier instance
   :rtype: GrowlNotifier

   This function ensures only one notifier instance exists throughout
   the application lifecycle. Subsequent calls return the same instance.

   **Example:**

   .. code-block:: python

      from django_growl import get_growl_notifier

      notifier = get_growl_notifier()
      if notifier.enabled:
          notifier.notify("Hello", "World")

send_notification
~~~~~~~~~~~~~~~~~

.. autofunction:: django_growl.notifier.send_notification
   :no-index:

   Send a notification using the singleton GrowlNotifier.

   :param str title: Notification title
   :param str message: Notification message
   :param str note_type: Notification type ('Info', 'Error', 'Server Status')
   :param bool sticky: Keep notification visible until dismissed
   :param icon: Icon path/URI (optional)
   :type icon: str, pathlib.Path, or None
   :return: None

   This is the main function you'll use to send notifications from your code.

   **Icon Priority:**
   
   1. ``icon`` parameter
   2. ``GROWL_ICON`` environment variable
   3. ``GROWL_ICON`` setting
   4. Package default icon

   **Example:**

   .. code-block:: python

      from django_growl import send_notification

      # Basic notification
      send_notification("Task Done", "Completed successfully")

      # With all options
      send_notification(
          title="Error Occurred",
          message="Database connection failed",
          note_type='Error',
          sticky=True,
          icon='/path/to/error-icon.png'
      )

Constants
---------

Notification Types
~~~~~~~~~~~~~~~~~~

The following notification types are available:

* ``'Info'`` - General information notifications (default)
* ``'Error'`` - Error notifications
* ``'Server Status'`` - Server status notifications

Example usage:

.. code-block:: python

   send_notification("Info", "Process started", note_type='Info')
   send_notification("Error", "Process failed", note_type='Error')
   send_notification("Status", "Server restarted", note_type='Server Status')