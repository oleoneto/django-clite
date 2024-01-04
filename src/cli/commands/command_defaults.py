import inflection
from cli.core.templates.template import TemplateParser


def generic(name: str):
    return TemplateParser().parse_string(
        content="from .{{name}} import {{name}}",
        variables={
            "name": name,
            "classname": inflection.camelize(name),
        },
    )


def admin(name: str):
    return TemplateParser().parse_string(
        content="from .{{name}} import {{classname}}Admin",
        variables={
            "name": name,
            "classname": inflection.camelize(name),
        },
    )


def admin_inline(name: str):
    return TemplateParser().parse_string(
        content="from .{{name}} import {{classname}}Inline",
        variables={
            "name": name,
            "classname": inflection.camelize(name),
        },
    )


def form(name: str):
    return TemplateParser().parse_string(
        content="from .{{name}} import {{classname}}Form",
        variables={
            "name": name,
            "classname": inflection.camelize(name),
        },
    )


def manager(name: str):
    return TemplateParser().parse_string(
        content="from .{{name}} import {{classname}}Manager",
        variables={
            "name": name,
            "classname": inflection.camelize(name),
        },
    )


def model(name: str):
    return TemplateParser().parse_string(
        content="from .{{name}} import {{classname}}",
        variables={
            "name": name,
            "classname": inflection.camelize(name),
        },
    )


def serializer(name: str):
    return TemplateParser().parse_string(
        content="from .{{name}} import {{classname}}Serializer",
        variables={
            "name": name,
            "classname": inflection.camelize(name),
        },
    )


def signal(name: str):
    return generic(name)


def tag(name: str):
    return generic(name)


def test(name: str):
    return TemplateParser().parse_string(
        content="from .{{name}}_test import {{classname}}TestCase",
        variables={
            "name": name,
            "classname": inflection.camelize(name),
        },
    )


def validator(name: str):
    return TemplateParser().parse_string(
            content="from .{{name}} import {{name}}_validator",
            variables={
                "name": name,
                "classname": inflection.camelize(name),
            },
        )


def view(name: str, klass: str):
    return TemplateParser().parse_string(
        content="from .{{name}} import {{classname}}",
        variables={
            "name": f"{name}{'_' + klass if klass else ''}",
            "classname": f"{inflection.camelize(name) + inflection.camelize(klass) + 'View' if klass else name}",
        },
    )


def viewset(name: str):
    return TemplateParser().parse_string(
        content="from .{{name}} import {{classname}}ViewSet",
        variables={
            "name": name,
            "classname": inflection.camelize(name),
        },
    )
