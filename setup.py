from setuptools import setup, find_packages
from version_get import VersionGet as vget

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="django-growl-notifier",
    version=vget().get(True),
    author="Hadi Cahyadi",
    author_email="cumulus13@gmail.com",
    description="Send Django server notifications to Growl",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cumulus13/django-growl-notifier",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 5.0",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Django>=3.2",
        "gntp>=1.0.3",
        "version_get"
    ],
    license="MIT"
)