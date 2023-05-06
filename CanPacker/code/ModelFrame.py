__author__      = "Noreddine Kessa"
__copyright__   = "!"
__license__ = "MIT License"


from Utilities import *
from ModelSignal import *


class ModelFrame:

    def __init__(self, name=""):
        self.name =name
        self.ID = 0
        self.isTx = True
        self.isRX = True
        self.dataLength = 8
        self.comment = ""
        self.signals=[]
        self.utilities 	= Utilities()
        self.cyclicity = 0
        self.tx_on_change = False

    def __str__(self):
        
        s = f'frame name :  {self.name}, ID {self.ID}, isTx {self.isTx}, isRX {self.isRX}, dataLength {self.dataLength}, comment {self.comment}.\n'
        for signal in self.signals:
            s += self.utilities.indent(f'\t{signal}\n', 4)
        return s

    def acceptLine(self , line): 
        #preprocess
        pLine = line #.replace(' ', '')
        #pLine = pLine.replace('\t', '')

        #split
        words = pLine.split(",")  

        if len (words) >=2:


            #parse for signals
            if (words[1]=="$SIGNAL"):
                signal = ModelSignal()
                if signal.acceptLine(line):
                    self.signals.append(signal)
                    return True
                else: 
                    return False    
            #parse for a frame
            if (words[0] !="$FRAME"):
                return False
            
            #check if we have a valid frame name
            name = words[1]
            if name.isnumeric(): 
                print (f'invalid frame name {name}')
                return False
            self.name = name

            #process CAN ID
            ID =  words[2]
            if False: #not ID.isnumeric(): no need to check if CAN ID is numeric, it can be a call to a function or a define includes
                print (f'invalid frame ID {ID}')
                return False
            self.ID = ID

            #process direction TX and RX 
            direction = words[3]
            if 'TX' in direction.upper(): 
                self.isTx = True
            else:  
                self.isTx = False 

            if 'RX' in direction.upper(): 
                self.isRx = True
            else : 
                self.isRx = False
            
            if 'TX_ON_CHANGE' in direction.upper(): 
                self.tx_on_change = True

            #process data length
            dataLength = words[4]
            if not dataLength.isnumeric():
                print (f'invalid frame dataLength {dataLength}')
                return False
            self.dataLength = int(dataLength)

            #process comment
            self.comment = words[5]

            #process cyclicity
            if words[6].isnumeric():
                self.cyclicity = int(words[6]); 

            return True
        
            

                

        