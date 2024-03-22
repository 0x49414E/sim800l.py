import serial, configparser,re
from pwn import log
from time import sleep

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
        self.p1 = log.progress("SMS Handler");
        self.data = "";
        self.run_count = 0;
    
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
                    self.p1.status(res.decode());
                    self.data = res.decode();
                    return;

    def send_sms(self):
        self.send_cmd(f"AT+CMGS=\"{self.phone}\"");
        self.send_cmd(self.message);
        self.write_ctrlz();

    def write_ctrlz(self):
        self.ser.write(bytes([26]));

    def close(self):
        self.ser.close();

    def run(self):
        try:
            self.send_cmd("AT", "OK");
            self.send_cmd("AT+CFUN=0");
            self.send_cmd("AT+CFUN=1", "SMS Ready");
            self.send_cmd("AT+CMGF=1");
            self.send_cmd("AT+CREG?", "0,1");

            creg_match = re.search(CREG_PATTERN, self.data);

            if creg_match:
                if(creg_match.group(2) == "1"):
                    pass;
                elif(creg_match.group(2) == "2"):
                    self.p1.status("[!] Error occurred...\n[!] AT+CREG responded with 0,2...");
                    self.run_count += 1;
                    if self.run_count >= 5:
                        raise Exception("Can't connect to GPRS network!");
                    self.run();

            self.send_sms();
        
        except Exception as e:
            self.p1.status(str(e)); 
            return;

