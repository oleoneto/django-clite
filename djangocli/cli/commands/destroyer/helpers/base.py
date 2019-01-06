import os
from djangocli.cli import log_error, log_success


class BaseHelper(object):

    def delete(self, base_dir, resource):

        file = resource

        if not resource.split('.')[-1] == 'py':
            file = f'{resource}.py'

        resource = resource.split('.')[0]

        try:
            os.chdir(base_dir)
            os.remove(file)
            log_success(f"Removed {file} successfully.")

            if len(os.listdir('.')) == 0:
                os.chdir('..')
                cur_dir = base_dir.split('/')[1]
                os.removedirs(cur_dir)
                log_success(f'Removed {cur_dir} directory.')
        except FileNotFoundError:
            log_error(f"File {file} for {resource.capitalize()} type not found.")
    # end def
# end class
