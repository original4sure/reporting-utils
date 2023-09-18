import os
import json

#Directory where your JSON files are located
input_directory = '/home/shauryaswami/Documents/o4s-tasks/dsl-schema-main/schemas'

#Output file where the combined SQL commands will be written
output_file = '/home/shauryaswami/Documents/o4s-tasks/create_tables.sql'

#Initialize an empty string to store SQL commands
sql_commands = ''

#Loop through files in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith('.json'):
        file_path = os.path.join(input_directory, filename)

        # Read and parse the JSON file
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)

        # Generate the CREATE TABLE command based on the JSON structure
        table_name = filename.split('.')[0]
        create_table_sql = f"CREATE TABLE {table_name} (\n"
        for key, value in data.items():
            # Determine the data type based on the value type 
            data_type = "TEXT" if isinstance(value, str) else \
                        "INTEGER" if isinstance(value, int) else \
                        "NUMERIC" if isinstance(value, float) else "TEXT"

            create_table_sql += f"    {key} {data_type},\n"

        create_table_sql = create_table_sql.rstrip(',\n')  
        create_table_sql += "\n);\n\n"

        # Append the CREATE TABLE command to the running list
        sql_commands += create_table_sql

#Write the combined SQL commands to the output file
with open(output_file, 'w') as f:
    f.write(sql_commands)

print(f'SQL commands written to {output_file}')
