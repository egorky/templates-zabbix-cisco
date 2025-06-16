import json
import re

bfd_template_file = "zabbix_bfd_template.json"

# Regex to identify hyphenated UUIDs
# This regex is quite specific to the standard xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx format
UUID_REGEX = re.compile(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')

corrected_uuids_count = 0

def fix_uuids_recursive(data_node):
    global corrected_uuids_count
    if isinstance(data_node, dict):
        for key, value in data_node.items():
            if isinstance(value, str) and UUID_REGEX.match(value):
                data_node[key] = value.replace('-', '')
                corrected_uuids_count += 1
                # print(f"Corrected UUID for key '{key}': {data_node[key]}")
            else:
                fix_uuids_recursive(value)
    elif isinstance(data_node, list):
        for i, item in enumerate(data_node):
            if isinstance(item, str) and UUID_REGEX.match(item):
                data_node[i] = item.replace('-', '')
                corrected_uuids_count += 1
                # print(f"Corrected UUID in list at index {i}: {data_node[i]}")
            else:
                fix_uuids_recursive(item)

try:
    with open(bfd_template_file, "r") as f:
        bfd_data = json.load(f)
except FileNotFoundError:
    print(f"Error: {bfd_template_file} not found.")
    exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {bfd_template_file}.")
    exit(1)

# Start the recursive correction
fix_uuids_recursive(bfd_data)

try:
    with open(bfd_template_file, "w") as f:
        json.dump(bfd_data, f, indent=4)
    print(f"Successfully removed hyphens from {corrected_uuids_count} UUIDs in {bfd_template_file}")
except IOError:
    print(f"Error: Could not write to {bfd_template_file}.")
    exit(1)

# For verification:
# with open(bfd_template_file, "r") as f:
#     print(f"Content of {bfd_template_file} after UUID correction:")
#     # Be careful printing large files; maybe just a snippet or confirmation of structure
#     temp_data_check = json.load(f)
#     # Example check:
#     if temp_data_check.get("zabbix_export", {}).get("templates"):
#         first_template_uuid = temp_data_check["zabbix_export"]["templates"][0].get("uuid")
#         if first_template_uuid and '-' not in first_template_uuid and len(first_template_uuid) == 32:
#             print(f"First template UUID '{first_template_uuid}' appears corrected.")
#         else:
#             print(f"First template UUID '{first_template_uuid}' does NOT appear corrected.")
