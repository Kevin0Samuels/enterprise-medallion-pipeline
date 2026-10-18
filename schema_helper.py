import sys
import os
import pyarrow.orc as orc
import yaml

def generate_bronze_yaml(file_path, table_name):
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found at {file_path}")
        return
    
    # Inspect schema of the raw ORC file using PyArrow
    orc_file = orc.ORCFile(file_path)
    schema = orc_file.schema
    
    columns = []
    for name in schema.names:
        field = schema.field(name)
        columns.append({
            "name": name,
            "type": str(field.type)
        })
        
    # Construct draft configuration dictionary
    config = {
        "version": "1.0",
        "table_name": f"bronze_{table_name}",
        "format": "ORC",
        "partitions": ["organisation_id", "processing_date"],
        "columns": columns,
        "s3_path_pattern": f"http://minio:9000/bronze/{table_name}/{{organisation_id}}/{{processing_date}}/data.orc"
    }
    
    # Write to a draft YAML configuration file
    yaml_filename = f"bronze_{table_name}_config.yaml"
    with open(yaml_filename, "w") as f:
        yaml.dump(config, f, sort_keys=False)
        
    print(f"\nSuccessfully generated draft YAML config: {yaml_filename}\n")
    print("--- Generated YAML Preview ---")
    print(yaml.dump(config, sort_keys=False))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 schema_helper.py <path_to_orc_file> <table_name>")
        print("Example: python3 schema_helper.py data_output/users/org_101/2026-10-06/data.orc users")
        sys.exit(1)
        
    file_arg = sys.argv[1]
    table_arg = sys.argv[2]
    generate_bronze_yaml(file_arg, table_arg)
