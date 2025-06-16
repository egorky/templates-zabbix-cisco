import json
import uuid

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

bfd_template_object = bfd_data["zabbix_export"]["templates"][0]

# Ensure 'items' list exists
if "items" not in bfd_template_object:
    bfd_template_object["items"] = []

# Define scalar items
scalar_items = [
    {
        "uuid": str(uuid.uuid4()),
        "name": "BFD Admin Status",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.4.1.9.10.137.1.1.1",
        "key": "ciscoBfdAdminStatus",
        "delay": "5m",
        "history": "7d", # Default history
        "trends": "365d", # Default trends
        "description": "The global administrative status of BFD in this router. The value enabled denotes that the BFD Process is active on at least one interface; disabled means it is not enabled on any interface.",
        "valuemap": {"name": "SNMP BFD Admin Status"},
        "tags": [{"tag": "Application", "value": "BFD"}]
    },
    {
        "uuid": str(uuid.uuid4()),
        "name": "BFD Version Number",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.4.1.9.10.137.1.1.3",
        "key": "ciscoBfdVersionNumber",
        "delay": "1h",
        "history": "7d",
        "trends": "365d",
        "value_type": "INTEGER", # Assuming this is a number
        "description": "The current default version number of the BFD protocol.",
        "tags": [{"tag": "Application", "value": "BFD"}]
    },
    {
        "uuid": str(uuid.uuid4()),
        "name": "BFD Session Notifications Enable",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.4.1.9.10.137.1.1.4",
        "key": "ciscoBfdSessNotificationsEnable",
        "delay": "5m",
        "history": "7d",
        "trends": "365d",
        "value_type": "INTEGER", # Assuming this is 0 or 1 / true or false
        "description": "Enables the emission of ciscoBfdSessUp and ciscoBfdSessDown notifications when set to true (1); otherwise these notifications are not emitted.",
        "valuemap": {"name": "SNMP Boolean"},
        "tags": [{"tag": "Application", "value": "BFD"}]
    }
]

# Add defined scalar items to the template
bfd_template_object["items"].extend(scalar_items)

# Save the updated template
try:
    with open(bfd_template_file, "w") as f:
        json.dump(bfd_data, f, indent=4)
    print(f"Successfully added scalar items to {bfd_template_file}")
except IOError:
    print(f"Error: Could not write to {bfd_template_file}.")
    exit(1)

# For verification:
# with open(bfd_template_file, "r") as f:
#     print(f"Content of {bfd_template_file} after adding scalar items:")
#     print(f.read())
