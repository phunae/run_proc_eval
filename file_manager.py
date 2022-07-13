"""Dealing with the CSV report file

This class creates a subfolder in the current directory,
renames the CSV report file and moves it in the newly created folder.

The folder name will be the name of the target process.

The CSV file will be renamed with the following format:
[Timestamp]_[process_name]_[evaluation_time_duration]_[evaluation_time_interval].csv'

"""

from os import path, mkdir, getcwd, replace
from datetime import timedelta

class HandlingProcessReport:
    def __init__(self, proc_name, date, interval, total_time):
        self.proc_name = proc_name
        self.date = date
        self.interval = interval
        self.total_time = total_time

    def _file_naming(self):
        duration = str(timedelta(seconds=int(self.total_time))).replace(':','-')

        file_name = f'[{self.date}]_[{self.proc_name}]_[duration_\
{duration}]_[{self.interval}s_interval].csv'

        return file_name
    
    def _create_proc_folder(self):
        try:
            folder_name = path.splitext(self.proc_name)[0]
            folder_path = path.join(getcwd(),folder_name)
            mkdir(folder_path)
        except FileExistsError:
            pass
        
        return folder_path

    def move_file(self):
        try:
            replace("report.csv", path.join(self._create_proc_folder(),
                                       self._file_naming()))

        except Exception as e:
            raise(CustomFileError(e))

    
        

        
            
            

    
        
