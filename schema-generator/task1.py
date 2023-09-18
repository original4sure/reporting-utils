import os
#the name of the specific directory path
path = '/home/shauryaswami/Documents/o4s-tasks/dsl-schema-main'
#list of all files in the directory
files = os.listdir(path)
#print all the files in the directory
for file in files:
    print(file)
    
    