from psutil import pid_exists
import configparser,os,signal

class PIDHandler:
    def __init__(self,file,pid):
        self.config = self.read_config(file);
        self.old_pid = int(self.config['INIT']['PID']);
        self.new_pid = pid if pid != -1 else self.old_pid;

    def read_config(self,file):
        c = configparser.ConfigParser();
        c.read(file);
        return c;

    def terminate(self):
        if(pid_exists(self.old_pid)):
            os.kill(self.old_pid, signal.SIGTERM);

    def new(self):
        if(self.old_pid != self.new_pid):
            self.terminate();
        with open("config/config.ini", "w") as c:
            self.config['INIT']['PID'] = str(self.new_pid);
            self.old_pid = self.new_pid;
            self.config.write(c); 

