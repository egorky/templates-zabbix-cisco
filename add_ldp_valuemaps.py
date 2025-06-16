import json
import uuid

ldp_template_file = "zabbix_mpls_ldp_template.json"

try:
    with open(ldp_template_file, "r") as f:
        ldp_data = json.load(f)
except FileNotFoundError:
    print(f"Error: {ldp_template_file} not found.")
    exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {ldp_template_file}.")
    exit(1)

if not ldp_data.get("zabbix_export", {}).get("templates"):
    print("Error: The template structure is missing the 'templates' array.")
    exit(1)

template = ldp_data["zabbix_export"]["templates"][0]

if "valuemaps" not in template:
    template["valuemaps"] = []

existing_valuemap_names = {vm.get("name") for vm in template["valuemaps"]}
valuemaps_to_add = []

def add_valuemap_if_not_exists(name, mappings_list):
    if name not in existing_valuemap_names:
        valuemaps_to_add.append({
            "uuid": uuid.uuid4().hex,
            "name": name,
            "mappings": mappings_list
        })
        existing_valuemap_names.add(name) # Add to set to prevent re-adding in same run
        return True
    return False

add_valuemap_if_not_exists("MPLS LDP Loop Detection Capable", [
    {"value": "1", "newvalue": "none"}, {"value": "2", "newvalue": "other"},
    {"value": "3", "newvalue": "hopCount"}, {"value": "4", "newvalue": "pathVector"},
    {"value": "5", "newvalue": "hopCountAndPathVector"}
])
add_valuemap_if_not_exists("MPLS LDP Entity Admin Status", [
    {"value": "1", "newvalue": "enable"}, {"value": "2", "newvalue": "disable"}
])
add_valuemap_if_not_exists("MPLS LDP Entity Oper Status", [
    {"value": "1", "newvalue": "unknown"}, {"value": "2", "newvalue": "enabled"},
    {"value": "3", "newvalue": "disabled"}
])
add_valuemap_if_not_exists("MPLS LDP Label Dist Method", [
    {"value": "1", "newvalue": "perPlatform"}, {"value": "2", "newvalue": "perInterface"}
])
add_valuemap_if_not_exists("MPLS LDP Label Retention Mode", [
    {"value": "1", "newvalue": "conservative"}, {"value": "2", "newvalue": "liberal"}
])
add_valuemap_if_not_exists("MPLS LDP Transport Addr Kind", [
    {"value": "1", "newvalue": "interface"}, {"value": "2", "newvalue": "loopback"}
])
# MIB TruthValue: 1=true, 2=false. Zabbix common boolean is 0=false, 1=true.
# Creating a specific "TruthValue" as per MIB.
add_valuemap_if_not_exists("TruthValue", [
    {"value": "1", "newvalue": "true"}, {"value": "2", "newvalue": "false"}
])
add_valuemap_if_not_exists("MPLS LDP Label Type", [
    {"value": "1", "newvalue": "generic"}, {"value": "2", "newvalue": "atm"},
    {"value": "3", "newvalue": "frameRelay"}
])
add_valuemap_if_not_exists("MPLS LDP Session State", [
    {"value": "1", "newvalue": "nonexistent"}, {"value": "2", "newvalue": "initialized"},
    {"value": "3", "newvalue": "openrec"}, {"value": "4", "newvalue": "opensent"},
    {"value": "5", "newvalue": "operational"}
])
add_valuemap_if_not_exists("MPLS LDP Session Role", [
    {"value": "1", "newvalue": "unknown"}, {"value": "2", "newvalue": "active"},
    {"value": "3", "newvalue": "passive"}
])
add_valuemap_if_not_exists("MPLS LDP Hello Adjacency Type", [
    {"value": "1", "newvalue": "link"}, {"value": "2", "newvalue": "targeted"}
])
add_valuemap_if_not_exists("MPLS FEC Type", [
    {"value": "1", "newvalue": "prefix"}, {"value": "2", "newvalue": "hostAddress"}
])
# InetAddressType is generic. The BFD template might have added "SNMP BFD Address Type".
# This one is specifically "InetAddressType" as often named in MIBs.
add_valuemap_if_not_exists("InetAddressType", [
    {"value": "0", "newvalue": "unknown"}, {"value": "1", "newvalue": "ipv4"},
    {"value": "2", "newvalue": "ipv6"}, {"value": "3", "newvalue": "ipv4z"},
    {"value": "4", "newvalue": "ipv6z"}, {"value": "16", "newvalue": "dns"} # Common ones
])

template["valuemaps"].extend(valuemaps_to_add)

try:
    with open(ldp_template_file, "w") as f:
        json.dump(ldp_data, f, indent=4)
    print(f"Successfully added/updated {len(valuemaps_to_add)} MPLS LDP specific value maps in {ldp_template_file}. Total valuemaps: {len(template['valuemaps'])}")
except IOError:
    print(f"Error: Could not write to {ldp_template_file}.")
    exit(1)

# For verification:
# with open(ldp_template_file, "r") as f:
#     data = json.load(f)
#     print("Current valuemaps:")
#     for vm in data["zabbix_export"]["templates"][0]["valuemaps"]:
#         print(f"  - {vm['name']}")
