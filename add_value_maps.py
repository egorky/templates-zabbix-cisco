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

if "valuemaps" not in bfd_template_object:
    bfd_template_object["valuemaps"] = []

# Check existing valuemap names to avoid duplicates if script is run multiple times
existing_valuemap_names = {vm.get("name") for vm in bfd_template_object["valuemaps"]}

new_valuemaps = []

# 1. SNMP BFD Admin Status
if "SNMP BFD Admin Status" not in existing_valuemap_names:
    new_valuemaps.append({
        "uuid": str(uuid.uuid4()),
        "name": "SNMP BFD Admin Status",
        "mappings": [
            {"value": "1", "newvalue": "enabled"},
            {"value": "2", "newvalue": "disabled"}
        ]
    })

# 2. SNMP Boolean (generic)
if "SNMP Boolean" not in existing_valuemap_names:
    new_valuemaps.append({
        "uuid": str(uuid.uuid4()),
        "name": "SNMP Boolean",
        "mappings": [
            {"value": "0", "newvalue": "false"},
            {"value": "1", "newvalue": "true"}
        ]
    })

# 3. SNMP BFD Session State
if "SNMP BFD Session State" not in existing_valuemap_names:
    new_valuemaps.append({
        "uuid": str(uuid.uuid4()),
        "name": "SNMP BFD Session State",
        "mappings": [
            {"value": "1", "newvalue": "adminDown"},
            {"value": "2", "newvalue": "down"},
            {"value": "3", "newvalue": "init"},
            {"value": "4", "newvalue": "up"}
        ]
    })

# 4. SNMP BFD Session Diag
if "SNMP BFD Session Diag" not in existing_valuemap_names:
    new_valuemaps.append({
        "uuid": str(uuid.uuid4()),
        "name": "SNMP BFD Session Diag",
        "mappings": [
            {"value": "0", "newvalue": "No Diagnostic"},
            {"value": "1", "newvalue": "Control Detection Time Expired"},
            {"value": "2", "newvalue": "Echo Function Failed"},
            {"value": "3", "newvalue": "Neighbor Signaled Session Down"},
            {"value": "4", "newvalue": "Forwarding Plane Reset"},
            {"value": "5", "newvalue": "Path Down"},
            {"value": "6", "newvalue": "Concatenated Path Down"},
            {"value": "7", "newvalue": "Administratively Down"},
            {"value": "8", "newvalue": "Reverse Concatenated Path Down"}
        ]
    })

# 5. SNMP BFD Session OperMode
if "SNMP BFD Session OperMode" not in existing_valuemap_names:
    new_valuemaps.append({
        "uuid": str(uuid.uuid4()),
        "name": "SNMP BFD Session OperMode",
        "mappings": [
            {"value": "1", "newvalue": "Asynchronous mode with Echo Function"},
            {"value": "2", "newvalue": "Asynchronous mode without Echo Function"}
        ]
    })

# 6. SNMP BFD Address Type
if "SNMP BFD Address Type" not in existing_valuemap_names:
    new_valuemaps.append({
        "uuid": str(uuid.uuid4()),
        "name": "SNMP BFD Address Type",
        "mappings": [
            {"value": "0", "newvalue": "Unknown"},
            {"value": "1", "newvalue": "IPv4"},
            {"value": "2", "newvalue": "IPv6"}
        ]
    })

bfd_template_object["valuemaps"].extend(new_valuemaps)

try:
    with open(bfd_template_file, "w") as f:
        json.dump(bfd_data, f, indent=4)
    print(f"Successfully added/updated BFD value maps in {bfd_template_file}")
except IOError:
    print(f"Error: Could not write to {bfd_template_file}.")
    exit(1)

# For verification:
# with open(bfd_template_file, "r") as f:
#     print(f"Content of {bfd_template_file} after adding value maps:")
#     print(f.read())
