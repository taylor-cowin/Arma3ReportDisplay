from pathlib import Path
from pathlib import WindowsPath
from collections import deque

import os
import threading
import re
import time
import datetime

current_logfile = None
file_updated = False
last_line_printed = None
report_dir = None
file_check_rate = 10 #How often (in seconds) to check for a new rpt file

def set_report_dir():
    global report_dir
    
    home_path = Path.home()
    if type(home_path) is WindowsPath:
        expected_dir = WindowsPath(home_path,'AppData','Local','Arma 3')
        if expected_dir.exists():
            report_dir = expected_dir
        else:
            handle_error('Could not find ' + str(expected_dir))
        
    else:
        handle_error('This program can only be run on Windows machines.')

def check_for_rpt_file():
    global file_updated
    global file_check_rate
    def _compare_timestamps(old_stamp, new_stamp):
        old_date = _parse_datetime(old_stamp)
        new_date = _parse_datetime(new_stamp)
        return old_date < new_date #return true if old date is older

    def _parse_datetime(stamp):
        def _get_year(stamp):
            return int(stamp[0:4])
        def _get_month(stamp):
            return int(stamp[5:7])
        def _get_day(stamp):
            return int(stamp[8:10])
        def _get_hour(stamp):
            return int(stamp[11:13])
        def _get_minute(stamp):
            return int(stamp[14:16])
        def _get_second(stamp):
            return int(stamp[17:19])
        return datetime.datetime(_get_year(stamp), _get_month(stamp), _get_day(stamp), _get_hour(stamp), _get_minute(stamp), _get_second(stamp))
    
    def _get_timestamp(file):
        dirty_timestamp = re.search(r"[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}-[0-9]{2}-[0-9]{2}.rpt", file) #get the end of the filename
        clean_timestamp = str(dirty_timestamp.group()).split('.')[0] #remove the .rpt
        return clean_timestamp

    def _parse_report_timestamp(file):
        global current_logfile
        global file_updated

        #First run
        if current_logfile is None:
            _set_current_logfile(file)
            file_updated = True
            check_for_rpt_file() #Just set the first file, so start the loop again in case there are more
        #Subsequent runs
        else:
            old_file = _get_timestamp(current_logfile) #inefficient -- should store the timestamp alongside the file to prevent constant matching
            new_file = _get_timestamp(file)
            #Returns true if file is newer
            if old_file != new_file:
                if _compare_timestamps(old_file, new_file):
                    _set_current_logfile(file)
                    file_updated = True
    
    def _set_current_logfile(file):
        global current_logfile
        current_logfile = file

    def _check_for_rpt_ext(file):
        if re.search(r".rpt", file):
            return True
        return False
    
    files = os.listdir(report_dir)
    report_list = []
    #Make a list of all reports
    for file in files:
        #Add to list if it is an '*.rpt' file
        if _check_for_rpt_ext(file):
            report_list.append(file)
    #If no report files are found
    if report_list == []:
        handle_error("No .rpt files found at " + str(report_dir))
    #Report files were found, so check timestamp for each to see if it is the most recent
    else:
        for rpt in report_list:
            _parse_report_timestamp(rpt)
    #Check for new log files every 10 seconds
    time.sleep(file_check_rate)
    check_for_rpt_file()
            
def print_log_lines():
    global current_logfile
    log_full_path = None
    
    def _check_new_file():
        global file_updated

        if file_updated is True:
            print('Newest .rpt file found: ' + str(current_logfile))
            file_updated = False
            print_log_lines()            
    
    def _get_last_line(file_handler):
        last_line = deque(file_handler, maxlen=2)[0]
        return last_line
    
    def _print_loop(log_full_path):
        global last_line_printed
        
        _check_new_file() #Make sure we're using the latest logfile
        file_handler = open(str(log_full_path), 'r')
        this_line = _get_last_line(file_handler)
              
        if this_line != last_line_printed or last_line_printed is None:
            print(this_line)
            last_line_printed = this_line
            
        time.sleep(.1)
        _print_loop(log_full_path)
    
    #If a log file exists, set the path   
    if current_logfile != None:
        log_full_path = str(report_dir) + '\\' + current_logfile
        _print_loop(log_full_path)
    #If no log file exists, keep checking
    else:
        time.sleep(.1)
        print_log_lines()
        
def handle_error(e):
    input('Unable to proceed: ' + str(e))
    quit()
        
if __name__ == '__main__':
    set_report_dir()
    
    check_thread = threading.Thread(group=None, target=check_for_rpt_file)
    parse_thread = threading.Thread(group=None, target=print_log_lines)
    
    check_thread.start()    
    parse_thread.start()
    
    check_thread.join()
    parse_thread.join()

    print('Execution complete. Program will now exit.')
