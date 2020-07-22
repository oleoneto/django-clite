# # cli:commands:create:presets:presets

PRESETS = {
    'environments',
    'celery',
    'dockerized',
    'dokku',
    'git',
    'heroku',
    # 'custom_settings',
    # 'custom_storage',
}

DEFAULTS = [p for p in PRESETS if p not in ['custom_settings', 'custom_storage']]
