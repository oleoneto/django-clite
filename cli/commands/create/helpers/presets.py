# cli:commands:create:helpers
import click
import inquirer
import os
from datetime import datetime
from cli.commands.create.presets import extra_apps
from cli.commands.create.presets import installable_apps
from cli.commands.create.presets import presets


def inquire_project_presets(project_name, default=False):

    remotes = {
        'github': 'git@github.com',
        'gitlab': 'git@gitlab.com',
        'bitbucket': 'git@bitbucket.org',
    }

    # ------------------------------------------
    # Default installation
    if default:
        return {
            'presets': presets.DEFAULTS,
            # 'custom_apps': [extra_apps.DEFAULTS],
            'remote': remotes['github'],
            'author': os.environ.get('USER'),
            'user': os.environ.get('USER'),
            'repository': project_name,
            'origin': f"{remotes['github']}:{os.environ.get('USER')}/{project_name}.git",
            'year': datetime.year,
        }
    # ------------------------------------------

    # ------------------------------------------
    # Customized installation
    # ------------------------------------------
    project_questions = [
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
    answers = inquirer.prompt(project_questions)

    # Remote origin URL
    answers['origin'] = f"{remotes[answers['remote']]}:{answers['user']}/{answers['repository']}.git"

    answers['year'] = datetime.year

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
        installed_apps_questions = [
            inquirer.Checkbox(
                'install', message='install default apps', choices=sorted(installable_apps.INSTALLABLE_APPS),
                default=installable_apps.DEFAULTS
            ),
        ]

        # Determine installed apps
        app_answers = inquirer.prompt(installed_apps_questions)['install']
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


def inquire_app_presets(app, default=False):

    remotes = {
        'github': 'git@github.com',
        'gitlab': 'git@gitlab.com',
        'bitbucket': 'git@bitbucket.org',
    }

    # ------------------------------------------
    # Default installation
    if default:
        return {
            'remote': remotes['github'],
            'author': os.environ.get('USER'),
            'user': os.environ.get('USER'),
            'repository': app,
            'origin': f"{remotes['github']}:{os.environ.get('USER')}/{app}.git",
            'url': f"https://{remotes['github']}.com/{os.environ.get('USER')}/{app}",
            'year': datetime.year,
        }
    # ------------------------------------------

    # ------------------------------------------
    # Customized installation
    # ------------------------------------------
    project_questions = [
        inquirer.List('remote', message='remote', choices=[r for r in remotes], carousel=True),
        inquirer.Text('author', message='package author', default=os.environ.get('USER')),
        inquirer.Text('user', message='repository user/organization', default=os.environ.get('USER')),
        inquirer.Text('repository', message='repository name', default=app),
        # TODO: Fix project repository url
        # inquirer.Text('url', message='', default=f"https://{remotes['github']}.com/{os.environ.get('USER')}/{app}"),
    ]

    # Get answers
    answers = inquirer.prompt(project_questions)

    # Remote origin URL
    answers['origin'] = f"{remotes[answers['remote']]}:{answers['user']}/{answers['repository']}.git"

    answers['year'] = datetime.year

    return answers
