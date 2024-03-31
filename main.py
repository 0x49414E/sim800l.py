from SMSHandler import SMSHandler
from PIDHandler import PIDHandler
import sys,signal,subprocess

def CTRL_C(sig, frame):
    print("[!] Exiting...");
    h.close();
    sys.exit(1);

signal.signal(signal.SIGINT,CTRL_C);

p = PIDHandler("config/config.ini", -1);
p.terminate();

def main():
    global h;
    h = SMSHandler("config/config.ini", "payload.ini");
    h.run();
    h.close();

    subprocess.Popen(["python", "status/check_status.py"], creationflags=subprocess.CREATE_NO_WINDOW, shell=True);

if __name__ == '__main__':
    main();