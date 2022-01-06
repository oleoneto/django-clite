import os


class FileLocator:
    def traverse_directory(self, working_directory):
        """
        Implementation by Michele Pasin
        https://gist.github.com/zdavkeos/1098474#gistcomment-2943865

        Mimic os.walk, but walk 'up' instead of down the directory tree.
        """

        directory_path = os.path.realpath(working_directory)

        # get files in current dir
        try:
            names = os.listdir(directory_path)
        except Exception as e:
            print(e)
            return

        dirs, non_dirs = [], []
        for name in names:
            if os.path.isdir(os.path.join(directory_path, name)):
                dirs.append(name)
            else:
                non_dirs.append(name)

        yield directory_path, dirs, non_dirs

        new_path = os.path.realpath(os.path.join(directory_path, '../../handlers'))

        # see if we are at the top
        if new_path == directory_path:
            return

        for x in self.traverse_directory(new_path):
            yield x

    def find_files_in_directory(self, working_directory):
        pass
