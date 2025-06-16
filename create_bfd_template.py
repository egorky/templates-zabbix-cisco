import json
import uuid
import os

# 1. Read the existing OSPF template
try:
    with open("zbx_export_templates.json", "r") as f:
        ospf_template_data = json.load(f)
except FileNotFoundError:
    print("Error: zbx_export_templates.json not found.")
    exit(1)
except json.JSONDecodeError:
    print("Error: Could not decode JSON from zbx_export_templates.json.")
    exit(1)

# 2. Create a new structure for the BFD template, deep copying the original
#    to preserve overall structure like version, date, and root groups.
bfd_template_data = json.loads(json.dumps(ospf_template_data))

# 3. Modify the template specific section for BFD
if not bfd_template_data.get("zabbix_export", {}).get("templates"):
    print("Error: The original template structure is missing the 'templates' array.")
    exit(1)

# Assuming there's only one template in the export to modify
bfd_template_object = bfd_template_data["zabbix_export"]["templates"][0]

# 4. Update top-level template metadata
bfd_template_object["uuid"] = str(uuid.uuid4())
bfd_template_object["template"] = "SNMP Cisco BFD"
bfd_template_object["name"] = "SNMP Cisco BFD"
bfd_template_object["description"] = "Template for monitoring Cisco BFD (Bidirectional Forwarding Detection) using SNMP. Based on ciscoIetfBfdMIB."
# Assuming the group "Templates" is fine. If not, this would need adjustment.
# bfd_template_object["groups"] = [{"name": "Templates"}] # Or some BFD specific group if desired

# Clear out specific content that will be replaced by BFD configurations
bfd_template_object["items"] = []
bfd_template_object["discovery_rules"] = []
bfd_template_object["valuemaps"] = []
# Graphs and dashboards might also need clearing if they are OSPF specific
# For now, let's clear graphs directly associated with the template object
bfd_template_object.pop("graphs", None) # Remove if it exists at this level
bfd_template_object.pop("dashboards", None) # Remove if it exists at this level

# Also clear root level graphs if they are specific to OSPF and not general.
# For this task, we assume root level graphs are not to be touched unless specified.
# If zbx_export_templates.json contains multiple templates, this logic would need to be more specific.

# Clear root-level graphs and dashboards as well
if "graphs" in bfd_template_data["zabbix_export"]:
    bfd_template_data["zabbix_export"]["graphs"] = []
if "dashboards" in bfd_template_data["zabbix_export"]:
    bfd_template_data["zabbix_export"]["dashboards"] = []


# 5. Create the new BFD template file
try:
    with open("zabbix_bfd_template.json", "w") as f:
        json.dump(bfd_template_data, f, indent=4)
    print("Successfully created and updated zabbix_bfd_template.json")
except IOError:
    print("Error: Could not write to zabbix_bfd_template.json.")
    exit(1)

# Verify by listing files
print("\nFiles in current directory:")
for item in os.listdir("."):
    print(item)

# Optional: print content of new file for verification
# with open("zabbix_bfd_template.json", "r") as f:
#     print("\nContent of zabbix_bfd_template.json:")
#     print(f.read())
