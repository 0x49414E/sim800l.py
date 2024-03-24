from time import sleep
import sys, os, signal

def ctrl_c(sig,frame):
    print("[!] Exiting...");
    sys.exit(1);

signal.signal(signal.SIGINT, ctrl_c);

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')));

from SMSHandler import SMSHandler

def log():
    while True:
        sleep(30);
        h = SMSHandler("config/config.ini", "payload.ini");
        h.log_status();
        h.close();

if __name__ == "__main__":
    log()