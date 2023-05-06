__author__      = "Noreddine Kessa"
__copyright__   = "!"
__license__ = "MIT License"


from Model import *
from ModelEnumType import *
from ModelFrame import *
from ModelSignal import *


class ModelBuilder:

    def __init__(self, ConfigPath=""):
        self.ConfigPath =ConfigPath
        self.model = None
        
        
        
    def build(self , ConfigPath):
        self.ConfigPath = ConfigPath    
        file1 = open(ConfigPath, 'r')
        Lines = file1.readlines()

        #create Model object    
        model = Model()

        #add source file name
        model.sourceFile = self.ConfigPath

        #Strips the newline character
        frame = None
        enumType = None

        for line in Lines:
            #print (f"Processing line:{line}")
            words = line.split(",")
            #process two words lines
            if len (words) >=2:
                if (words[0]=="$NAME" or words[0]=="$TX_FUNCTION" or words[0]=="$RX_FUNCTION" ):
                    if not model.acceptLine(line): 
                        print(f'error in line "{line}"')
                        return False
                elif (words[0]=="$C_INCLUDE"):
                    model.includes_c.append(words[1])
                elif (words[0]=="$H_INCLUDE"):
                    model.includes_h.append(words[1])
                elif (words[0]=="$FRAME"):
                    frame = ModelFrame()
                    if not frame.acceptLine(line):
                        print(f'error in line "{line}"')
                        return False
                    model.frames.append(frame)
                elif (words[1]=="$SIGNAL"):
                    if not frame.acceptLine(line): 
                        print(f'error in line "{line}"')
                        return False

                elif (words[0]=="$ENUMTYPE"):
                    enumType = ModelEnumType()
                    if not enumType.acceptLine(line): 
                        print(f'error in line "{line}"')
                        return False
                    model.enumTypes.append(enumType)
                elif  (words[1]=="$ENUMITEM"):
                    if not enumType.acceptLine(line): 
                        print(f'error in line "{line}"')
                        return False
                                   
                    
        self.model = model
        return True