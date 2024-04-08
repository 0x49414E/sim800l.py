from time import sleep
import sys, os, signal,logging

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
    with open("logs/module_status.log", "r+") as w:
        w.seek(0);
        w.truncate();
    sleep(10);
    try:
        h = SMSHandler("config/config.ini", "payload.ini");
        h.log_status();
        h.close();
        with open("./logs/ok.log", mode="w") as f:
            f.write("OK");
    except Exception as e:
        logger = logging.getLogger(__name__);
        with open("./logs/error.log", mode="w") as f:
            logging.basicConfig(filename='./logs/error.log', encoding='utf-8', level=logging.DEBUG, filemode='w', format='%(asctime)s %(message)s');
            logger.error(str(e));

if __name__ == "__main__":
    log()