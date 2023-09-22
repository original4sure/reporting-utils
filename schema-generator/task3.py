import os
import json
# Directory where your JSON files are located
directory = '/home/shauryaswami/Documents/o4s-tasks/dsl-schema-main/schemas'

# Output file where the combined SQL commands will be written
output_file = '/home/shauryaswami/Documents/o4s-tasks/create-tables.sql'

def generate_create_table(json_data, table_name):
    create_table_sql = f'CREATE TABLE {table_name} (\n'
    for item in json_data['table_creation']:
        key = item['dest_column']
        data_type = item['dest_datatype'].lower()  # Convert to lowercase for case-insensitive comparison
        if data_type == 'int' and 0 <= value <= 4294967295:
            data_type = 'UINT32'  # For values within the range of UINT32
        elif data_type == 'int':
            data_type = 'INTEGER'
        elif data_type == 'String' or data_type == 'string':
            data_type = 'TEXT'
        elif data_type == 'list':
            data_type = 'ARRAY'
        elif data_type == "DateTime64(3, 'UTC')":
            data_type = 'DATETIME'
        else:
            raise Exception(f"Unhandled datatype encountered: {data_type}")
            data_type = 'TEXT'  # Default to TEXT for unknown data types
        create_table_sql += f'    "{key}" {data_type},\n'
    create_table_sql = create_table_sql.rstrip(',\n') + '\n);'
    return create_table_sql

# Get a list of JSON files in the directory
json_files = [f for f in os.listdir(directory) if f.endswith('.json')]

# Open the output file for writing
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
