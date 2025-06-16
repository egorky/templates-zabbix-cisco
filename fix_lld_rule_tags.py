import json

bfd_template_file = "zabbix_bfd_template.json"

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
removed_tags_count = 0

if "discovery_rules" in template:
    for i, rule in enumerate(template["discovery_rules"]):
        if "tags" in rule: # Check if the rule object itself has a 'tags' key
            # To be safe, let's check if it's the specific problematic tag structure
            # or just any tag. The user's report was specific, but generally,
            # discovery rules don't have direct tags like items/prototypes do.
            print(f"Found 'tags' directly under discovery rule '{rule.get('name', 'Unnamed Rule ' + str(i))}'. Removing it.")
            print(f"Tag content was: {json.dumps(rule['tags'])}")
            del rule["tags"]
            removed_tags_count += 1

try:
    with open(bfd_template_file, "w") as f:
        json.dump(bfd_data, f, indent=4)
    if removed_tags_count > 0:
        print(f"Successfully removed direct 'tags' from {removed_tags_count} discovery rule object(s) in {bfd_template_file}")
    else:
        print(f"No direct 'tags' found on discovery rule objects in {bfd_template_file}. No changes made for this step.")
except IOError:
    print(f"Error: Could not write to {bfd_template_file}.")
    exit(1)

# For verification:
# with open(bfd_template_file, "r") as f:
#     print(f"Content of {bfd_template_file} after removing discovery rule tags:")
#     # print(f.read()) # Potentially large output
#     data_check = json.load(f)
#     if data_check.get("zabbix_export", {}).get("templates",[{}])[0].get("discovery_rules"):
#         first_rule_tags = data_check["zabbix_export"]["templates"][0]["discovery_rules"][0].get("tags")
#         if first_rule_tags is None:
#             print("Verified: First discovery rule does not have a direct 'tags' key.")
#         else:
#             print(f"Verification FAILED: First discovery rule still has direct 'tags': {first_rule_tags}")
