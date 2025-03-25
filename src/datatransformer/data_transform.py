import json
import os
import sys
from pathlib import Path
from typing import Any

from utils.logger import logger
from utils.load_config import load_config
from utils.load_mapping_schema import load_mapping_schema

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def get_nested_value(d: dict, key_path: str) -> Any:
    """
    Safely get a nested value from a dictionary using dot notation like 'metadata.arguments'.
    Returns None if the key path doesn't exist.
    """
    keys = key_path.split('.')
    for key in keys:
        if isinstance(d, dict):
            d = d.get(key, {})
        else:
            return None
    return d or None


def replace_predicted_with_mapped(agent_data, mapping_schema):
    """
    Transforms the 'predicted_function' field of each agent output using a mapping schema.
    """
    source_key = mapping_schema["source_key"]
    field_mappings = mapping_schema["mappings"]

    output = []

    for item in agent_data:
        new_item = item.copy()
        mapped_functions = []

        for func in item.get(source_key, []):
            mapped_func = {}
            for source_field, target_field in field_mappings.items():
                value = get_nested_value(func, source_field)
                mapped_func[target_field] = value
            mapped_functions.append(mapped_func)

        new_item[source_key] = mapped_functions
        output.append(new_item)

    return output


def main():
    try:
        config = load_config()
        data_transform_config = config["data_transformation"]
        logger.info("Configuration loaded successfully.")
    except Exception as e:
        logger.exception("Failed to load configuration.")
        return

    try:
        dataset_path = Path(__file__).resolve().parents[1]
        input_file = os.path.join(dataset_path, data_transform_config["input_path"], data_transform_config["input_file"])
        output_file_json = os.path.join(dataset_path, data_transform_config["output_path"], data_transform_config["output_file_json"])
        output_file_jsonl = os.path.join(dataset_path, data_transform_config["output_path"], data_transform_config["output_file_jsonl"])
    except KeyError as e:
        logger.exception(f"Missing key in config: {e}")
        return

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            input_data = json.load(f)
        logger.info(f"Loaded input data from {input_file}")
    except Exception as e:
        logger.exception(f"Failed to read input file: {input_file}")
        return

    try:
        mapping_schema = load_mapping_schema()
        mapped_output = replace_predicted_with_mapped(input_data, mapping_schema)
        logger.info("Mapping transformation completed.")
    except Exception as e:
        logger.exception("Failed during mapping transformation.")
        return

    try:
        os.makedirs(os.path.dirname(output_file_json), exist_ok=True)

        with open(output_file_json, "w", encoding="utf-8") as f:
            json.dump(mapped_output, f, indent=2)
        logger.info(f"Transformed data written to {output_file_json}")

        with open(output_file_jsonl, "w", encoding="utf-8") as f:
            for item in mapped_output:
                f.write(json.dumps(item) + "\n")
        logger.info(f"Transformed data (JSONL) written to {output_file_jsonl}")

    except Exception as e:
        logger.exception("Failed to write output files.")


if __name__ == "__main__":
    main()
