Contributing
============

Thank you for your interest in contributing to Django Growl Notifier!

This document provides guidelines for contributing to the project.

Ways to Contribute
------------------

* Report bugs
* Suggest new features
* Improve documentation
* Submit bug fixes
* Add new features
* Write tests

Getting Started
---------------

1. Fork the Repository
~~~~~~~~~~~~~~~~~~~~~~

Fork the project on GitHub:

https://github.com/cumulus13/django-growl-notifier

2. Clone Your Fork
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git clone https://github.com/YOUR-USERNAME/django-growl-notifier.git
   cd django-growl-notifier

3. Create a Virtual Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate

4. Install Development Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install -e .[dev]

This installs:

* Package in editable mode
* Testing dependencies (pytest, coverage)
* Documentation dependencies (Sphinx)
* Code quality tools (black, flake8)

Development Workflow
--------------------

1. Create a Branch
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix

2. Make Your Changes
~~~~~~~~~~~~~~~~~~~~

* Write clean, readable code
* Follow PEP 8 style guide
* Add docstrings to functions and classes
* Update documentation if needed

3. Write Tests
~~~~~~~~~~~~~~

.. code-block:: bash

   # Run tests
   pytest

   # Run with coverage
   pytest --cov=django_growl

   # Generate coverage report
   pytest --cov=django_growl --cov-report=html

4. Format Code
~~~~~~~~~~~~~~

.. code-block:: bash

   # Format with black
   black django_growl

   # Check with flake8
   flake8 django_growl

5. Update Documentation
~~~~~~~~~~~~~~~~~~~~~~~

If you changed functionality:

.. code-block:: bash

   cd docs
   make html
   # View in browser: docs/_build/html/index.html

6. Commit Changes
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git add .
   git commit -m "Add feature: description of your changes"

Write clear commit messages:

* Use present tense ("Add feature" not "Added feature")
* First line: brief summary (50 chars or less)
* Blank line, then detailed description if needed

7. Push and Create Pull Request
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git push origin feature/your-feature-name

Then open a Pull Request on GitHub.

Code Style
----------

* Follow PEP 8
* Use meaningful variable names
* Write docstrings for public functions
* Keep functions focused and small
* Add type hints where appropriate

Example:

.. code-block:: python

   def send_notification(
       title: str,
       message: str,
       note_type: str = 'Info',
       sticky: bool = False,
       icon: Optional[str] = None
   ) -> None:
       '''Send a Growl notification.
       
       Args:
           title: Notification title
           message: Notification message
           note_type: Type of notification
           sticky: Keep notification visible
           icon: Custom icon path
       '''
       # Implementation

Testing
-------

Write tests for new features:

.. code-block:: python

   # tests/test_notifier.py
   import pytest
   from django_growl import send_notification
   
   def test_send_notification():
       '''Test basic notification sending'''
       # This should not raise an exception
       send_notification("Test", "Message")
   
   def test_notification_with_icon():
       '''Test notification with custom icon'''
       send_notification(
           "Test",
           "Message",
           icon="/path/to/icon.png"
       )

Run tests:

.. code-block:: bash

   pytest -v

Documentation
-------------

Update documentation when you:

* Add new features
* Change existing behavior
* Add new configuration options

Documentation is in ``docs/`` directory using reStructuredText.

Build documentation:

.. code-block:: bash

   cd docs
   make html

Reporting Bugs
--------------

When reporting bugs, include:

* Django version
* Python version
* django-growl-notifier version
* Operating system
* Steps to reproduce
* Expected behavior
* Actual behavior
* Full error traceback

Example bug report:

.. code-block:: text

   **Environment:**
   - Django 5.2.8
   - Python 3.11
   - django-growl-notifier 0.1.0
   - Windows 11

   **Description:**
   Notifications not appearing when...

   **Steps to Reproduce:**
   1. Configure GROWL_HOSTS...
   2. Run python manage.py runserver
   3. ...

   **Expected:**
   Should see notification

   **Actual:**
   No notification appears

   **Traceback:**
   ```
   Traceback (most recent call last):
   ...
   ```

Suggesting Features
-------------------

When suggesting features:

* Explain the use case
* Describe the proposed solution
* Consider backwards compatibility
* Provide examples if possible

Pull Request Guidelines
-----------------------

* Keep PRs focused on a single change
* Update CHANGELOG.md
* Add tests for new features
* Update documentation
* Ensure all tests pass
* Follow code style guidelines

PR Description Template:

.. code-block:: text

   ## Description
   Brief description of changes

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Performance improvement

   ## Checklist
   - [ ] Tests added/updated
   - [ ] Documentation updated
   - [ ] CHANGELOG.md updated
   - [ ] All tests passing
   - [ ] Code formatted with black

Code Review Process
-------------------

1. Automated checks run on PR
2. Maintainer reviews code
3. Changes requested if needed
4. Once approved, PR is merged

Questions?
----------

* Open an issue on GitHub
* Email: cumulus13@gmail.com

Thank You!
----------

Your contributions make this project better!
