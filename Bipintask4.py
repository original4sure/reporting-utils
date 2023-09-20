import os
import json

def list_json_files(directory):
    json_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    return json_files

def json_to_avro_schema(json_data):
    avro_schema = {
        "type": "record",
        "name": "Example",
        "fields": []
    }
    
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            field = {
                "name": key,
                "type": ["null", "string"] if value is None else "string" if isinstance(value, str) else "int" if isinstance(value, int) else "double" if isinstance(value, float) else "boolean" if isinstance(value, bool) else json_to_avro_schema(value)
            }
            avro_schema["fields"].append(field)
    elif isinstance(json_data, list):
        if json_data:
            avro_schema["fields"].append({
                "name": "items",
                "type": ["null", json_to_avro_schema(json_data[0])]
            })

    return avro_schema

def main(directory):
    json_files = list_json_files(directory)

    if not json_files:
        print("No JSON files found in the specified directory.")
        return

    avro_schema_dir = '/home/bipinpreetsingh/Pythontasks/dsl-schema-main/avro_schemas/'  # Directory to save Avro schema files

    # Create the output directory if it doesn't exist
    if not os.path.exists(avro_schema_dir):
        os.makedirs(avro_schema_dir)

    for json_filename in json_files:
        with open(json_filename, 'r') as json_file:
            json_data = json.load(json_file)
        
        # Infer the Avro schema from JSON data
        avro_schema = json_to_avro_schema(json_data)

        # Create the Avro schema file name
        avro_schema_filename = os.path.splitext(os.path.basename(json_filename))[0] + '.avsc'
        avro_schema_file_path = os.path.join(avro_schema_dir, avro_schema_filename)

        # Save the Avro schema to a file
        with open(avro_schema_file_path, 'w') as avro_schema_file:
            json.dump(avro_schema, avro_schema_file, indent=4)

        print(f"Created Avro schema: {avro_schema_file_path}")

if __name__ == '__main__':
    input_directory = '/home/bipinpreetsingh/Pythontasks/dsl-schema-main/schemas/'  # Replace with the path to your directory
    main(input_directory)
