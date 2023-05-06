__author__      = "Noreddine Kessa"
__copyright__   = "!"
__license__ = "MIT License"


from Model import *
from Utilities import *

class HeaderGenerator:

    def __init__(self, model):
        self.model = model
        self.CPPGuardStart = f'\n#ifdef __cplusplus \nextern \"C\" \n{{ \n#endif		/* __cplusplus */ \n'
        self.CPPGuardEnd = f'\n\n#ifdef __cplusplus\n}}\n#endif		/* __cplusplus */\n'

        self.headerFileGuardStart = f'\n#ifndef {self.model.name.upper()} \n#define {self.model.name.upper()}\n'
        self.headerFileGuardEnd = f'\n#endif /*{self.model.name.upper()}*/'


    def getHeaderFile(self): 
        s = ""
        s+= Utilities().getDisclamer(self.model)
        s+=self.headerFileGuardStart
        s += self.CPPGuardStart
        s +="\n\n"
        s+= f'#include "{self.model.name}_glue.h"\n'
        s += self.getIncludesH()
        s +="\n\n"
        if self.model.tx_function:
            getTick = f'{self.model.name}_ticksMs'; 
            getTickSince = f'{self.model.name}_ticksSince'
            sendFrame = f'{self.model.name}_sendFrame'
            s+=f'/*user defined function return ticks elapsed in milliseconds since start of program execution */\n'
            s+=f'extern uint32_t {getTick}(void);\n\n'
            s+=f'/*user defined function return ticks elapsed in milliseconds since stampMs*/\n'
            s+=f'extern uint32_t {getTickSince}(uint32_t stampMs);\n\n'
            s+=f'/*user defined function that sends frames over the can bus */\n'
            s+=f'extern bool {sendFrame}(uint32_t id, uint8_t * pData);\n\n'

            s+='/*call this function cyclically to send out:\n\t-cyclic frames,\n\t-frames that are sent out when changed */\n'
            s+=f'void {self.model.name}_cyclic(void);'
            s +="\n\n"
        if self.model.rx_function:
            s+= "/*feed incoming frames to this function for processing*/\n"
            s+=f'void {self.model.name}_parse(uint32_t id , uint8_t * pData);'
            s +="\n\n"
        s += self.getEnumerations()
        s +="\n\n"
        s +="\n\n"
        s +=self.getPackersH()
        s +="\n\n"
        s +="\n\n"
        s+= self.getUnPackersH()
        s += self.CPPGuardEnd
        s +="\n\n"
        s +="\n\n"
        s +=self.headerFileGuardEnd
        return s
    

    def getIncludesH(self): 
        s= ""; 
        for line in self.model.includes_h: 
            s+= f'{line}\n'
        return s
    
    def getEnumerations(self ): 
        s=""
        #process one enumeration at a time
        for enumType in self.model.enumTypes:
            s+= f"typedef enum \n"
            s+= f"{{\n"
            
            for enumItem in enumType.enumItems: 
                comment = ""
                if enumItem.comment !="":
                    comment = f"/*{enumItem.comment}*/"
                s+= f"    {enumItem.name} = {enumItem.value},{comment}\n"

            s+= f"\n}} {enumType.typeName};\n"

        return s 

    def getPackersH(self):

        s="\n"
        for frame in self.model.frames: 
            s+="\n\n"
            #frame comment
            if frame.comment != "": 
                s+=  f'/*{frame.comment}*/\n'
            
            #packer name
            s+= f'bool {frame.name}_pack(\n    const uint32_t ID,\n    uint8_t * pData'
            for index, signal in enumerate(frame.signals) : 
                comment = ""
                if signal.comment !="": 
                    comment = f'/*{signal.comment}*/'
                if signal.isConstant: 
                    s+=f'\n    /*,const {signal.dataType} {signal.name} */ {comment} /*is a constant no argument is used*/'
                elif signal.getter == "": 
                    s+=f',\n    const {signal.dataType} {signal.name}  {comment}'
                else: 
                    s+=f'\n    /*,const  {signal.dataType} {signal.name} */ {comment} /*value taken from {signal.getter}(), */ '
            s+=');'



        return s
            



    def getUnPackersH(self):

        s="\n"
        for frame in self.model.frames: 
            s+="\n\n"
            #frame comment
            if frame.comment != "": 
                s+=  f'/*{frame.comment}*/\n'
            
            #packer name
            s+= f'bool {frame.name}_unpack(\n    const uint32_t ID,\n    const uint8_t * pData'
            for index, signal in enumerate(frame.signals) : 
                comment = ""
                if signal.comment !="": 
                    comment = f'/*{signal.comment}*/'
                if signal.isConstant: 
                    s+=f'\n    /*{signal.dataType} {signal.name} */ {comment} /*is a constant no argument is used*/'
                elif signal.setter == "": 
                    s+=f',\n    {signal.dataType} * {signal.name}  {comment}'
                else: 
                    s+=f'\n    /*{signal.dataType} * {signal.name} */ {comment} /*value set to {signal.setter}() */ '
            s+=');'



        return s