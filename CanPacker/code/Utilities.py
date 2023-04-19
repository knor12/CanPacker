__author__      = "Noreddine Kessa"
__copyright__   = "!"
__license__ = "MIT License"



class Utilities:

    def __init__(self, name=""):
        self.name = name
        self.toolName = "CanPacker"
        self.version = "V0.05"

 
    
    def indent(self,st,  numSpaces):
        spaces = ""
        for i in range(numSpaces):
            spaces += " "
        #indent the first line
        ns = spaces + st
        #indent all other lines
        ns = ns.replace('\n', '\n' + spaces)

        #remove indentation after the last line
        ns+='\n'
        return ns 
    
    def removeWhiteSpace(self, s):
        s = s.replace(' ', '')
        s = s.replace('\t', '')
        return s
    

    def getDisclamer(self, model):
        from datetime import date        
        s = f"\
/*\n\
*this file is auto generated by  {self.toolName} version {self.version }.\n\
*@file {model.sourceFile}\n\
*@date {date.today()}\n\
*@author n.kessa\n\
*@brief frame packer/unpacker {model.sourceFile}\n\
*/\n\
\n\
\n\
\n"
        return s 
    

    def writeFile(self, fileName, content):
        with open(fileName, 'w') as f:
            f.write(content)


    def writeFileWithIndent(self, fileName, content, numSpaces):
        with open(fileName, 'w') as f:
            f.write(self.indent(content, numSpaces))


