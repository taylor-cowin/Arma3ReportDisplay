from pathlib import Path
from pathlib import WindowsPath
import os
import threading

current_logfile = None

def get_report_dir():
    home_path = Path.home()
    if type(home_path) is WindowsPath:
        expected_dir = WindowsPath(home_path,'AppData','Local','Arma 3')
        if expected_dir.exists():
            return expected_dir
        else:
            handle_error('Could not find ' + str(expected_dir))
        
    else:
        handle_error('This program can only be run on Windows machines.')
    
def check_for_rpt_file():
    files = os.listdir(report_dir)
    
            #check list of files every 30 seconds
            #if new file, switch to it
def print_log_lines():
        #print last line of file unless it has already been printed - check every 15ms   
    
def handle_error(e):
    input('Unable to proceed: ' + str(e))
    quit()
        
if __name__ == "__main__":
    report_dir = get_report_dir()
    
    check_thread = threading.Thread(check_for_rpt_file)
    parse_thread = threading.Thread(print_log_lines)
    
    check_thread.start()    
    parse_thread.start()
    
    check_thread.join()
    parse_thread.join()

    print('Execution complete. Program will now exit.')
