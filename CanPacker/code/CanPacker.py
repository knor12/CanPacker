__author__      = "Noreddine Kessa"
__copyright__   = "!"
__license__ = "MIT License"

from HeaderGenerator import *
from SourceGenerator import *
from Model import *
from ModelFrame import *
from ModelSignal import *
from ModelBuilder  import *
from Utilities import *
from ModelChecker import *
from GlueHeaderGenerator import *
import sys
import os
from pathlib import Path

if __name__ == "__main__":


    #process command line arguments for input configuration file
    file =  sys.argv[1]

    #check if file exists
    if not os.path.exists(file):
        print (f'Configuration file {file} not found')
        exit()
    
    
    path = file 

    
    
    #find the extension of the configuration file
    filename, file_extension = os.path.splitext(path)
    #print(f"file name={filename}, file extension={file_extension}")
    reader = 0
    if ".csv" == file_extension:
        modelBuilder = ModelBuilder(ConfigPath=path)
    else:
        print(f"extension of {path} not identified\n")
        exit( False)
        
    
    #read configuration
    
    if not modelBuilder.build(ConfigPath =path):
        print(f'error building the model from file.')
        exit()
        
    #print the model built
    model = modelBuilder.model
    print (f'{model}')

    #check the sanity of the model
    modelChecker = ModelChecker(model)
    if not modelChecker.check():
        print (f'{modelChecker}')
        exit()

    #print the header file
    headerGenerator = HeaderGenerator(model); 
    sHeader = headerGenerator.getHeaderFile()
    print(f'{sHeader}')


    #print the souce file
    sourceGenerator = SourceGenerator(model)
    sSource = sourceGenerator.getSourceFile()
    print(f'{sSource}')

    glueHeaderGenerator= GlueHeaderGenerator(model)
    sGlue = glueHeaderGenerator.getHeaderFile()
    print(f'{sGlue}')

    utilities =Utilities() 
    utilities.writeFile(fileName=f'{model.name}.h', content=sHeader)
    utilities.writeFile(fileName=f'{model.name}.c', content=sSource)

    if not os.path.exists(f'{model.name}_glue.h'): 
        utilities.writeFile(fileName=f'{model.name}_glue.h', content=sGlue)


    
