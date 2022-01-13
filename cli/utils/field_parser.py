import inflection
from .fs.fs import FSHelper
from cli.decorators import watch_templates


@watch_templates(scope='generator')
class FieldParser(FSHelper):
    def __append_admin_field(self, value):
        # TODO: Add default `id` field
        if value not in self.admin_fields_list:
            self.admin_fields_list.append(value)

    def append_import(self, value, scope=''):
        if value not in self.imports_list:
            self.imports_list.append([f'{scope}.{value}', f'{inflection.camelize(value)}'])

    def append_special_import(self, value, scope=''):
        """
        Creates an import statement for special inheritance.

        :param scope:
        :param value:
        :return:
        """
        if value in DEFAULT_SPECIAL_INHERITABLE_TYPES:
            statement = DEFAULT_SPECIAL_INHERITABLE_TYPES[value]
            value = inflection.camelize(inflection.underscore(value))
            self.special_import = (statement, value)
            return True
        else:
            model = inflection.camelize(inflection.underscore(value))
            value = inflection.underscore(value)
            if scope:
                if self.project_name:
                    self.special_import = (f'{self.project_name}.{scope}.models.{value}', model)
                else:
                    self.special_import = (f'{scope}.models.{value}', model)
            else:
                self.special_import = (f'.{value}', model)
        return False
