import os
import sys
import asyncio
import yaml
from utils.load_config import load_config
from utils.logger import logger

# Add the paths to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), 'datagenerator'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'datatransformer'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'evaluator'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'report'))

from datagenerator import device_control_agent
from datatransformer import data_transform
from evaluator import eval_main
from reportgenerator import generate_report

if __name__ == "__main__":
    try:
        config = load_config()
        pipeline_config = config['pipeline']['steps']
        logger.info(f"Pipeline config: {pipeline_config}")
    except Exception as e:
        logger.exception("Failed to load configuration.")
        sys.exit(1)

    if 'data_generation' in pipeline_config:
        try:
            logger.info("Executing device_control_agent")
            asyncio.run(device_control_agent.main())
            logger.info("device_control_agent executed")
        except Exception as e:
            logger.exception("device_control_agent step failed")

    if 'data_transformation' in pipeline_config:
        try:
            logger.info("Executing data_transform")
            data_transform.main()
            logger.info("data_transform executed")
        except Exception as e:
            logger.exception("data_transform step failed")

    if 'evaluation' in pipeline_config:
        try:
            logger.info("Executing eval_main")
            eval_main.main()
            logger.info("eval_main executed")
        except Exception as e:
            logger.exception("eval_main step failed")

    if 'reporting' in pipeline_config:
        try:
            logger.info("Executing report generation")
            generate_report.main()
            logger.info("report generation executed")
        except Exception as e:
            logger.exception("report generation step failed")

    logger.info("Pipeline executed (some steps may have failed).")
