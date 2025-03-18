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

def compare_timestamps(old_stamp, new_stamp):
    old_date = parse_datetime(old_stamp)
    new_date = parse_datetime(new_stamp)
    return old_date < new_date #return true if old date is older
    
def parse_datetime(stamp):
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
    
def get_timestamp(file):
    dirty_timestamp = re.search(r"[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}-[0-9]{2}-[0-9]{2}.rpt", file) #get the end of the filename
    clean_timestamp = str(dirty_timestamp.group()).split('.')[0] #remove the .rpt
    return clean_timestamp

def parse_report_timestamp(file):
    global current_logfile
    global file_updated
    if current_logfile is None:
        current_logfile = file
        file_updated = True
        check_for_rpt_file() #Initialized, so start the loop again in case there are more
    else:
        old_file = get_timestamp(current_logfile) #inefficient -- should store the timestamp alongside the file to prevent constant matching
        new_file = get_timestamp(file)
        #Returns true if file is newer
        if old_file != new_file:
            if compare_timestamps(old_file, new_file):
                current_logfile = file
                file_updated = True

def check_for_rpt(file):
    if re.search(r".rpt", file):
        return True
    return False

def check_for_rpt_file():
    global file_updated
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
            
def print_log_lines():
    global current_logfile
    file_handler = None
    
    def _check_new_file():
        global file_updated
        global file_handler
        if file_updated is True:
            print('Newest .rpt file found: ' + str(current_logfile))
            file_handler = open(str(current_logfile), 'r')
            file_updated = False
            print_log_lines()            
    
    def _get_last_line(file_path):
        global file_handler
        ##NEED TO MOVE THIS AROUND - NEED TO ONLY WHEN FILE CHANGES
        last_line = deque(file_handler, maxlen=1).pop().strip()
        return last_line
    
    def _print_loop():
        global last_line_printed
        _check_new_file() #Make sure we're using the latest logfile
        this_line = _get_last_line(log_full_path)
        if this_line != last_line_printed:
            print(this_line)
            last_line_printed = this_line
        
    if current_logfile != None:
        log_full_path = str(get_report_dir()) + '\\' + current_logfile
        _print_loop()
    else: #Keep checking until there's a file
        time.sleep(.1)
        print_log_lines()
        
def handle_error(e):
    input('Unable to proceed: ' + str(e))
    quit()
        
if __name__ == '__main__':
    report_dir = get_report_dir()
    
    check_thread = threading.Thread(group=None, target=check_for_rpt_file)
    parse_thread = threading.Thread(group=None, target=print_log_lines)
    
    check_thread.start()    
    parse_thread.start()
    
    check_thread.join()
    parse_thread.join()

    print('Execution complete. Program will now exit.')
