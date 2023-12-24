import os
import subprocess
from datetime import datetime
import logging
import wmi
from pyuac import main_requires_admin

#Based on:
# https://stackoverflow.com/questions/1813872/running-a-process-in-pythonw-with-popen-without-a-console
def launchWithoutConsole(command, args):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    return subprocess.Popen([command] + args, startupinfo=startupinfo)

@main_requires_admin
def main():
    logging.basicConfig(filename=r'C:\Program Files\HP Envy Special Keys\log.log',
                        encoding='utf-8', level=logging.DEBUG)
    logging.info(f'[{datetime.now()}] Process started')
    
    os.chdir(r'C:\Program Files\OmenMon')
    omen_process = launchWithoutConsole(r'OmenMon.exe', [])
    logging.info(f'[{datetime.now()}] OmenMon started, pid={omen_process.pid}')
    
    c = wmi.WMI(namespace=r'root\wmi')
    watcher = c.hpqbevnt.watch_for()
    while True:
        event = watcher()
        event_id = event.wmi_property('EventId').value
        event_data = event.wmi_property('EventData').value
        match (event_id, event_data):
            case (4, 0):
                logging.info(f'[{datetime.now()}] Detected mic_mute_toggle')
            case (26, 254):
                logging.info(f'[{datetime.now()}] Detected camera_on')
            case (26, 255):
                logging.info(f'[{datetime.now()}] Detected camera_off')
            case (29, 8614):
                logging.info(f'[{datetime.now()}] Detected hpcc')
                # Re-launching OmenMon opens the OmenMon GUI.
                # The new process terminates by itself automatically.
                launchWithoutConsole(r'OmenMon.exe', [])
            case (29, 8615):
                logging.info(f'[{datetime.now()}] Detected fn_esc')
            case _:
                logging.info(f'[{datetime.now()}] Detected unknown event {event_id}:{event_data}')

if __name__ == "__main__":
    main()
