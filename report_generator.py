import csv
import os
from timeit import default_timer as timer
from time import sleep
from custom_exceptions import CustomEvalError


class GenerateProcessEvaluationReport():
    def __init__(self, p_id, i, os_name):
        try:
            import psutil
            
        except ModuleNotFoundError as e:
            install_module = input("This implementation uses the psutil module\
to capture process information.\nDo you agree to install the module on this\
machine?\n(y/n)")
            
            if install_module in ('y','Y'): 
                subprocess.run(["pip", "install", "psutil"], shell=True)
                import psutil
            else:
                raise(e, "\nThis program cannot run without the psutil module...")
            
        self.p_id = p_id
        self.process = psutil.Process(p_id)
        self.process_name = self.process.name()
        self.i = i
        
        self.os_name = os_name
        self.buffer = []
        self.total_time = 0

        if self.os_name == "Linux":
            self.field_names = ['CPU(%)', 'MEM_RSS(MB)', 'MEM_VMS(MB)', 'NO_FDs']
            self.n_hndl = self.process.num_fds
            self.no_cpus = 1            

        elif self.os_name == "Windows":
            self.field_names = ['CPU(%)', 'MEM_WS(MB)', 'MEM_PRVT(MB)', 'NO_OPN_HNDLS']
            self.n_hndl = self.process.num_handles
            self.no_cpus = psutil.cpu_count()

    def _write_the_report(self, rows=None):
        if rows == None:
            with open("report.csv", "w") as file:
                writer = csv.writer(file)
                writer.writerow(self.field_names)

        else:
            with open("report.csv", "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(self.buffer)

                self.buffer = []

    def process_eval(self):
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
        
        time_init = timer()
        trail = 0
        
        self._write_the_report()

        while True:
            try:
                cpu = '{:.2f}'.format(self.process.cpu_percent(self.i) / self.no_cpus)
                memory_s = '{:.2f}'.format(self.process.memory_info()[0] / (1024**2))
                memory_v = '{:.2f}'.format(self.process.memory_info()[1] / (1024**2))
                no_handles = self.n_hndl()
                
                self.buffer.append([cpu, memory_s, memory_v, no_handles])

                print(cpu, memory_s, memory_v, no_handles)

            except Exception as e:
                if len(self.buffer) != 0:
                    self._write_the_report(self.buffer)

                print(CustomEvalError(e))                
                break
            
            if len(self.buffer) > 5:
                self._write_the_report(self.buffer)

            sleep(float(self.i) - trail)
            trail = (timer() - time_init) % (self.i * 2)

        self.total_time = timer() - time_init

    
                
            

          
            

                        

            

        
