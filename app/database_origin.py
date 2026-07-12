import json
import os

shipments = {}

# Locate shipments.json relative to this file
base_dir = os.path.dirname(os.path.abspath(__file__))
shipments_file_path = os.path.join(base_dir, "shipments.json")

# Load from .json file
with open(shipments_file_path) as json_file:
    data = json.load(json_file)

    # Map as dictionary
    for value in data:
        shipments[value["id"]] = value


# Save changes to .json file
def save():
    with open(shipments_file_path, "w") as json_file:
        json.dump(
            # Convert to list of shipments
            list(shipments.values()),
            json_file,
        )

