from time import sleep
import serial, configparser,re, logging

CREG_PATTERN = r"\+CREG:\s*(\d+),(\d+)";

class SMSHandler:
    def __init__(self, config_file, payload_file):
        self.payload = self.load_payload(payload_file);
        self.config = self.read_config(config_file);
        self.phone = self.payload["Body"]["Number"];
        self.message = self.payload["Body"]["Message"];
        self.port = str(self.config['SIM800L']['SerialPort']);
        self.baudrate = int(self.config['SIM800L']['BaudRate']);
        self.ser = serial.Serial(self.port, self.baudrate, timeout=10);
        self.logger = logging.getLogger(__name__);
        self.data = "";
        self.run_count = 0;
        self.sending = 0;
    
    def read_config(self, config_file):
        config = configparser.ConfigParser();
        config.read(config_file); 
        return config;

    def load_payload(self, payload_file):
        payload = configparser.ConfigParser();
        payload.read(payload_file);
        return payload;
    
    def send_cmd(self, cmd, filter=""):
        while True:
            self.ser.write(f"{cmd}\r\n".encode());
            sleep(0.1);
            if self.ser.in_waiting > 0:
                res = self.ser.read(self.ser.in_waiting);
                if(filter.encode() in res):
                    self.data = re.sub(r'^>.*$', '', res.decode(), flags=re.MULTILINE);
                    if(self.sending == 0):
                        self.logger.info(f"\r[+] Command {cmd} sent! Received response:\n>> " + self.data);
                    elif(self.sending == 1):
                        self.logger.info(f"\r[+] Sending SMS to {self.phone}!\n");
                    return;

    def check_status(self):
        self.send_cmd("AT", "OK");
        self.send_cmd("AT+CFUN=0");
        self.send_cmd("AT+CFUN=1", "SMS Ready");
        self.send_cmd("AT+CMGF=1");
        self.send_cmd("AT+CREG?", "0,1");
        
    def log_status(self):
        logging.basicConfig(filename='./logs/module_status.log', encoding='utf-8', level=logging.DEBUG, filemode='w', format='%(asctime)s %(message)s');
        self.logger.info("\r[!] Logging status info!\r");
        self.check_status();

    def send_sms(self):
        self.sending = 1;
        self.send_cmd(f"AT+CMGS=\"{self.phone}\"");
        self.sending = 2;
        self.send_cmd(self.message);
        self.write_ctrlz();

    def write_ctrlz(self):
        self.ser.write(bytes([26]));

    def close(self):
        self.ser.close();

    def run(self):
        try:
            logging.basicConfig(filename='./logs/handler.log', encoding='utf-8', level=logging.DEBUG, filemode='w', format='%(asctime)s %(message)s')
            self.logger.info("\r[!] Logging SMS handler events!\r");
            self.check_status();

            creg_match = re.search(CREG_PATTERN, self.data);

            if creg_match:
                if(creg_match.group(2) == "1"):
                    pass;
                else:
                    self.logger.error(f"[!] Error occurred...\n[!] AT+CREG responded with 0,{creg_match.group(2)}...");
                    self.run_count += 1;
                    if self.run_count >= 5:
                        raise Exception("AT+CREG?: Can't connect to GPRS network!");
                    self.run();

            self.send_sms();
        
        except Exception as e:
            self.logger.error(str(e)); 
            return;

