import os
import json

# Directory where your JSON files are located
directory = '/home/shauryaswami/Documents/o4s-tasks/dsl-schema-main/schemas/'

# Output file where the combined SQL commands will be written
output_file = '/home/shauryaswami/reporting-utils/schema-generator/create_tables.sql'

def resolve_dest_datatype(dest_datatype: str):
    # Mapping of dest_datatype values to PostgreSQL data types
    datatype_mapping = {
        "string": 'TEXT',
        "datetime64(3, 'utc')": 'TIMESTAMP',
        "datetime": 'TIMESTAMP',
        'int': 'INTEGER',
        "lowcardinality(string)": 'STRING',
        "datetime64(0, 'utc')": 'INTEGER',
        "uint8": 'INTEGER',
        "uint32": 'INTEGER',
        "uint64" :'INTEGER',
        "int32": 'INTEGER',
        "float32": 'INTEGER',
        "float64": 'INTEGER',
        "int64": 'INTEGER',
        "array(string)": 'ARRAY',
        "array(float64)": 'ARRAY',
        "array(int64)": 'ARRAY',
        "map(string, string)": 'ARRAY'
    }
    print(f"getting {dest_datatype.lower()}")
    return datatype_mapping.get(dest_datatype.lower())  # Default to TEXT if not found

def generate_create_table(json_data, table_name):
    create_table_sql = f'CREATE TABLE {table_name} (\n'
    for item in json_data['table_creation']:
        key = item['dest_column']
        dest_datatype = item['dest_datatype'].lower()  # Convert to lowercase for case-insensitive comparison
        data_type = resolve_dest_datatype(dest_datatype)
        if not data_type:
            raise Exception(f"unhandled type: {dest_datatype}")
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
