import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.evaluation import evaluate
from evaluator_repo.end_to_end_function_call_eval import EndToEndFunctionCallEvaluator
from utils.logger import logger  # ✅ Add logger

# Load environment variables
load_dotenv(override=True)

def custom_eval(name, data_path, output_path):
    """
    Evaluate the model using the given data and column mapping.
    """
    try:
        credential = DefaultAzureCredential()
        logger.info("Azure credential initialized.")
    except Exception as e:
        logger.exception("Failed to initialize Azure credentials.")
        return

    try:
        connection_string = os.environ["CONNECTION_STRING"]
        project = AIProjectClient.from_connection_string(
            conn_str=connection_string,
            credential=credential,
        )
        logger.info("Connected to Azure AI Project successfully.")
    except KeyError:
        logger.exception("Missing CONNECTION_STRING in environment variables.")
        return
    except Exception as e:
        logger.exception("Failed to connect to Azure AI Project.")
        return

    try:
        model_config = {
            "azure_endpoint": os.environ["AZURE_OPENAI_ENDPOINT"],
            "api_key": os.environ["AZURE_OPENAI_API_KEY"],
            "azure_deployment": os.environ["AZURE_OPENAI_DEPLOYMENT"],
            "api_version": os.environ["AZURE_OPENAI_API_VERSION"],
        }
        logger.info("Model configuration loaded.")
    except KeyError as e:
        logger.exception(f"Missing model config environment variable: {e}")
        return

    try:
        end_to_end_function_call_eval = EndToEndFunctionCallEvaluator()
        logger.info("End-to-end function call evaluator initialized.")

        result = evaluate(
            data=data_path,
            evaluation_name=name,
            evaluators={
                "end_to_end_function_call": end_to_end_function_call_eval
            },
            evaluator_config={
                "end_to_end_function_call": {
                    "column_mapping": {
                        "query": "${data.query}",
                        "expected": "${data.expected_function}",
                        "predicted": "${data.predicted_function}",
                        "response": "${data.predicted_response}"
                    }
                }
            },
            azure_ai_project=project.scope,
            output_path=output_path,
        )
        logger.info(f"Evaluation '{name}' completed. Results saved to {output_path}")
        return result
    except Exception as e:
        logger.exception("Evaluation failed.")
        return
