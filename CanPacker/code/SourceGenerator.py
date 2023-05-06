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
        s +="\n\n"
        s +=self.getUnPackersC()
        s +="\n\n"
        s+=self.getCyclicFunction(); 
        s +="\n\n"
        s+=self.getParserFunction();
        s +="\n\n"
        s += self.CPPGuardEnd
        return s
    

    def getIncludesC(self): 
        s= ""; 
        for line in self.model.includes_c: 
            s+= f'\n{line}'
        return s
    

    def getParserFunction(self): 
        s=""
        if not self.model.rx_function:
            return s
        
        #process variables that parsed
        for frame in self.model.frames: 
            if frame.isRX:
                #setters need to be defined signals in frames defined as RX frames
                for signal in frame.signals: 
                    if signal.setter == "" and not signal.isConstant:
                        print(f'error signal {signal.name} in frame {frame.name} is an rx signal but doesnt have a setter' ); 
                        exit (-1) 
        
        s+= "\n\n"
        s+=f'void {self.model.name}_parse(uint32_t id , uint8_t * pData)'
        s+='{'
        for frame in self.model.frames:
            fID = frame.ID 
            unpack = f'{frame.name}_unpack' #(\n    const uint32_t ID, \n    const uint8_t * pU8Data'
            if frame.isRX:
                s+= f'if({fID}==id){{ {unpack}(id, pData);  }}' 
        
        s+='}'
        return s

    def getCyclicFunction(self): 
        s=""
        if not self.model.tx_function:
            return s
        

        #global function names
        getTick = f'{self.model.name}_ticksMs'; 
        getTickSince = f'{self.model.name}_ticksSince'
        sendFrame = f'{self.model.name}_sendFrame'

        s+= "\n\n"
        s+= f'void {self.model.name}_cyclic(void)\n'
        s+='{\n'
        
        #process variables that are sent on change
        for frame in self.model.frames: 
            if frame.tx_on_change:
                #getters need to be defined for all frames sent on change
                for signal in frame.signals: 
                    if signal.getter == "" and not signal.isConstant:
                        print(f'error signal {signal.name} in frame {frame.name} is a sent on change frame but doesnt have a getter' ); 
                        exit (-1) 

                old_frame = f'u64{frame.name}_old_data'
                now_frame = f'u64{frame.name}_now_data'
                ID = f'{frame.ID}'
                dataLength = f'{frame.dataLength}'
                s+=f'/**send frame {frame.name} on change.**/\n' 
                s+=f'static uint64_t {old_frame} = 0;\n'
                s+=f'uint64_t {now_frame}  = 0;\n'
                s+='/*built the new frame*/\n'
                s+=f'{frame.name}_pack( {ID}, (uint8_t *)(&{now_frame}));\n'
                s+='/*see if frame has changed*/\n'
                s+=f'if ({old_frame} != {now_frame})\n'
                s+='{\n'
                s+=f'    /*send the frame*/\n'
                s+=f'    {self.model.name}_sendFrame({ID}, (uint8_t *) (&{now_frame}), {dataLength}, false);\n'
                s+=f'    /*save copy of data sent.*/\n'
                s+=f'    {old_frame} = {now_frame};\n'
                s+='}\n'

        #process cyclic functions
        for frame in self.model.frames: 
            counter = f'{frame.name}_counterMs'
            now_frame = f'u64{frame.name}_now_data'
            ID = f'{frame.ID}'
            if frame.cyclicity != 0:
                #getters need to be defined for all frames sent cyclicaly
                for signal in frame.signals: 
                    if signal.getter == "" and not signal.isConstant:
                        print(f'error signal {signal.name} in frame {frame.name} is in a cyclical frame but doesnt have a getter' ); 
                        exit (-1)
                s+=f'/**send frame {frame.name} cyclically.**/\n' 
                s+=f'/*define a counter*/\n'
                s+=f'static uint32_t {counter} = 0;\n'
                s+=f'/*initialize the counter*/\n'
                s+=f'if ({counter}==0){{{counter} = {getTick}(); }}\n'
                s+='/*see if the time is up for sendig the frame.*/\n'
                s+=f'if ({frame.cyclicity} <= {getTickSince}({counter}))'
                s+='{\n'
                s+=f'uint64_t {now_frame}  = 0;\n'
                s+='/*pack the frame to be sent*/\n'
                s+=f'{frame.name}_pack( {ID}, (uint8_t *)(&{now_frame}));\n'
                s+='/*send the frame*/\n'
                s+=f'{sendFrame}({ID}, (uint8_t *) (&{now_frame}));\n' 
                s+='/*reset the counter for next iteration*/\n'
                s+=f'{counter} = {getTick}(); '
                s+='}'


        s+='}\n\n'
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
            #identify a proper type before manipulating the frame data
            dataType = 'uint8_t'
            if frame.dataLength >1: 
                dataType = 'uint16_t'
            if frame.dataLength >2: 
                dataType = 'uint32_t'
            if frame.dataLength >4: 
                dataType = 'uint64_t'
                
            s+=f'    {dataType} * pData = ({dataType} *)(pU8Data);\n'
            s+=f'    * pData = 0u;\n\n'

            #check if the CAN ID is correct
            #s+= f'    /*check ID match*/ \n'
            #s+= f'    if ({frame.ID} != ID){{return false}}; \n'

            for index, signal in enumerate(frame.signals) : 
                #pack the signal
                s+=f'\n    /*packing {signal.name}*/\n'
                if signal.isConstant:
                    s+=f'    *pData = (*pData ) | (((uint64_t)({signal.constantValue}&{self.getMaskFromBitLegth(signal.bitLength)}))<<{signal.startbitAbsolue});\n'
                
                elif signal.getter != "":
                    s+=f'    *pData = (*pData ) | ((({dataType})({signal.getter}())& {self.getMaskFromBitLegth(signal.bitLength)})<<{signal.startbitAbsolue});\n'
                else: 
                    s+=f'     *pData = (*pData ) | ((({dataType})({signal.name})& {self.getMaskFromBitLegth(signal.bitLength)})<<{signal.startbitAbsolue});\n'
        
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
            #check for valid input
            s+=f'    /*nothing to do if invalid data pointer provided*/\n'
            s+=f'    if (pU8Data==0){{return false;}}\n\n'
            #define variable for easy manip
            s+=f'    uint64_t * pU64Data = (uint64_t *)(pU8Data);\n\n'

            #check if the CAN ID is correct
            s+= f'    /*check ID match*/ \n'
            if ('(' in frame.ID) and (')' in frame.ID ):#if an expression is used put it as is  
                s+=f'    if (!({frame.ID})){{return false;}} \n'
            elif frame.ID =='': #no frame ID specified
                pass 
            else: #frame value specified
                s+= f'    if ({frame.ID} != ID){{return false;}} \n'

            for index, signal in enumerate(frame.signals) : 
                #unpack the signal
                s+=f'\n    /*unpacking {signal.name}*/\n'
                s+=f'    {signal.dataType} _{signal.name} = \
({signal.dataType})(((* pU64Data)>>{signal.startbitAbsolue})&{self.getMaskFromBitLegth(signal.bitLength)}); \n'
                
                #what to do with it
                #check if constant value is good
                if signal.isConstant:
                    s+=f'    if(_{signal.name}!={signal.constantValue}){{return false;}}\n'
                
                #check if we have a setter
                if signal.setter != "":
                    s+=f'    {signal.setter}(_{signal.name});\n'
                elif not signal.isConstant: 
                    s+=f'    if ({signal.name} !=0){{* {signal.name} = _{signal.name};}} \n'


            s+=f'    return true;\n'
            #end of function body
            s+=f'}}'
        return s
    


            


        