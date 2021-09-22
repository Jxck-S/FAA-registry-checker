import configparser
import time
from colorama import Fore, Back, Style
import platform
import traceback
if platform.system() == "Windows":
    from colorama import init
    init(convert=True)
elif platform.system() == "Linux":
    pid_file_path = "./pid.pid"
    def write_pid_file(filepath):
        import os
        pid = str(os.getpid())
        f = open(filepath, 'w')
        f.write(pid)
        f.close()
    write_pid_file(pid_file_path)
    print("Made PIDFile")
from datetime import datetime
import pytz
import os
import signal
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
import sys
sys.path.extend([os.getcwd()])
#Dependency Handling
def download_dependency(url, file_name):
    try:
        import requests
        file_content = requests.get(url)
        open(("./dependencies/" + file_name), 'wb').write(file_content.content)
    except Exception as e:
        raise e("Error getting", file_name, "from", url)
    else:
        print("Successfully got", file_name)
def reget_dependencies():
    if not os.path.isdir("./dependencies/"):
        os.mkdir("./dependencies/")
    required_files = [('FAA_Reg_DB_Latest.zip', "https://registry.faa.gov/database/ReleasableAircraft.zip")]
    for file in required_files:
        file_name = file[0]
        url = file[1]
        if not os.path.isfile("./dependencies/" + file_name):
            print(file_name,  "does not exist downloading now")
            download_dependency(url, file_name)
        else:
            print("Already have", file_name, "deleting and redownloading")
            os.remove("./dependencies/" + file_name)
            download_dependency(url, file_name)

        import zipfile
        registry_zipped_file = './dependencies/FAA_Reg_DB_Latest.zip'
        with zipfile.ZipFile(registry_zipped_file, 'r') as zipObject:
            if os.path.isfile("./dependencies/MASTER.txt"):
                os.remove("./dependencies/MASTER.txt")
            if os.path.isfile("./dependencies/ACFTREF.txt"):
                os.remove("./dependencies/ACFTREF.txt")
            zipObject.extract("MASTER.txt", "./dependencies")
            zipObject.extract("ACFTREF.txt", "./dependencies")
import csv
def lookup_mfr_mdl_code(mdl_code):
    with open('./dependencies/ACFTREF.txt', 'r', encoding='utf-8-sig') as mfr_mdls_csv:
        mfr_mdls_csv = csv.DictReader(filter(lambda row: row[0]!='#', mfr_mdls_csv))
        for mdl in mfr_mdls_csv:
            if mdl['CODE'] == mdl_code:
                return mdl


main_config = configparser.ConfigParser()
print(os.getcwd())
main_config.read('./configs/mainconf.ini')
if main_config.getboolean('DISCORD', 'ENABLE'):
        from defDiscord import sendDis
        sendDis("Started", main_config)
def service_exit(signum, frame):
    if main_config.getboolean('DISCORD', 'ENABLE'):
        from defDiscord import sendDis
        sendDis("Service Stop", main_config)
    os.remove(pid_file_path)
    raise SystemExit("Service Stop")
signal.signal(signal.SIGTERM, service_exit)

try:
    import sys
    running_Count = 0
    failed_count = 0
    try:
        tz = pytz.timezone(main_config.get('TIME', 'TZ'))
        datetime_tz = datetime.now(tz)
    except pytz.exceptions.UnknownTimeZoneError:
        tz = pytz.UTC
        datetime_tz = datetime.now(tz)
    import json
    search_names =  json.loads(main_config.get('SEARCH', 'NAMES'))
    print("Search names", search_names)
    found_aircraft = []
    first_check = True
    while True:
        header = ("-------- " + str(running_Count) + " -------- " + str(datetime_tz.strftime("%I:%M:%S %p")) + " ---------------------------------------------------------------------------")
        print (Back.GREEN +  Fore.BLACK + header[0:100] + Style.RESET_ALL)
        if datetime_tz.hour == 0 and datetime_tz.minute == 0:
            running_Count = 0
        start_time = time.time()
        reget_dependencies()
        with open('./dependencies/MASTER.txt', 'r', encoding='utf-8-sig') as aircraft_master_csv:
            aircraft_master_csv = csv.DictReader(filter(lambda row: row[0]!='#', aircraft_master_csv))
            for reg in aircraft_master_csv:
                if reg['NAME'].strip() in search_names and reg['N-NUMBER'].strip() not in found_aircraft:
                    found_aircraft.append(reg['N-NUMBER'].strip())
                    if not first_check:
                        reg_ac_type = lookup_mfr_mdl_code(reg['MFR MDL CODE'])
                        message = "Found new reg for " + reg['NAME'].strip() + " N" + reg['N-NUMBER'].strip() + " a " + reg_ac_type['MFR'].strip() + " " + reg_ac_type['MODEL'].strip() + " https://registry.faa.gov/aircraftinquiry/Search/NNumberResult?NNumbertxt=" + reg['N-NUMBER']
                        print(message)
                        sendDis(message, main_config)
                    #print(json.dumps(reg, indent=2))
                    #print())
        print(len(found_aircraft), "Current Regs in searched names")
        first_check = False
        running_Count +=1
        elapsed_calc_time = time.time() - start_time
        footer = "-------- " + str(running_Count) + " -------- " + str(datetime_tz.strftime("%I:%M:%S %p")) + " ------------------------Elapsed Time- " + str(round(elapsed_calc_time, 3)) + " -------------------------------------"
        print (Back.GREEN + Fore.BLACK + footer[0:100] + Style.RESET_ALL)
        from datetime import time as dtime, datetime, timedelta, timezone
        hour = dtime(hour=5)
        if int(datetime.utcnow().strftime('%H')) >= 5:
            tmrw = datetime.utcnow().date() + timedelta(days=1)
            dt = datetime.combine(tmrw, hour, tzinfo=timezone.utc)
        else:
            dt = datetime.combine(datetime.utcnow().date(), hour, tzinfo=timezone.utc)
        import pause
        print("Sleeping till", dt)
        pause.until(dt)
except KeyboardInterrupt as e:
    print(e)
    if main_config.getboolean('DISCORD', 'ENABLE'):
        from defDiscord import sendDis
        sendDis(str("Manual Exit: " + str(e)), main_config)
except Exception as e:
    if main_config.getboolean('DISCORD', 'ENABLE'):
        try:
            os.remove('crash_latest.log')
        except OSError:
            pass
        import logging
        logging.basicConfig(filename='crash_latest.log', filemode='w', format='%(asctime)s - %(message)s')
        logging.Formatter.converter = time.gmtime
        logging.error(e)
        logging.error(str(traceback.format_exc()))
        from defDiscord import sendDis
        sendDis(str("Error Exiting: " + str(e)), main_config, "crash_latest.log")
    raise e
finally:
    if platform.system() == "Linux" and os.path.isfile(pid_file_path):
        os.remove(pid_file_path)