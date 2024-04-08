from SMSHandler import SMSHandler
from PIDHandler import PIDHandler
import sys,signal,logging

def CTRL_C(sig, frame):
    print("[!] Exiting...");
    h.close();
    sys.exit(1);

signal.signal(signal.SIGINT,CTRL_C);

p = PIDHandler("config/config.ini", -1);
p.terminate();

def main():
    global h;
    try:
        h = SMSHandler("config/config.ini", "payload.ini");
        h.run();
        h.close();
        with open("./logs/ok.log", mode="w") as f:
            f.write("OK");
    except Exception as e:
        logger = logging.getLogger(__name__);
        with open("./logs/error.log", mode="w") as f:
            logging.basicConfig(filename='./logs/error.log', encoding='utf-8', level=logging.DEBUG, filemode='w', format='%(asctime)s %(message)s');
            logger.error(str(e));

if __name__ == '__main__':
    main();