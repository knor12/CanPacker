__author__      = "Noreddine Kessa"
__copyright__   = "!"
__license__ = "MIT License"


from Model import *
from Utilities import *

class GlueHeaderGenerator:

    def __init__(self, model):
        self.model = model
        self.CPPGuardStart = f'\n#ifdef __cplusplus \nextern \"C\" \n{{ \n#endif		/* __cplusplus */ \n'
        self.CPPGuardEnd = f'\n\n#ifdef __cplusplus\n}}\n#endif		/* __cplusplus */\n'

        self.headerFileGuardStart = f'\n#ifndef {self.model.name.upper()}_GLUE \n#define {self.model.name.upper()}_GLUE\n'
        self.headerFileGuardEnd = f'\n#endif /*{self.model.name.upper()}_GLUE*/'


    def getHeaderFile(self): 
        s = ""
        s+= f'/*add {self.model.name} glue code here*/'
        s+=self.headerFileGuardStart
        s +="\n\n"
        s += self.CPPGuardStart
        s +="\n\n"
        s += self.CPPGuardEnd
        s +="\n\n"
        s +=self.headerFileGuardEnd
        return s
    

    