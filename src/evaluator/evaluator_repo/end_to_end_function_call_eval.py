from evaluator_repo.eval_utils.function_call_utils import compare_field, compare_full_match, compare_field_itemwise

class EndToEndFunctionCallEvaluator:
    def __init__(self):
        pass

    def __call__(self, expected, predicted, **kwargs): 
        return {
                "Plugin_name_accuracy": compare_field(expected, predicted, "plugin_name"), 
                "Function_name_accuracy": compare_field(expected, predicted, "function_name"),
                "Arguments_accuracy": compare_field(expected, predicted, "arguments"),
                "Itemwise_arguments_accuracy": compare_field_itemwise(expected, predicted, "arguments"),
                "Itemwise_plugin_accuracy": compare_field_itemwise(expected, predicted, "plugin_name"),
                "Overall_accuracy": compare_full_match(expected, predicted),
                } 