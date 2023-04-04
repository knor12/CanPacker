__author__      = "Noreddine Kessa"
__copyright__   = "!"
__license__ = "MIT License"


from ModelFrame import *
from ModelEnumType import *
from ModelSignal import *
from Utilities import *

class Model:

    def __init__(self, name=""):
        self.name =name
        self.includes_c = []
        self.includes_h = []
        self.frames=[]
        self.enumTypes=[]
        self.utilities = Utilities()
        self.sourceFile = ""

    def acceptLine(self , line): 
        words = line.split(",")  
        if len (words) >=2:
            if (words[0]=="$NAME"):
                self.name = words[1]
                return True

        return False   
    


    def __str__(self):
        s = f'model name : {self.name}, source file:{self.sourceFile}\n'
        
        s += f'model frames\n'
        sFrames = ""
        for frame in self.frames:
            sFrames+=f'{frame}'
        s += self.utilities.indent( sFrames, 4)
        
        s += f'model enumTypes\n'
        sEnumType = ""
        for enumeration in self.enumTypes:
            sEnumType +=f'{enumeration}'
        s += self.utilities.indent(f'{sEnumType}' , 10)

        s += f'model h_includes\n'
        sIncludesH = ""
        for i in self.includes_h:
            sIncludesH +=f'{i}\n'
        s += self.utilities.indent(f'{sIncludesH}' , 10)

        s += f'model c_includes\n'
        sIncludesC = ""
        for i in self.includes_c:
            sIncludesC +=f'{i}\n'
        s += self.utilities.indent(f'{sIncludesC}' , 10)

        return s
