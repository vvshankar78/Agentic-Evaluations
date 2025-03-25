import yaml
import os
import json

def load_config():
    """
    Loads the config.yaml file from the config folder and returns its contents as a dictionary.
    """
    config_path = os.path.join(os.path.dirname(__file__), '../../config/config.yaml')
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found at {config_path}")
    except yaml.YAMLError as e:
        raise RuntimeError(f"Error parsing YAML file: {e}")
    
