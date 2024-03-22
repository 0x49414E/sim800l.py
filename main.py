import sys,signal
from SMSHandler import SMSHandler

def CTRL_C(sig, frame):
    print("[!] Exiting...");
    sys.exit(1);

signal.signal(signal.SIGINT,CTRL_C);

def main():
    h = SMSHandler("config/config.ini", "payload.ini");
    h.run();
    h.close();

if __name__ == '__main__':
    main();