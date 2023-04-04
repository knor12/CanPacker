__author__      = "Noreddine Kessa"
__copyright__   = "!"
__license__ = "MIT License"

from Model import *
from ModelFrame import *
from ModelEnumType import *
from ModelSignal import *
from Utilities import *

class ModelChecker:

    def __init__(self, model):
        self.model = model
        self.SResultDescription="No errors"
 
    def check(self):
        if (not self.checkDoubleFrameNaming()) or \
        (not self.checkDoubleSignalNaming())or\
        (not self.checkOutOfRange())or\
        (not self.checkBitOverLap()):
            return False

        return True    

    def checkDoubleFrameNaming(self):
        for i, frameOut in enumerate(self.model.frames): 
            for j, frameIn in enumerate(self.model.frames):
                if  frameOut.name == frameIn.name and not (frameOut is frameIn):
                    self.SResultDescription=f'Error frame name {frameOut.name} duplicates'
                    return False
        return True
    
    def checkDoubleSignalNaming(self):
        for i, frame in enumerate(self.model.frames): 
            for signalOut in frame.signals:
                for signalIn in frame.signals:
                    if signalOut.name == signalIn.name and not (signalOut is signalIn):
                        self.SResultDescription=f'Error frame {frame.name}, signal name {signalOut.name} duplicates'
                        return False
        return True
    

    def checkOutOfRange(self):
        for i, frame in enumerate(self.model.frames):
             if frame.dataLength > 8:
                self.SResultDescription=f'Error frame {frame.name}, data length out of range'
                return False
             for signal in frame.signals:
                if signal.startbitAbsolue > 64-1:
                     self.SResultDescription=f'Error frame {frame.name}, signal name {signal.name} start out of range, {signal.startbitAbsolue}'
                     return False
                if (signal.startbitAbsolue + signal.bitLength) > 64:
                     self.SResultDescription=f'Error frame {frame.name}, signal name {signal.name} end out of range, {signal.startbitAbsolue + signal.bitLength}'
                     return False
        return True
    

    def checkBitOverLap(self):
        bitsOuts = []
        bitsIns = []
        for i, frame in enumerate(self.model.frames): 
            for signalOut in frame.signals:
                for signalIn in frame.signals:
                    if signalOut is signalIn:
                        continue

                    bitsOuts.clear()
                    for i in range(signalOut.startbitAbsolue, signalOut.startbitAbsolue + signalOut.bitLength):
                        #print(f'out push{i}')
                        bitsOuts.append(i)
                    bitsIns.clear()
                    for j in range(signalIn.startbitAbsolue, signalIn.startbitAbsolue + signalIn.bitLength):
                        #print(f'out push{i}')
                        bitsIns.append(j)

                    for bitIn in bitsIns:
                        for bitOut in bitsOuts: 
                            if bitIn == bitOut: 
                                self.SResultDescription=f'bit overlap: frame {frame.name}, signals {signalIn.name} and {signalOut.name}, bit number {bitIn}'
                                return False   

        return True


    def __str__(self):
        return self.SResultDescription
