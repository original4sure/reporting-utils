import json
import os
import glob

# Specify the directory where the JSON files are located
directory_path = '/home/bipinpreetsingh/Pythontasks/dsl-schema-main/schemas/'

# Use glob to get a list of JSON files in the directory
json_file_paths = glob.glob(os.path.join(directory_path, '*.json'))

# Define the output directory where text files will be saved
output_directory = '/home/bipinpreetsingh/Pythontasks/dsl-schema-main/output/'

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

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

# Iterate over each JSON file
for json_file_path in json_file_paths:
    # Initialize the JSON schema for each file
    jsonSchema = {
        "type": "object",
        "properties": {}
    }

    # Read the JSON file
    with open(json_file_path, 'r', encoding='utf-8') as file:
        schema = json.load(file)

    # Concatenate the audit_logs and table_creation arrays
    items = schema.get("audit_logs", []) + schema.get("table_creation", [])

    # Iterate through each item
    for item in items:
        dest_datatype = item["dest_datatype"]
        dest_column = item["dest_column"]
        
        # Check if the dest_datatype is in allowedDestTypes
        if dest_datatype in allowedDestTypes:
            jsonSchema["properties"][dest_column] = {
                "type": allowedDestTypeMap[dest_datatype]
            }

    # Convert the resulting JSON schema to a JSON string
    jsonSchemaString = json.dumps(jsonSchema, indent=2)

    # Create the output text file path
    output_file_path = os.path.join(output_directory, os.path.basename(json_file_path).replace('.json', '.txt'))

    # Write the JSON schema to the output text file
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(f"JSON Schema for {json_file_path}:\n")
        output_file.write(jsonSchemaString)

    print(f"JSON Schema for {json_file_path} saved to {output_file_path}.")
