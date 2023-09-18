
import os
import json

#Directory where your JSON files are located
directory = '/home/shauryaswami/reporting-utils/schema-generator/dsl-schema-main/schemas'

#Output file where the combined SQL commands will be written
output_file = '/home/shauryaswami/reporting-utils/schema-generator/create_tables.sql'

def generate_create_table(json_data, table_name):
    create_table_sql = f'CREATE TABLE {table_name} (\n'
    for key, value in json_data.items():
        if isinstance(value, int) and 0 <= value <= 4294967295:
            data_type = 'UINT32'  # For values within the range of uint32
        elif isinstance(value, int):
            data_type = 'INTEGER'
        elif isinstance(value, float):
            data_type = 'FLOAT64'
        elif isinstance(value, str):
            data_type = 'TEXT'
        elif isinstance(value, bool):
            data_type = 'BOOLEAN'
        elif isinstance(value, list):
            data_type = 'ARRAY'  
        else:
            data_type = 'TEXT'  
            
    create_table_sql += f'    "{key}" {data_type},\n'
    create_table_sql = create_table_sql.rstrip(',\n') + '\n);'
    return create_table_sql

#Get a list of JSON files in the directory
json_files = [f for f in os.listdir(directory) if f.endswith('.json')]

#Open the output file for writing
with open(output_file, 'w') as outfile:
    for json_file in json_files:
        file_path = os.path.join(directory, json_file)
        table_name = os.path.splitext(json_file)[0]  # Use file name as table name
        with open(file_path, 'r') as json_data:
            data = json.load(json_data)
            create_table_sql = generate_create_table(data, table_name)
            outfile.write(f'-- Table for {json_file}\n')
            outfile.write(create_table_sql + '\n\n')

print(f'CREATE TABLE commands have been written to {output_file}')
