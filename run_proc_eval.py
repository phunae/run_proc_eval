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
from time import sleep
from timeit import default_timer as timer
import csv
from datetime import datetime

from custom_exceptions import CustomCommandException, CustomProcessError, CustomEvalError

from file_manager import HandlingProcessReport

try:
    import psutil    
except ModuleNotFoundError as e:
    subprocess.run(["pip", "install", "psutil"], shell=True)
    import psutil


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
    

def proc_run(path):
    try:
        return subprocess.Popen(path)
    except Exception as e:
        raise CustomProcessError(e)
              
def proc_eval(p, i, os_name):
    """This is where the process evaluation values are being captured.
    
    The CPU percentage is retrieved as such:
        - in Linux:
        The returned value is not split evenly between all available CPUs.
        This will result in values over 100% on systems where more than two CPU cores are installed.
        (up to 800% for an 8 Core system)

        - in Windows:
        The returned values will be an average of the values we would get on Linux, 
        against the total number of CPU cores.

    The memory consumption information is displayed in MBs.

    The open handles will be returned as integers.
    """

    if os_name == 'Linux':
        n_hndl = p.num_fds
        no_cpus = 1
    elif os_name == 'Windows':
        n_hndl = p.num_handles
        no_cpus = psutil.cpu_count()

    cpu = '{:.2f}'.format(p.cpu_percent(i) / no_cpus)
    memory_s = '{:.1f}'.format(p.memory_info()[0] / (1024*1024))
    memory_v = '{:.1f}'.format(p.memory_info()[1] / (1024*1024))
    no_handles = n_hndl()
    
    return cpu, memory_s, memory_v, no_handles

if __name__ == "__main__":

    path, interval = load_parameters()        
    os_name = platform.system()

    if os_name == "Linux":
        field_names = ['CPU(%)', 'MEM_RSS(MB)', 'MEM_VMS(MB)', 'NO_FDs']

    elif os_name == "Windows":
        field_names = ['CPU(%)', 'MEM_WS(MB)', 'MEM_PRVT(MB)', 'NO_OPN_HNDLS']

    else: raise Exception("This tool is only supported on Linux and Windows")
       
    p = proc_run(path)  
    proc = psutil.Process(p.pid)
    proc_name = proc.name()


    with open("report.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(field_names)

        time_init = timer()
        date = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")

        while p.poll() is None:
            try:
                cpu, memory_s, memory_v, no_handles = proc_eval(proc, interval/2, os_name)
            except Exception as e:
                print(CustomEvalError(e))
                break

            print(cpu, memory_s, memory_v, no_handles)

            writer.writerow([cpu, memory_s, memory_v, no_handles])
            
            sleep(float(interval)/2)

        total_time = timer() - time_init

    handle_report = HandlingProcessReport(proc_name, date, interval, total_time)

    handle_report.move_file()

    

    

    
    







