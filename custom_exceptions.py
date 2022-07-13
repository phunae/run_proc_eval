"""This class provides exceptions and errors specific to this tool"""

class CustomCommandException(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        if self.error.__class__.__name__ == 'IndexError':
            return 'This command needs two parameters... \n\
        run_proc_eval.py [path_to_process] [time_interval]'

        elif self.error.__class__.__name__ == 'ValueError':
            return f'The second paramenter needs to be a float or an integer\
...\nThis represents a time interval in seconds\n\
run_proc_eval.py [path_to_process] [time_interval]'

        else:
            return '{}:{}'.format(type(self.error),self.error)

class CustomProcessError(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        if self.error.__class__.__name__ in ('FileNotFoundError', 'NoSuchProcess'):
            return 'The path provided is not leading to a valid process'

        else:
            return '{}:{}'.format(type(self.error),self.error)
    
class CustomEvalError(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        if self.error.__class__.__name__ in ('AccessDenied', 'NoSuchProcess'):
            return 'The target process has closed...'

        else:
            return '{}:{}'.format(type(self.error),self.error)

class CustomFileError(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        if self.error.__class__.__name__ in ('PermissionError'):
            return 'Access is denied for this system path.\
Copy the .py files to a folder with write permissions.'

        else:
            return '{}:{}'.format(type(self.error),self.error)
    
