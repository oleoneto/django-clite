# helpers:template
import jinja2


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
