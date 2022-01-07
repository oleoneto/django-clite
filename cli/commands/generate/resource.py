import click
from cli.utils.sanitize import sanitized_string


@click.command()
@click.option('-a', '--abstract', is_flag=True, help="Creates an abstract model type.")
@click.option('-t', '--test-case', is_flag=True, help="Creates a TestCase for model.")
@click.option('-f', '--full', is_flag=True, help="Adds all related resources and TestCase")
@click.option('--register-admin', is_flag=True, help="Register model to admin site.")
@click.option('--register-inline', is_flag=True, help="Register model to admin site as inline.")
@click.option('-m', '--is-managed', is_flag=True, help="Add created_by and updated_by fields.")
@click.option('-i', '--inherits', '--extends', required=False, help="Add model inheritance.")
@click.option('--app', required=False, help="If base model inherits is in another app.")
@click.option('--api', is_flag=True, help='Only add api-related files.')
@click.option('-s', '--soft-delete', is_flag=True, help='Add ability to soft-delete records.')
@click.argument("name", required=True)
@click.argument("fields", nargs=-1, required=False)
@click.pass_context
def model(ctx, name, full, abstract, fields, register_admin,
          register_inline, test_case, inherits, api, app, is_managed, soft_delete):
    """
    Generates a model under the models directory.
    One can specify multiple attributes after the model's name, like so:

        D g model track int:number char:title fk:album bool:is_favorite

    This will generate a Track model and add a foreign key of Album.
    If the model is to be added to admin.site one can optionally opt in by specifying the --register-admin flag.
    """

    name = ModelHelper.check_noun(name)

    # Ensure --app is used only if --inherits is used
    if app and not inherits:
        log_error("You've specified an app inheritance scope but did not specify the model to inherit from.")
        log_error("Please rerun the command like so:")
        log_standard(f"D generate model {name} --inherits BASE_MODEL --app {app}")
        raise click.Abort

    path = ctx.obj['models']

    helper = ModelHelper(
        cwd=path,
        dry=ctx.obj['dry'],
        force=ctx.obj['force'],
        verbose=ctx.obj['verbose']
    )

    model_fields = helper.create(
        model=name,
        api=api,
        abstract=abstract,
        fields=fields,
        inherits=inherits,
        scope=app,
        project=ctx.obj['project_name'],
        is_managed=is_managed,
        soft_delete=soft_delete
    )

    if api:
        ctx.invoke(test, name=name, scope="model")
        ctx.invoke(serializer, name=name)
        ctx.invoke(viewset, name=name)

    if register_admin or full:
        ctx.invoke(admin, name=name, fields=model_fields)

    if register_inline or full:
        ctx.invoke(admin, name=name, inline=True)

    if (test_case or full) and not api:
        ctx.invoke(test, name=name, scope="model")

    if full and not api:
        ctx.invoke(serializer, name=name)
        ctx.invoke(viewset, name=name)

    if full:
        ctx.invoke(form, name=name)
        ctx.invoke(template, name=name, class_type='list')
        ctx.invoke(template, name=name, class_type='detail')
        ctx.invoke(view, name=name, class_type="list")
        ctx.invoke(view, name=name, class_type="detail")

    # Retuning model fields
    return model_fields


@click.command()
@click.argument("name", required=True)
@click.argument("fields", nargs=-1)
@click.option('-i', '--inherits', '--extends', required=False, help="Add model inheritance.")
@click.option('-m', '--is-managed', is_flag=True, help="Add created_by and updated_by fields.")
@click.option('--api', is_flag=True, help='Only add api-related files.')
@click.option('-s', '--soft-delete', is_flag=True, help='Add ability to soft-delete records.')
@click.pass_context
def resource(ctx, name, fields, inherits, api, is_managed, soft_delete):
    """
    Generates an app resource.

    This is ideal to add a model along with admin, serializer, view, viewset, template, and tests.
    You can invoke this command the same way you would the model command:

        D g resource track int:number char:title fk:album bool:is_featured

    This will generate a model with the specified attributes and all the related modules specified above.

    In case you're building an api, and don't need forms, templates and views, you can pass the --api flag to the command
    in order to prevent these files from being created.
    """

    name = ModelHelper.check_noun(name)

    try:
        ctx.invoke(
            model,
            name=name,
            api=api,
            register_admin=api,
            register_inline=api,
            fields=fields,
            test_case=True,
            inherits=inherits,
            is_managed=is_managed,
            soft_delete=soft_delete
        )

        ctx.invoke(admin, name=name)

        ctx.invoke(admin, name=name, inline=True)

        ctx.invoke(serializer, name=name)

        ctx.invoke(viewset, name=name)

        if not api:
            ctx.invoke(form, name=name)
            ctx.invoke(view, name=name, class_type='list')
            ctx.invoke(view, name=name, class_type='detail')
    except (KeyboardInterrupt, SystemExit) as e:
        log_error('Exited!')


@click.command(name='index')
@click.argument('name', required=True)
@click.option('-t', 'template', help='Template file associated with this search index')
@click.pass_context
def search_index(ctx, name, template):
    """
    Generates a search index for a given model.
    """

    path = ctx.obj['search_indexes']

    helper = IndexHelper(
        cwd=path,
        dry=ctx.obj['dry'],
        force=ctx.obj['force'],
        verbose=ctx.obj['verbose'],
    )

    helper.create(model=name, template=template)
