
import yaml
import os
import json

def load_mapping_schema():
    """
    Loads the mapping_schema.json file from the config folder and returns its contents as a dictionary.
    """
    schema_path = os.path.join(os.path.dirname(__file__), '../../config/mapping_schema.json')
    try:
        with open(schema_path, 'r') as file:
            schema = json.load(file)
        return schema
    except FileNotFoundError:
        raise FileNotFoundError(f"Mapping schema file not found at {schema_path}")
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Error parsing JSON file: {e}")