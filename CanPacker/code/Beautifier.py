import os
from os.path import exists

class Beautifier:

    def __init__(self, name='name'):
        self.name = name
        sourceDir = os.path.dirname(__file__)
        self.exe = f"{sourceDir}\\astyle-3.2.1-x64\\astyle.exe"
        #'.\\astyle-3.2.1-x64\\astyle.exe'
        if not exists(self.exe):
            print(f'file {self.exe} needed to run beatify')
            
        self.arg = "--style=allman  --indent=spaces=4 --break-blocks --delete-empty-lines"
    
    def beatify(self, filePath):
        cmd = f'{self.exe} {self.arg} {filePath}'
        print(f'executing {cmd}')

        if not exists(filePath):
            print(f'file {filePath} not found')
        
        ret = os.system(cmd)
        if (ret== 0):
            print (f'{filePath} formated ok')
        else:
            print (f'{filePath} error formatting ')
            
        
            
        
        
        
        
if __name__ == "__main__":
    print('before')
    beatifier = Beautifier()
    beatifier.beatify('org.c')
    print('after')
    
    
