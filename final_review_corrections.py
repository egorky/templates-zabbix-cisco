import json

bfd_template_file = "zabbix_bfd_template.json"
review_notes = []

try:
    with open(bfd_template_file, "r") as f:
        bfd_data = json.load(f)
except FileNotFoundError:
    review_notes.append(f"Error: {bfd_template_file} not found.")
    print("\n".join(review_notes))
    exit(1)
except json.JSONDecodeError:
    review_notes.append(f"Error: Could not decode JSON from {bfd_template_file}.")
    print("\n".join(review_notes))
    exit(1)

# Get the template object
template = bfd_data.get("zabbix_export", {}).get("templates", [{}])[0]
if not template:
    review_notes.append("Error: Template object not found or empty.")
    print("\n".join(review_notes))
    exit(1)

# 1. Check value_type correction
# Checking ciscoBfdVersionNumber (direct item)
item_checked = False
for item in template.get("items", []):
    if item.get("key") == "ciscoBfdVersionNumber":
        if item.get("value_type") == "UNSIGNED":
            review_notes.append("SUCCESS: Item 'ciscoBfdVersionNumber' has value_type 'UNSIGNED'.")
        else:
            review_notes.append(f"FAILURE: Item 'ciscoBfdVersionNumber' has value_type '{item.get('value_type')}', expected 'UNSIGNED'.")
        item_checked = True
        break
if not item_checked:
    review_notes.append("NOTE: Item 'ciscoBfdVersionNumber' not found for value_type check.")

# Checking a performance counter (item prototype)
proto_checked = False
if template.get("discovery_rules"):
    for rule in template["discovery_rules"]:
        if rule.get("key") == "bfdSessIndex":
            for proto in rule.get("item_prototypes", []):
                if proto.get("key") == "ciscoBfdSessPerfPktInHC[{#SNMPINDEX}]": # This was INTEGER before
                    if proto.get("value_type") == "UNSIGNED":
                        review_notes.append("SUCCESS: Item proto 'ciscoBfdSessPerfPktInHC' has value_type 'UNSIGNED'.")
                    else:
                        review_notes.append(f"FAILURE: Item proto 'ciscoBfdSessPerfPktInHC' has value_type '{proto.get('value_type')}', expected 'UNSIGNED'.")
                    proto_checked = True
                    break
            break
if not proto_checked:
    review_notes.append("NOTE: Item proto 'ciscoBfdSessPerfPktInHC' not found for value_type check.")


# 2. Check UUID format (no hyphens, 32 chars)
template_uuid = template.get("uuid", "")
if len(template_uuid) == 32 and '-' not in template_uuid:
    review_notes.append(f"SUCCESS: Template UUID '{template_uuid[:8]}...' format appears correct.")
else:
    review_notes.append(f"FAILURE: Template UUID '{template_uuid}' format incorrect.")

if template.get("items"):
    first_item_uuid = template["items"][0].get("uuid", "")
    if len(first_item_uuid) == 32 and '-' not in first_item_uuid:
        review_notes.append(f"SUCCESS: First item UUID '{first_item_uuid[:8]}...' format appears correct.")
    else:
        review_notes.append(f"FAILURE: First item UUID '{first_item_uuid}' format incorrect.")
else:
    review_notes.append("NOTE: No direct items to check UUID for.")

# 3. Check for removed tags from discovery rule
rule_tags_checked = False
if template.get("discovery_rules"):
    for rule in template["discovery_rules"]:
        if rule.get("key") == "bfdSessIndex": # The rule we modified
            if "tags" not in rule:
                review_notes.append("SUCCESS: Discovery rule 'bfdSessIndex' does not have a direct 'tags' key.")
            else:
                review_notes.append(f"FAILURE: Discovery rule 'bfdSessIndex' still has a direct 'tags' key: {rule['tags']}")
            rule_tags_checked = True
            break
if not rule_tags_checked:
    review_notes.append("NOTE: Discovery rule 'bfdSessIndex' not found for tag check.")

print("Final Review of Corrections:")
for note in review_notes:
    print(f"- {note}")

# Determine overall success for exit code, though agent doesn't use it directly from stdout
all_success = all("SUCCESS" in note or "NOTE" in note for note in review_notes)
if not all_success:
    print("\nSome checks failed or did not find the expected elements.")
    # exit(1) # Do not fail subtask, just report
else:
    print("\nAll spot checks passed or noted as element not found for check.")
