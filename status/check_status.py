from time import sleep
import sys, os, signal, configparser

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')));
from PIDHandler import PIDHandler
from SMSHandler import SMSHandler

def ctrl_c(sig,frame):
    print("[!] Exiting...");
    sys.exit(1);

signal.signal(signal.SIGINT, ctrl_c);


# If there's a process active, kill the process and start a new one. Save the PID to the config.ini file.

pid = os.getpid();
p = PIDHandler("config/config.ini", -1);
p.terminate();
p.new_pid = pid;
p.new();


def log():
    while True:
        config = configparser.ConfigParser();
        config.read("config/config.ini");
        terminate = config['INIT']['terminate'];
        with open("logs/module_status.log", "r+") as w:
            if(int(terminate) == 1):
                p.terminate();
                break;
            elif(int(terminate) == 0):
                pass;
            w.seek(0);
            w.truncate();
        sleep(10);
        h = SMSHandler("config/config.ini", "payload.ini");
        h.log_status();
        h.close();

if __name__ == "__main__":
    log()