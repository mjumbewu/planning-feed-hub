import os
from django.core.exceptions import ImproperlyConfigured

try:
    from . import local
except ImportError:
    local = None

local_env = {}

def get_var(var_name):
    var = getattr(
        local, var_name, local_env.get(
            var_name, os.environ.get(var_name, None)))
    return var

def parse_db_url(url_str):
    import sys
    import urlparse

    # Register database schemes in URLs.
    urlparse.uses_netloc.append('postgres')
    urlparse.uses_netloc.append('mysql')

    try:
        url = urlparse.urlparse(os.environ['DATABASE_URL'])
    except KeyError:
        raise ImproperlyConfigured('You must supply a valid DATABASE or a '
                                   'DATABASE_URL')

    engines = {
        'postgres': 'django.db.backends.postgresql_psycopg2',
    }

    def_ports = {
        'postgres': 5432
    }

    # Update with environment configuration.
    db_settings = {
        'ENGINE': engines.get(url.scheme, ''),
        'NAME': url.path[1:],
        'USER': url.username,
        'PASSWORD': url.password,
        'HOST': url.hostname,
        'PORT': url.port or def_ports.get(url.scheme, ''),
    }

    return db_settings
