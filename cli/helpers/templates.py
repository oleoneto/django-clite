# helpers:template
import jinja2
import os


def get_template(name, path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file == name:
                return f'{root}{file}'
    return None


def get_template_path(name, path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file == name:
                return os.path.realpath(root)
    return None


def get_templates(pattern, path):
    templates = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(pattern):
                templates.append({
                    file: root,
                })
    return templates


def rendered_file_template(path, template, context):
    """
    :param path: path to templates directory
    :param template: template to render
    :param context: context dict for template
    :return: rendered template
    """

    _ = jinja2.Environment(
        loader=jinja2.FileSystemLoader(path)
    ).get_template(template).render(context)

    return _
