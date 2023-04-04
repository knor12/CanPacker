__author__      = "Noreddine Kessa"
__copyright__   = "!"
__license__ = "MIT License"


from ModelEnumItem import *
from Utilities import *

class ModelEnumType:

    def __init__(self, name=""):
        self.name =name
        self.typeName = ""
        self.enumItems = []
        self.comment = ""
        self.utilities = Utilities()
        
    def __str__(self):
        s = f'enumeration name :  {self.name},  typeName {self.typeName}, comment {self.comment}.\n'
        for enumItem in self.enumItems:
            s += self.utilities.indent(f'\t{enumItem}\n', 4)
        return s
        

    def acceptLine(self , line): 
        words = line.split(",")  
        if len (words) >=2:

            #check if we have an enum item
            if  (words[1]=="$ENUMITEM"):
                    enumItem = ModelEnumItem()
                    if  enumItem.acceptLine(line): 
                        self.enumItems.append(enumItem)
                        return True
                    else: 
                        print(f'error in line "{line}"')
                        return False
            

            #quick check of line header
            if (words[0] !="$ENUMTYPE"):
                return False
            
            #check if we have a valid frame name
            name = words[1]
            if name.isnumeric(): 
                print (f'invalid enumeration name {name}')
                return False
            self.name = name
            self.typeName = name

            #process value
            comment =  words[2]
            self.comment = comment

            return True
        
