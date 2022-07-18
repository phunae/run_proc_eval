"""run_proc_eval.py - Running a process and retrieving consumption of resources

This script starts a process and retrieves
the following process information while the process is running:
    - CPU usage (percent)
    - Memory consumption: 
        - Working Set and Private Bytes (for Windows systems) 
        - Resident Set Size and Virtual Memory Size (for Linux systems)
    - Number of open handles (Windows) or Number of file descriptors (Linux)

The output will be saved as a csv file in a new folder 
- created in the current directory.

--------------------

The script can be run from a command shell in the following format:

Linux: 
python3 run_proc_eval.py [path_to_process] [time_interval_between_data_collection_iterations]

Windows:
python run_proc_eval.py [path_to_process] [time_interval_between_data_collection_iterations]

Where:
- [path_to_process] 
needs to be a valid path to a process
- [time_interval_between_data_collection_iterations] 
will be an integer or a float number representing seconds

Examples:
python3 run_proc_eval.py gedit 2
python run_proc_eval.py "c:\windows\system32\mspaint.exe"

*** For the process data collection, the script uses the psutil library, which is automatically
*** installed if it can't be found and if the "pip" installer is setup in place.
"""

import sys
import subprocess
import platform
from timeit import default_timer as timer
from datetime import datetime

from custom_exceptions import CustomCommandException, CustomProcessError

from file_manager import HandlingReportFile
from report_generator import GenerateProcessEvaluationReport


def load_parameters(args = sys.argv[1:]):
    try:
        path, interval = args[0], args[1]        
    except IndexError as e:
        raise CustomCommandException(e)

    try:
        interval = float(interval)       
    except ValueError as e:
        raise CustomCommandException(e)

    return path, interval
    

def start_process(path):
    try:
        return subprocess.Popen(path)
    except Exception as e:
        raise CustomProcessError(e)
              
if __name__ == "__main__":

    path, interval = load_parameters()        
    os_name = platform.system()

    if os_name not in ('Linux', 'Windows'):
        raise Exception("This tool is only supported on Linux and Windows")

    date = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
       
    p = start_process(path)  

    rg = GenerateProcessEvaluationReport(p.pid, interval/2, os_name)

    rg.process_eval()

    handle_report = HandlingReportFile(rg.process_name, date, interval, rg.total_time)

    handle_report.move_file()

    

    

    
    







