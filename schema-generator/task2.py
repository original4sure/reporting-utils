import os
#name of the specific directory path
directory_path = '/home/shauryaswami/Documents/o4s-tasks/dsl-schema-main/schemas'
#name of all the files in the directory
files = os.listdir(directory_path)
#reading the files names which ends with .json
json_files = [file for file in files if file.endswith('.json')]
#printing all the files ending with .json
for json_file in json_files:
    print(json_file)
    