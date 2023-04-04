__author__      = "Noreddine Kessa"
__copyright__   = "!"
__license__ = "MIT License"


from Model import *
from Utilities import *

class SourceGenerator:

    def __init__(self, model):
        self.model = model
        self.CPPGuardStart = f'\n#ifdef __cplusplus \nextern \"C\" \n{{ \n#endif		/* __cplusplus */ \n'
        self.CPPGuardEnd = f'#ifdef __cplusplus\n}}\n#endif		/* __cplusplus */\n'


    def getSourceFile(self): 
        s = ""
        s += Utilities().getDisclamer(self.model)
        s += self.CPPGuardStart
        s +="\n\n"
        s += f'#include "{self.model.name}.h"'
        s += self.getIncludesC()
        s +="\n\n"
        s +="\n\n"
        s +=self.getPackersC()
        s +=self.getUnPackersC()
        s +="\n\n"
        s +="\n\n"
        s += self.CPPGuardEnd
        return s
    

    def getIncludesC(self): 
        s= ""; 
        for line in self.model.includes_c: 
            s+= f'\n{line}'
        return s
    
    def getPackersC(self):
        s="\n"
        for frame in self.model.frames: 
            s+="\n\n"
            #frame comment
            if frame.comment != "": 
                s+=  f'/* packing {frame.comment}*/\n'
            
            #packer name
            s+= f'bool {frame.name}_pack(\n    const uint32_t ID, \n    uint8_t * pU8Data'
            for index, signal in enumerate(frame.signals) : 
                comment = ""
                if signal.comment !="": 
                    comment = f'/*{signal.comment}*/'
                if signal.isConstant: 
                    s+=f'\n    /*{signal.dataType} {signal.name} */ {comment} /*is a constant no argument is used*/'
                elif signal.getter == "": 
                    s+=f',\n    const {signal.dataType}  {signal.name} {comment}'
                else: 
                    s+=f'\n    /*{signal.dataType}  {signal.name} */ {comment} /*value gotton from {signal.getter}()*/ '
            s+=')\n'

            #start of function body
            s+=f'{{\n'
            s+=f'    (void)ID; /*not used for now*/\n\n'
            #define variable for easy manip
            s+=f'    /*nothing to do if invalid data pointer provided*/\n'
            s+=f'    if (pU8Data==0){{return false;}}\n\n'
            s+=f'    uint64_t * pU64Data = (uint64_t *)(pU8Data);\n'
            s+=f'    * pU64Data = 0u;\n\n'

            #check if the CAN ID is correct
            #s+= f'    /*check ID match*/ \n'
            #s+= f'    if ({frame.ID} != ID){{return false}}; \n'

            for index, signal in enumerate(frame.signals) : 
                #pack the signal
                s+=f'\n    /*packing {signal.name}*/\n'
                if signal.isConstant:
                    s+=f'    *pU64Data = (*pU64Data ) | (((uint64_t)({signal.constantValue}&{self.getMaskFromBitLegth(signal.bitLength)}))<<{signal.startbitAbsolue});\n'
                
                elif signal.getter != "":
                    s+=f'    *pU64Data = (*pU64Data ) | (((uint64_t)({signal.getter}())& {self.getMaskFromBitLegth(signal.bitLength)})<<{signal.startbitAbsolue});\n'
                else: 
                    s+=f'     *pU64Data = (*pU64Data ) | (((uint64_t)({signal.name})& {self.getMaskFromBitLegth(signal.bitLength)})<<{signal.startbitAbsolue});\n'
        
            s+=f'    return true;\n'
            #end of function body
            s+=f'}}'


        return s

    

    def getMaskFromBitLegth(self,  bitLength):
    
        n = bitLength-1
        mask = 0
        while (n >-1):
            mask+= (1<<n)
            n-=1
        
        return hex( mask)

    def getUnPackersC(self):

        s="\n"
        for frame in self.model.frames: 
            s+="\n\n"
            #frame comment
            if frame.comment != "": 
                s+=  f'/* unpacking {frame.comment}*/\n'
            
            #packer name
            s+= f'bool {frame.name}_unpack(\n    const uint32_t ID, \n    const uint8_t * pU8Data'
            for index, signal in enumerate(frame.signals) : 
                comment = ""
                if signal.comment !="": 
                    comment = f'/*{signal.comment}*/'
                if signal.isConstant: 
                    s+=f'\n    /*{signal.dataType} {signal.name}*/ {comment} /*is a constant no argument is used*/'
                elif signal.setter == "": 
                    s+=f',\n    {signal.dataType} * {signal.name} {comment}'
                else: 
                    s+=f'\n    /*{signal.dataType} * {signal.name}*/ {comment} /*value set to {signal.setter}()*/ '
            s+=')\n'

            #start of function body
            s+=f'{{\n'
            #define variable for easy manip
            s+=f'    uint64_t * pU64Data = (uint64_t *)(pU8Data);\n\n'

            #check if the CAN ID is correct
            s+= f'    /*check ID match*/ \n'
            s+= f'    if ({frame.ID} != ID){{return false;}} \n'

            for index, signal in enumerate(frame.signals) : 
                #unpack the signal
                s+=f'\n    /*unpacking {signal.name}*/\n'
                s+=f'    {signal.dataType} {signal.name}_ = \
({signal.dataType})(((* pU64Data)>>{signal.startbitAbsolue})&{self.getMaskFromBitLegth(signal.bitLength)}); \n'
                
                #what to do with it
                #check if constant value is good
                if signal.isConstant:
                    s+=f'    if({signal.name}_!={signal.constantValue}){{return false;}}\n'
                
                #check if we have a setter
                if signal.setter != "":
                    s+=f'    {signal.setter}({signal.name}_);\n'
                elif not signal.isConstant: 
                    s+=f'    if ({signal.name} !=0){{* {signal.name} = {signal.name}_;}} \n'


            s+=f'    return true;\n'
            #end of function body
            s+=f'}}'
        return s
            


        