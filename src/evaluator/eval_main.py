import os
import sys
from pathlib import Path

from run_eval import custom_eval
from utils.load_config import load_config
from utils.logger import logger 

# Ensure project root is in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def main():
    try:
        config = load_config()
        eval_config = config["evaluation"]
        logger.info("Evaluation config loaded successfully.")
    except Exception as e:
        logger.exception("Failed to load evaluation config.")
        return

    try:
        dataset_path = Path(__file__).resolve().parents[1]
        input_file = os.path.join(dataset_path, eval_config["input_path"], eval_config["input_file"])
        output_file = os.path.join(dataset_path, eval_config["output_path"], eval_config["output_file"])
        eval_name = eval_config["eval_name"]
        logger.info(f"Running evaluation '{eval_name}'")
    except KeyError as e:
        logger.exception(f"Missing evaluation config key: {e}")
        return
    except Exception as e:
        logger.exception("Failed to construct input/output paths.")
        return

    try:
        result = custom_eval(eval_name, input_file, output_file)
        logger.info(f"Evaluation completed. Output saved to {output_file}")
    except Exception as e:
        logger.exception("Evaluation step failed.")


if __name__ == "__main__":
    main()
