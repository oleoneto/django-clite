# # cli:commands:new:defaults:app
from cli.core.filesystem import File, Directory


def generic_package(n: str) -> Directory:
    return Directory(n, children=[File(name="__init__.py", template="shared/init.tpl")])


def new_app(name: str) -> Directory:
    admin = Directory(name="admin", children=[
        File(name="__init__.py", template="shared/init.tpl"),
        generic_package("actions"),
        generic_package("inlines"),
        generic_package("permissions"),
    ])

    models = Directory("models", children=[
        File(name="__init__.py", template="shared/init.tpl"),
        generic_package("managers"),
        generic_package("signals"),
        generic_package("validators"),
    ])

    router = Directory("router", children=[
        File(name="__init__.py", template="app/router_init.tpl"),
        File(name="api.py", template="app/api.tpl"),
        File(name="router.py", template="app/router.tpl")
    ])

    tests = Directory("tests", children=[
        File(name="__init__.py", template="app/viewsets_init.tpl"),
        generic_package("models"),
        generic_package("viewsets"),
    ])

    viewsets = Directory("viewsets", children=[
        Directory(name="permissions"),
        Directory(name="mixins"),
        File(name="__init__.py", template="shared/init.tpl"),
    ])

    app = Directory(name=name, children=[
        admin,
        models,
        router,
        tests,
        viewsets,
        generic_package("fixtures"),
        generic_package("forms"),
        generic_package("middleware"),
        generic_package("migrations"),
        generic_package("serializers"),
        generic_package("tasks"),
        generic_package("templates"),
        generic_package("templatetags"),
        generic_package("views"),
        File(name="__init__.py", template="shared/init.tpl"),
        File(name="apps.py", template="app/apps.tpl"),
        File(name="urls.py", template="app/urls.tpl"),
        File(name="constants.py", content=""),
    ])

    return app


def application_callback(ctx, param, value) -> list[Directory]:
    apps = []

    for name in value:
        app = new_app(name)

        if ctx.params.get("is_package", False):
            app = Directory(name=name, children=[
                app,
                File(name="LICENSE", template="shared/LICENSE.tpl"),
                File(name="MANIFEST", template="shared/MANIFEST.tpl"),
                File(name="README.md", template="shared/README.tpl"),
                File(name="pyproject.toml", template="shared/pyproject.tpl"),
            ])

        apps.append(app)

    return apps
