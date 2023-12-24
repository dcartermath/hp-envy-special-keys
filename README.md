# HP Envy Special Keys
This project explains how to make the HP Command Center (HPCC) button (located on F12) on HP ENVY 15t-ep000 laptops open OmenMon instead of HP Command Center. Your mileage may vary on other laptop models.

It also allows for detection of the webcam shutter button (between the HPCC and power buttons), microphone mute button (F8), and the Fn+Esc keyboard combination. By default, it simply logs those keypresses into a log file, but the Python script can easily be edited to have different functionality.

## Installation and Usage
### Setting up Python
1. Download and install the latest version of [Python](https://www.python.org/downloads/). Take note of where the Python folder is installed.
2. Open a command prompt and run `cd "<Python folder location>\Scripts"` (replacing `<Python folder location>` with the actual location, i.e. `C:\...`).
3. Run `pip install wmi pyuac`. You can close the command prompt after it finishes installation.
### Setting up OmenMon
4. Download [OmenMon](https://github.com/OmenMon/OmenMon/releases) and extract the `.zip` file.
5. Navigate to `C:\Program Files` and make a new folder called `OmenMon`.
6. Put the contents of the OmenMon download in `C:\Program Files\OmenMon`. Now `C:\Program Files\OmenMon` should contain three files: `OmenMon.exe`, `OmenMon.sys`, `OmenMon.xml`.
### Setting up HP Envy Special Keys
7. Download `hpesk.pyw` from this repository.
8. Navigate to `C:\Program Files` and make a new folder called `HP Envy Special Keys`.
9. Put `hpesk.pyw` in `C:\Program Files\HP Envy Special Keys`.
### Setting up the Startup Task
10. Search for `Task Scheduler` in the Start Menu and open it.
11. Click `Create Task...` (on the right side of the screen, under `Actions`).
12. Set the following options:
- General
    - Name: `HP Envy Special Keys`.
    - Check `Run with highest privileges`.
    - Configure for: `<your Windows version>`.
- Triggers
    - Click `New...`.
    - Begin the task: `At log on`.
    - Click `OK`.
- Actions
    - Click `New...`.
    - Action: `Start a program`.
    - Program/script: `"<Python folder location>/pythonw.exe"`.
    - Add arguments: `"C:\Program Files\HP Envy Special Keys\hpesk.pyw"` (with the quotes).
    - Start in: `C:\Program Files\HP Envy Special Keys` (no quotes).
    - Click `OK`.
- Conditions
    - Uncheck everything.
- Settings
    - Uncheck `Stop the task if it runs longer than: ...`.
13. Click `OK`.
### Last Steps
14. Search for `HP Command Center` in the Start Menu. Right-click and press `Uninstall`.
15. Restart your computer.

If everything worked, then you should see an icon for OmenMon in the taskbar at bottom right of your screen, and pressing the HPCC button will open the OmenMon GUI. A log file is created at `C:\Program Files\HP Envy Special Keys\log.log`, which logs every time a special key is pressed.

## Stopping the script
1. Open Task Manager.
2. Go to the Details tab.
3. Select `pythonw.exe` and click `End task`.

## Technical Details
The way the HPCC key (and some of the other special keys) works is by writing a WMI event. This is detected by the HPCC background process, which then opens the HPCC GUI.

The WMI events are written to the `root\wmi` namespace and `hpqbevnt` class. Different keys are distinguished by the `EventId` and `EventData` properties. Here is a table of the combinations I know about:

| EventId | EventData | Meaning                     |
|---------|-----------|-----------------------------|
| 4       | 0         | Microphone mute (F8) toggle |
| 26      | 254       | Webcam shutter open         |
| 26      | 255       | Webcam shutter close        |
| 29      | 8614      | HPCC (F12) button           |
| 29      | 8615      | Fn+Esc                      |

Presumably one could send WMI events to control these functions programmatically, but I have not attempted it. This information may also be helpful if you want to detect these keypresses in an AutoHotKey script, for example.

This information was found by decompiling HPCC, similar to [this blog post](https://lantian.pub/en/article/modify-computer/reverse-engineered-linux-driver-for-hp-omen-macro-keys.lantian/) where an HP Omen user managed to restore macro key functionality on Linux.