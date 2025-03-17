from pathlib import Path
from pathlib import WindowsPath
import os
import threading
import re
import time

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

def set_current_logfile(file):
    global current_logfile
    current_logfile = file

#def compare_timestamps(stamp1, stamp2):





def get_timestamp(file):

    ###LEFT OFF HERE

    dirty_timestamp = re.search(r"[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}-[0-9]{2}-[0-9]{2}.rpt", file) #get the end of the filename
    print(dirty_timestamp.group().)
    clean_timestamp = str(dirty_timestamp.group()).split('.')[0] #remove the .rpt
    return clean_timestamp

    ### LEFT OFF HERE


def parse_report_timestamp(file):
    global current_logfile

    if current_logfile is None:
        current_logfile = file
        check_for_rpt_file() #Initialized, so start the loop again in case there are more
    else:
        old_file = get_timestamp(current_logfile)
        new_file = get_timestamp(file)

        #Returns true if file is newer
        #if compare_timestamps(old_file, new_file):
         #   current_logfile = file
        #    print("Newer file detected: " + str(current_logfile))

def check_for_rpt(file):
    if re.search(r".rpt", file):
        return True
    return False

def check_for_rpt_file():
    files = os.listdir(report_dir)
    report_list = []
    #Make a list of all reports
    for file in files:
        if check_for_rpt(file):
            report_list.append(file)
    if report_list == []:
        handle_error("No .rpt files found at " + str(report_dir))
    else:
        for rpt in report_list:
            parse_report_timestamp(rpt)
    time.sleep(10)
    check_for_rpt_file()
            #check list of files every X seconds
            #if new file, switch to it
#def print_log_lines():
        #print last line of file unless it has already been printed - check every 15ms     

def handle_error(e):
    input('Unable to proceed: ' + str(e))
    quit()
        
if __name__ == '__main__':
    report_dir = get_report_dir()
    
    check_thread = threading.Thread(group=None, target=check_for_rpt_file)
#    parse_thread = threading.Thread(print_log_lines,1)
    
    check_thread.start()    
#    parse_thread.start()
    
    check_thread.join()
#    parse_thread.join()

    print('Execution complete. Program will now exit.')
