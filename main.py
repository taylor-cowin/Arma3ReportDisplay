from pathlib import Path
from pathlib import WindowsPath

def get_report_dir():
    home_path = Path.home()
    if type(home_path) is WindowsPath:
        expected_dir = WindowsPath(home_path,'AppData','Local','Arma 3')
        if expected_dir.exists():
            return expected_dir
        else:
            report_error('Could not find ' + str(expected_dir))
        
    else:
        report_error('This program can only be run on Windows machines.')
    
def report_error(e):
    input('Unable to proceed: ' + str(e))
    quit()
        
if __name__ == "__main__":
    report_dir = get_report_dir()