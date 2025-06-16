import json
import uuid
import os

bfd_template_file = "zabbix_bfd_template.json"
ldp_template_file = "zabbix_mpls_ldp_template.json"

# 1. Read the existing BFD template
try:
    with open(bfd_template_file, "r") as f:
        base_template_data = json.load(f)
except FileNotFoundError:
    print(f"Error: Base template {bfd_template_file} not found.")
    exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {bfd_template_file}.")
    exit(1)

# 2. Perform a deep copy
ldp_template_data = json.loads(json.dumps(base_template_data))

# 3. Modify the template specific section for LDP
if not ldp_template_data.get("zabbix_export", {}).get("templates"):
    print("Error: The base template structure is missing the 'templates' array.")
    exit(1)

# Assuming there's only one template in the export to modify
ldp_template_object = ldp_template_data["zabbix_export"]["templates"][0]

# 4. Update top-level template metadata
ldp_template_object["uuid"] = uuid.uuid4().hex # Generate 32-char hex UUID
ldp_template_object["template"] = "SNMP MPLS LDP"
ldp_template_object["name"] = "SNMP MPLS LDP"
ldp_template_object["description"] = "Template for monitoring MPLS LDP (Label Distribution Protocol) using SNMP, based on MPLS-LDP-STD-MIB (RFC 3815)."

# Clear out BFD-specific content that will be replaced by LDP configurations
ldp_template_object["items"] = []
ldp_template_object["discovery_rules"] = []
ldp_template_object["valuemaps"] = []
ldp_template_object.pop("graphs", None) # Remove if it exists at template level
ldp_template_object.pop("dashboards", None) # Remove if it exists at template level

# The root level graphs/dashboards should have been cleared when BFD was made from OSPF.
# If any new root level elements were added to BFD template and are BFD specific, clear them here.
# For now, this focuses on the template object itself.

# 5. Create the new LDP template file
try:
    with open(ldp_template_file, "w") as f:
        json.dump(ldp_template_data, f, indent=4)
    print(f"Successfully created and initialized {ldp_template_file} from {bfd_template_file}")
except IOError:
    print(f"Error: Could not write to {ldp_template_file}.")
    exit(1)

# Verify by listing files
print("\nFiles in current directory:")
for item in os.listdir("."):
    print(item)

# Optional: print content of new file for verification snippet
# with open(ldp_template_file, "r") as f:
#     new_data = json.load(f)
#     print("\nSnippet of zabbix_mpls_ldp_template.json:")
#     print(f"Template Name: {new_data['zabbix_export']['templates'][0]['name']}")
#     print(f"Template UUID: {new_data['zabbix_export']['templates'][0]['uuid']}")
#     print(f"Number of items: {len(new_data['zabbix_export']['templates'][0]['items'])}")
#     print(f"Number of discovery_rules: {len(new_data['zabbix_export']['templates'][0]['discovery_rules'])}")
#     print(f"Number of valuemaps: {len(new_data['zabbix_export']['templates'][0]['valuemaps'])}")
