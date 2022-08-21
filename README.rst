=====
Scrap
=====

Scrap is a collection of useful stuff that I'm tired of rewriting/copying from previous projects.

Quick Start
-----------

1. Add 'scrap' to your 'INSTALLED_APPS' setting like this::

    INSTALLED_APPS = [
        ...
        'scrap',
    ]

2. Add '' to your 'MIDDLEWARE' setting if you want queries logged.  I believe it has to be first in the list.  Probably should check on that.::

    MIDDLEWARE = [
        'scrap.db.QueryCountDebugMiddleware',
        ...
    ]

3. Make sure LOGGING shows DEBUG level to see the query logging.  An example of such is::

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s|%(asctime)s|%(module)s|%(process)d|%(thread)d|%(message)s',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
            },
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
        }
    }

4. No migrations to run.  No urls to add.


Remove these notes
------------------

Build the package::

    python setup.py sdist

Install the package via ``pip``::

    python -m pip install --user django-scrap/dist/django-scrap-0.1.tar.gz

Install the package via ``requirements.txt``::

    # Line from requirements.txt shows a relative path to the folder containing 'setup.py'.
    ../django-scrap
