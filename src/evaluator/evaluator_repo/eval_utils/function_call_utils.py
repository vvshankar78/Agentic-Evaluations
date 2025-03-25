def compare_full_match(expected, predicted):
    """Returns True if expected and predicted functions fully match (order-sensitive)."""
    return expected == predicted

def compare_field(expected, predicted, field):
    """
    Compare specific field (e.g., 'plugin_name' or 'arguments') between two function lists.
    Returns True if all items match field-wise (order-sensitive).
    """
    expected_fields = [func.get(field) for func in expected]
    predicted_fields = [func.get(field) for func in predicted]
    return expected_fields == predicted_fields

def compare_field_itemwise(expected, predicted, field):
    """
    Returns a list of 1s and 0s indicating field-wise match for each item.
    1 = match, 0 = no match
    """
    result = []

    # Case 1: predicted is empty
    if not predicted:
        return [0] * len(expected)

    # Case 2: length mismatch
    if len(expected) != len(predicted):
        return [0] * len(expected)

    # Case 3: field-by-field comparison
    for e, p in zip(expected, predicted):
        result.append(1 if e.get(field) == p.get(field) else 0)

    return result