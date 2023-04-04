__author__      = "Noreddine Kessa"
__copyright__   = "!"
__license__ = "MIT License"


from Utilities import *



class ModelSignal:

    def __init__(self, name=""):
        self.name =name
        self.startByte = 1000
        self.startBit= 1000
        self.bitLength = 1000
        self.isConstant = False
        self.constantValue = 10000
        self.dataType = ""
        self.setter = ""
        self.getter = ""
        self.comment = ""
        self.startbitAbsolue = self.startByte*8 +self.startBit
        self.utilities = Utilities()
        
    def __str__(self):
        
        s = f'signal name :  {self.name}, \
startByte {self.startByte},\
startBit {self.startBit},\
bitLength {self.bitLength},\
isConstant {self.isConstant}.\
constantValue {self.constantValue},\
dataType {self.dataType},\
setter {self.setter},\
getter {self.getter},\
absStartBit {self.startbitAbsolue },\
comment {self.comment},\n'
        
        return s

    def acceptLine(self , line): 
        #preprocess
        pLine = line#.replace(' ', '')
        #pLine = pLine.replace('\t', '')

        #split
        words = pLine.split(",")  

        if len (words) >=2:
            #quick check of line header
            if (words[1] !="$SIGNAL"):
                return False
            
            #check if we have a valid frame name
            name = words[2]
            if name.isnumeric(): 
                print (f'invalid frame name {name}')
                return False
            self.name = name

            #process start byte
            startByte = words[3]
            if startByte.isnumeric():
                self.startByte = int(startByte)
            else:   
                print (f'invalid start byte {startByte}')
                return False

            #process start bit
            startBit = words[4]
            if startBit.isnumeric():
                self.startBit = int(startBit)
            else:
                print (f'invalid start bit {startBit}')
                return False

            #process bitLength
            bitLength = words[5]
            if bitLength.isnumeric():
                self.bitLength = int(bitLength)
            else:
                print (f'invalid length {bitLength}')
                return False

            #process constant value
            constantValue = words[6]
            self.constantValue = constantValue
            if constantValue !="": 
                self.isConstant = True

        
            #process datatype
            self.dataType = words[7]

            #process setter
            self.setter =   self.utilities.removeWhiteSpace(words[8]) 

            #process getter
            self.getter =   self.utilities.removeWhiteSpace(words[9])

            #process comment
            self.comment =   words[10]

            self.startbitAbsolue = self.startByte*8 +self.startBit

            return True



        
            

                

        