run_proc_eval.py - RUNNING A PROCESS AND RETRIEVING CONSUMPTION OF RESOURCES

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

---------------------

DEALING WITH THE CSV REPORT FILE

The tool creates a subfolder in the current directory,
renames the CSV report file and moves it in the newly created folder.

The folder name will be the name of the target process.

The CSV file will be renamed with the following format:
[Timestamp]_[process_name]_[evaluation_time_duration]_[evaluation_time_interval].csv'
