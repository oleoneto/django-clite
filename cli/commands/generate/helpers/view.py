import inflection
from cli.helpers.logger import *
from cli.helpers import sanitized_string
from cli.helpers import rendered_file_template
from cli.commands.generate.helpers.generator import Generator


class ViewHelper(Generator):

    def create(self, model, **kwargs):
        model = self.check_noun(model)
        model = sanitized_string(model)
        classname = inflection.camelize(model)
        singular = inflection.singularize(classname)
        plural = inflection.pluralize(classname)
        class_type = kwargs.get('class_type', None)
        extra = {}

        filename = f"{model.lower()}.py"
        template = 'view-function.tpl'
        template_import = 'view-function-import.tpl'
        view_name = inflection.underscore(singular)
        route_name = f'{inflection.underscore(model)}/'
        template_name = f'{model.lower()}.html'

        if class_type is not None:
            filename = f"{model.lower()}_{class_type}.py"
            template = 'view-class.tpl'
            template_import = 'view-class-import.tpl'

            if class_type not in ['template']:
                view_name = inflection.underscore(singular) + f'-{class_type}'
                template_name += f'_{class_type.lower()}.html'
                extra['object_name'] = plural if class_type == 'list' else singular

            if class_type in ['form', 'update', 'create']:
                extra['form_class'] = f'{classname}Form'

            if class_type in ['list']:
                route_name = f'{inflection.underscore(plural)}/'
                extra['pagination'] = True

            if class_type in ['detail', 'update']:
                route_name += '<slug:slug>'

        content = rendered_file_template(
            path=self.TEMPLATES_DIRECTORY,
            template=template,
            context={
                'model': model,
                'classname': classname,
                'class_type': class_type,
                'route_name': route_name,
                'view_name': view_name,
                'template_name': template_name,
                **extra,
            }
        )

        import_content = rendered_file_template(
            path=self.TEMPLATES_DIRECTORY,
            template=template_import,
            context={
                'model': model,
                'classname': classname,
                'class_type': class_type,
            }
        )

        self.add_import(
            template=template_import,
            content=import_content
        )

        if self.create_file(
            path=self.cwd,
            filename=filename,
            content=content
        ):

            resource = f"{model}_view."
            if class_type:
                resource = f"{classname}{class_type.capitalize()}View."
            log_success(DEFAULT_CREATE_MESSAGE.format(filename, resource))

    def delete(self, model, **kwargs):
        model = self.check_noun(model)
        classname = inflection.camelize(model)
        class_type = kwargs.get('class_type', None)

        filename = f"{model}.py"
        template_import = 'view-function-import.tpl'

        if class_type is not None:
            filename = f"{model}_{class_type}.py"
            template_import = 'view-class-import.tpl'

        content = rendered_file_template(
            path=self.TEMPLATES_DIRECTORY,
            template=template_import,
            context={
                'model': model,
                'classname': classname,
                'class_type': class_type,
            }
        )

        self.remove_import(content=content)

        if self.destroy_file(
            filename=filename,
            path=self.cwd
        ):

            resource = f"{model}_view."
            if class_type:
                resource = f"{classname}{class_type.capitalize()}View."
            log_success(DEFAULT_DELETE_MESSAGE.format(filename, resource))

        return True
