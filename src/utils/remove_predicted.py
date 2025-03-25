import json
# Read ground_truth.json file and assign it to data variable
with open('ground_truth.json', 'r') as file:
    data = json.load(file)

# Remove 'predicted_function' from each entry
for entry in data:
    if "predicted_function" in entry:
        del entry["predicted_function"]

# Convert back to JSON string
modified_json = json.dumps(data, indent=2)
with open('new_ground_truth.json', 'w') as file:
    file.write(modified_json)

