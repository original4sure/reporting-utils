# This script reads JSON files containing schema information, generates JSON schemas
# based on the content, and saves the schemas to separate text files.
import json
import os
import glob

# Define the allowed destination type map
allowedDestTypeMap = {
    "String": "string",
    "LowCardinality(String)": "string",
    "DateTime64(0, 'UTC')": "integer",
    "DateTime": "integer",
    "UInt8": "integer",
    "UInt32": "integer",
    "UInt64": "integer",
    "Int64": "integer"
}

# Create a list of allowed destination types
allowedDestTypes = list(allowedDestTypeMap.keys())

def read_json_files(directory_path):
    """
    Read JSON files from a specified directory.
    """
    json_file_paths = glob.glob(os.path.join(directory_path, '*.json'))
    json_data_list = []

    for json_file_path in json_file_paths:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            schema = json.load(file)
            json_data_list.append((schema, json_file_path))

    return json_data_list

def generate_json_schemas(json_data_list):
    """
    Generate JSON schemas from a list of JSON objects.
    """
    json_schemas = []

    for schema, json_file_path in json_data_list:
        jsonSchema = {
            "type": "object",
            "properties": {}
        }

        items = schema.get("audit_logs", []) + schema.get("table_creation", [])

        for item in items:
            dest_datatype = item["dest_datatype"]
            dest_column = item["dest_column"]

            if dest_datatype in allowedDestTypes:
                jsonSchema["properties"][dest_column] = {
                    "type": allowedDestTypeMap[dest_datatype]
                }

        jsonSchemaString = json.dumps(jsonSchema, indent=2)
        json_schemas.append((jsonSchemaString, json_file_path))

    return json_schemas

def save_json_schemas_to_files(json_schemas, output_directory):
    """
    Save JSON schemas to separate text files.
    """
    os.makedirs(output_directory, exist_ok=True)

    for index, (json_schema, json_file_path) in enumerate(json_schemas):
        base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
        output_file_path = os.path.join(output_directory, f'{base_filename}_schema.txt')
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(json_schema)

        print(f"JSON Schema for {json_file_path} saved to {output_file_path}.")

def main():
    # directory where JSON files are located
    directory_path = '/home/bipinpreetsingh/Pythontasks/dsl-schema-main/schemas/'

    # output directory
    output_directory = '/home/bipinpreetsingh/Pythontasks/output/'

    json_data_list = read_json_files(directory_path)
    json_schemas = generate_json_schemas(json_data_list)
    save_json_schemas_to_files(json_schemas, output_directory)

if __name__ == "__main__":
    main()
