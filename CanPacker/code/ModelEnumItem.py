__author__      = "Noreddine Kessa"
__copyright__   = "!"
__license__ = "MIT License"



class ModelEnumItem:

    def __init__(self, name=""):
        self.name =name
        self.value =""
        self.comment = ""
        
    def __str__(self):
        s = f'enumeration name :  {self.name}, value {self.value}, comment {self.comment}.\n'
        return s    

    def acceptLine(self , line): 
        words = line.split(",")  
        if len (words) >=2:
            #quick check of line header
            if (words[1] !="$ENUMITEM"):
                return False
            
            #check if we have a valid frame name
            name = words[2]
            if name.isnumeric(): 
                print (f'invalid enumeration name {name}')
                return False
            self.name = name

            #process value
            value =  words[3]
            self.value = value

            #process comment
            self.comment = words[4]

            
        else: 
            print(f"error parsing:{line}")
            return False

        return True
        

