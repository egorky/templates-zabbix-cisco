import json

bfd_template_file = "zabbix_bfd_template.json"
corrected_count = 0

try:
    with open(bfd_template_file, "r") as f:
        bfd_data = json.load(f)
except FileNotFoundError:
    print(f"Error: {bfd_template_file} not found.")
    exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {bfd_template_file}.")
    exit(1)

if not bfd_data.get("zabbix_export", {}).get("templates"):
    print("Error: The template structure is missing the 'templates' array.")
    exit(1)

template = bfd_data["zabbix_export"]["templates"][0]

# Correct 'value_type' in standard items
if "items" in template:
    for item in template["items"]:
        if item.get("value_type") == "INTEGER":
            item["value_type"] = "UNSIGNED"
            corrected_count += 1
            print(f"Corrected value_type for item: {item.get('key', item.get('name'))}")

# Correct 'value_type' in item prototypes within discovery rules
if "discovery_rules" in template:
    for rule in template["discovery_rules"]:
        if "item_prototypes" in rule:
            for item_proto in rule["item_prototypes"]:
                if item_proto.get("value_type") == "INTEGER":
                    item_proto["value_type"] = "UNSIGNED"
                    corrected_count += 1
                    print(f"Corrected value_type for item prototype: {item_proto.get('key', item_proto.get('name'))}")

try:
    with open(bfd_template_file, "w") as f:
        json.dump(bfd_data, f, indent=4)
    print(f"Successfully corrected {corrected_count} 'value_type' fields to 'UNSIGNED' in {bfd_template_file}")
except IOError:
    print(f"Error: Could not write to {bfd_template_file}.")
    exit(1)

# For verification:
# with open(bfd_template_file, "r") as f:
#     print(f"Content of {bfd_template_file} after value_type correction:")
#     print(f.read())
