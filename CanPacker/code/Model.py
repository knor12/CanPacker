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
        self.tx_function = False
        self.rx_function = False

    def acceptLine(self , line): 
        words = line.split(",")  
        if len (words) >=2:
            if (words[0]=="$NAME"):
                self.name = words[1]
                return True
            elif (words[0]=="$TX_FUNCTION"):
                if "TRUE" in words[1].upper():
                    self.tx_function = True
                    return True
            elif (words[0]=="$RX_FUNCTION"):
                if "TRUE" in words[1].upper():
                    self.rx_function = True
                    return True          

        return True   
    


    def __str__(self):
        s = f'model name : {self.name}, source file:{self.sourceFile}, tx_function={self.tx_function}, rx_function={self.rx_function}\n'
        
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
