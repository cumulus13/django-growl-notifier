Middleware API
==============

Error notification middleware for Django.

.. automodule:: django_growl.middleware
   :members:
   :undoc-members:
   :show-inheritance:

GrowlErrorMiddleware
--------------------

.. autoclass:: django_growl.middleware.GrowlErrorMiddleware
   :members:
   :special-members: __init__, __call__
   :undoc-members:
   :no-index:

   Middleware to send Growl notifications when Django encounters errors.

   This middleware catches exceptions and sends detailed error notifications
   including the exception message, stacktrace, request path, and HTTP method.

   **Configuration:**

   Add to ``MIDDLEWARE`` in settings:

   .. code-block:: python

      MIDDLEWARE = [
          # ... other middleware
          'django_growl.middleware.GrowlErrorMiddleware',
      ]

   **Settings:**

   .. code-block:: python

      # Enable error notifications (default: True)
      GROWL_NOTIFY_ERRORS = True

      # Make error notifications sticky (default: True)
      GROWL_STICKY_ERRORS = True

   **Attributes:**

   .. attribute:: notify_errors
      
      Whether error notifications are enabled.
      
      :type: bool

   .. attribute:: sticky_errors
      
      Whether error notifications should be sticky.
      
      :type: bool

Methods
~~~~~~~

.. currentmodule:: django_growl.middleware

.. automethod:: GrowlErrorMiddleware.__init__
   :no-index:

   Initialize the middleware.

   :param get_response: Django's get_response callable
   :type get_response: typing.Callable

   Reads configuration from Django settings:
   
   * ``GROWL_NOTIFY_ERRORS`` - Enable/disable error notifications
   * ``GROWL_STICKY_ERRORS`` - Make error notifications sticky

.. automethod:: GrowlErrorMiddleware.__call__
   :no-index:

   Process the request through middleware chain.

   :param request: Django HTTP request object
   :type request: django.http.HttpRequest
   :return: Response from next middleware/view
   :rtype: django.http.HttpResponse


   .. automethod:: GrowlErrorMiddleware.process_exception
      :no-index:

   Handle exceptions and send notifications.

   :param request: Django HTTP request object
   :type request: django.http.HttpRequest
   :param exception: The raised exception
   :type exception: Exception
   :return: None (lets Django handle the exception normally)
   :rtype: None

   This method is called automatically by Django when an exception occurs.
   It formats the error information and sends a Growl notification with:
   
   * Exception type and message
   * Request path and method
   * Full stacktrace (truncated if too long)

   **Example notification format:**

   .. code-block:: text

      Title: Django Error: ValueError
      
      Message:
      Error: invalid literal for int()
      Path: /api/users/abc/
      Method: GET

      Traceback:
      File "views.py", line 42, in user_detail
        user_id = int(user_id_str)
      ValueError: invalid literal for int()

Usage Example
~~~~~~~~~~~~~

Once configured, the middleware automatically sends notifications for all
unhandled exceptions:

.. code-block:: python

   # views.py
   def my_view(request):
       # This error will trigger a Growl notification
       raise ValueError("Something went wrong")

   # The notification will include:
   # - Error type: ValueError
   # - Error message: Something went wrong
   # - Request path: /my-view/
   # - Request method: GET
   # - Full stacktrace

Disabling Error Notifications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Temporarily disable error notifications:

.. code-block:: python

   # settings.py
   GROWL_NOTIFY_ERRORS = False

Or remove the middleware:

.. code-block:: python

   MIDDLEWARE = [
       # ... other middleware
       # 'django_growl.middleware.GrowlErrorMiddleware',  # Commented out
   ]