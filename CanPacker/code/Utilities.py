__author__      = "Noreddine Kessa"
__copyright__   = "!"
__license__ = "MIT License"



class Utilities:

    def __init__(self, name=""):
        self.name = name
        self.toolName = "CanPacker"
        self.version = "V0.01"

 
    
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
        s="/*\n"
        s+= f"* Generated using  {self.toolName} version {self.version }.\n"
        s+= f"* Description file used is {model.sourceFile}, edit the description, the regenerate the source code, do not edit this file manualy.\n"
        s+="*/"
        return s 
    

    def writeFile(self, fileName, content):
        with open(fileName, 'w') as f:
            f.write(content)


    def writeFileWithIndent(self, fileName, content, numSpaces):
        with open(fileName, 'w') as f:
            f.write(self.indent(content, numSpaces))

