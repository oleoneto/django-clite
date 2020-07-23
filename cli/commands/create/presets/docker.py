# # cli:commands:create:presets:docker

SERVICES = {
    'celery',
    'database',
    'redis',
    'vault',
}

DEFAULTS = [p for p in SERVICES if p not in ['vault']]
