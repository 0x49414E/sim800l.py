from SMSHandler import SMSHandler
from PIDHandler import PIDHandler
import sys,signal,logging,argparse

def CTRL_C(sig, frame):
    print("[!] Exiting...");
    h.close();
    sys.exit(1);

def get_args():
    parser = argparse.ArgumentParser(prog="SIM800L HANDLER", description="Send an SMS through the CLI.");
    parser.add_argument("--phones", help="List of phone numbers separated by commas", required=True, dest="phones");
    parser.add_argument("--msg", help="Message to send", dest="msg",required=True);

    args = parser.parse_args();

    return [args.phones, args.msg];

signal.signal(signal.SIGINT,CTRL_C);

p = PIDHandler("config/config.ini", -1);
p.terminate();

def main():
    global h;
    try:
        phones, msg = get_args();
        phones = list(phones.split(","));
        h = SMSHandler("config/config.ini", phones, msg);
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