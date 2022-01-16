import click
from cli.handlers.filesystem.file_handler import FileHandler
from cli.handlers.filesystem.template_handler import SharedTemplateHandler
from cli.utils.fs.utils import inside_project_directory


file_handler = FileHandler()


@click.group()
@click.pass_context
def docker(ctx):
    """
    Run Docker-related options for your project.
    """

    ctx.ensure_object(dict)

    ctx.obj['scoped_context'] = {
        'verbose': ctx.obj['verbose'],
        'force': ctx.obj['force'],
        'dry': ctx.obj['dry'],
    }

    if ctx.invoked_subcommand is not None:
        if not inside_project_directory(ctx, exit_on_error=not ctx.obj['force']):
            click.Abort()


@docker.command()
@click.pass_context
def create_dockerfile(ctx):
    """
    Creates a Dockerfile for this project.
    """

    dockerfile_content = SharedTemplateHandler.parsed_template(template='dockerfile.tpl')
    file_handler.create_file(dockerfile_content, filename='Dockerfile', **ctx.obj)

    entrypoint_content = SharedTemplateHandler.parsed_template(template='docker_entrypoint.tpl')
    file_handler.create_file(entrypoint_content, filename='docker-entrypoint.sh', **ctx.obj)


@docker.command()
@click.pass_context
def create_compose(ctx):
    """
    Creates a docker-compose file for this project.
    """

    manage_file = ctx.obj['project_files'].get('manage.py')
    project = manage_file.parent.name

    compose_content = SharedTemplateHandler.parsed_template(template='docker_compose.tpl', context={'project': project})
    file_handler.create_file(compose_content, filename='docker-compose.yml', **ctx.obj)
