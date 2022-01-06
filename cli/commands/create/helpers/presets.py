# cli:commands:create:helpers
import click
import inquirer
import os
from cli.config.presets import docker, extra_apps, installable_apps
from cli.config.presets import presets


def inquire_app_presets(app, default=False):

    remotes = {
        'bitbucket': 'bitbucket.org',
        'github': 'github.com',
        'gitlab': 'gitlab.com',
    }

    # ------------------------------------------
    # Default installation
    if default:
        return {
            'author': os.environ.get('USER'),
            'origin': f"git@{remotes['github']}:{os.environ.get('USER')}/{app}.git",
            'remote': remotes['github'],
            'repository': app,
            'url': f"https://{remotes['github']}/{os.environ.get('USER')}/{app}",
            'user': os.environ.get('USER'),
        }
    # ------------------------------------------

    # ------------------------------------------
    # Customized installation
    # ------------------------------------------
    questions = [
        inquirer.List('remote', message='remote', choices=[r for r in remotes], carousel=True),
        inquirer.Text('author', message='package author', default=os.environ.get('USER')),
        inquirer.Text('email', message='author email address'),
        inquirer.Text('user', message='repository user/organization', default=os.environ.get('USER')),
        inquirer.Text('repository', message='repository name', default=app),
    ]

    # Get answers
    answers = inquirer.prompt(questions)

    # Remote origin URL
    answers['origin'] = f"git@{remotes[answers['remote']]}:{answers['user']}/{answers['repository']}.git"
    answers['url'] = f"https://{remotes[answers['remote']]}/{answers['user']}/{answers['repository']}"

    return answers


def inquire_docker_options(default=False):
    if default:
        return {
            'services': docker.DEFAULTS,
        }

    # Choose redis, db, wsgi, celery
    questions = [
        inquirer.Checkbox(
            'services',
            message='supported docker services',
            choices=sorted(docker.SERVICES),
            default=docker.DEFAULTS
        ),
    ]

    answers = inquirer.prompt(questions)

    return answers


def inquire_installable_apps(default=False):
    apps = []
    middleware = []

    if default:
        apps = [a for a in installable_apps.DEFAULTS]
        middleware = [
            app for a in installable_apps.INSTALLABLE_APPS
            if a in installable_apps.DEFAULTS
            for app in installable_apps.INSTALLABLE_APPS[a]['middleware']
        ]
        return apps, middleware

    if click.confirm('Would you like to add apps to your INSTALLED_APPS?'):
        app_questions = [
            inquirer.Checkbox(
                'install', message='install default apps', choices=sorted(installable_apps.INSTALLABLE_APPS),
                default=installable_apps.DEFAULTS
            ),
        ]

        # Determine installed apps
        app_answers = inquirer.prompt(app_questions)['install']
        apps = [
            app for a in installable_apps.INSTALLABLE_APPS
            if a in app_answers
            for app in installable_apps.INSTALLABLE_APPS[a]['apps']
        ]

        middleware = [
            app for a in installable_apps.INSTALLABLE_APPS
            if a in app_answers
            for app in installable_apps.INSTALLABLE_APPS[a]['middleware']
        ]

    return apps, middleware


def inquire_project_presets(project_name, default=False):

    remotes = {
        'bitbucket': 'bitbucket.org',
        'github': 'github.com',
        'gitlab': 'gitlab.com',
    }

    # ------------------------------------------
    # Default installation
    if default:
        return {
            'author': os.environ.get('USER'),
            'origin': f"git@{remotes['github']}:{os.environ.get('USER')}/{project_name}.git",
            'presets': presets.DEFAULTS,
            'remote': remotes['github'],
            'repository': project_name,
            'url': f"https://{remotes['github']}/{os.environ.get('USER')}/{project_name}",
            'user': os.environ.get('USER'),
            # 'custom_apps': [extra_apps.DEFAULTS],
        }
    # ------------------------------------------

    # ------------------------------------------
    # Customized installation
    # ------------------------------------------
    questions = [
        inquirer.Checkbox(
            'presets', message='supported presets', choices=sorted(presets.PRESETS), default=presets.DEFAULTS
        ),
        inquirer.Checkbox(
            'custom_apps', message='custom apps', choices=extra_apps.EXTRA_APPS
        ),
        inquirer.List('remote', message='remote', choices=[r for r in remotes], carousel=True),
        inquirer.Text('author', message='package author', default=os.environ.get('USER')),
        inquirer.Text('user', message='repository user/organization', default=os.environ.get('USER')),
        inquirer.Text('repository', message='repository name', default=project_name),
    ]

    # Get answers
    answers = inquirer.prompt(questions)

    # Remote origin URL
    answers['origin'] = f"git@{remotes[answers['remote']]}:{answers['user']}/{answers['repository']}.git"
    answers['url'] = f"https://{remotes[answers['remote']]}/{answers['user']}/{answers['repository']}"

    return answers
