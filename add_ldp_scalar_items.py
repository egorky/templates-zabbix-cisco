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

ldp_template_object = ldp_data["zabbix_export"]["templates"][0]

# Ensure 'items' list exists
if "items" not in ldp_template_object:
    ldp_template_object["items"] = []

# Define scalar items
scalar_items_to_add = [
    {
        "uuid": uuid.uuid4().hex,
        "name": "MPLS LDP LSR ID",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.1.1.0", # Added .0 for scalar instance
        "key": "mplsLdpLsrId",
        "delay": "1h", "history": "7d", "trends": "0d", # Store as text, no trends
        "value_type": "TEXT",
        "description": "The Label Switching Router's Identifier. (mplsLdpLsrId)",
        "tags": [{"tag": "Application", "value": "MPLS_LDP"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "MPLS LDP LSR Loop Detection Capable",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.1.2.0", # Added .0
        "key": "mplsLdpLsrLoopDetectionCapable",
        "delay": "1h", "history": "7d", "trends": "365d",
        "value_type": "UNSIGNED",
        "description": "An indication of whether this Label Switching Router supports loop detection. (mplsLdpLsrLoopDetectionCapable)",
        "valuemap": {"name": "MPLS LDP Loop Detection Capable"},
        "tags": [{"tag": "Application", "value": "MPLS_LDP"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "MPLS LDP Entity Last Change",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.2.1.0", # Added .0
        "key": "mplsLdpEntityLastChange",
        "delay": "5m", "history": "7d", "trends": "365d",
        "value_type": "UNSIGNED", "units": "unixtime",
        "description": "SysUpTime of the most recent add/delete or change to mplsLdpEntityTable. (mplsLdpEntityLastChange)",
        "tags": [{"tag": "Application", "value": "MPLS_LDP"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "MPLS LDP Entity Index Next",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.2.2.0", # Added .0
        "key": "mplsLdpEntityIndexNext",
        "delay": "1h", "history": "7d", "trends": "365d",
        "value_type": "UNSIGNED",
        "description": "Appropriate value for mplsLdpEntityIndex when creating entries. 0 means no unassigned entries. (mplsLdpEntityIndexNext)",
        "tags": [{"tag": "Application", "value": "MPLS_LDP"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "MPLS LDP Peer Last Change",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.3.1.0", # Added .0
        "key": "mplsLdpPeerLastChange",
        "delay": "5m", "history": "7d", "trends": "365d",
        "value_type": "UNSIGNED", "units": "unixtime",
        "description": "SysUpTime of the most recent add/delete to mplsLdpPeerTable/mplsLdpSessionTable. (mplsLdpPeerLastChange)",
        "tags": [{"tag": "Application", "value": "MPLS_LDP"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "MPLS FEC Last Change",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.3.8.1.0", # Added .0
        "key": "mplsFecLastChange",
        "delay": "5m", "history": "7d", "trends": "365d",
        "value_type": "UNSIGNED", "units": "unixtime",
        "description": "SysUpTime of the most recent add/delete or change to mplsLdpFecTable. (mplsFecLastChange)",
        "tags": [{"tag": "Application", "value": "MPLS_LDP"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "MPLS FEC Index Next",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.3.8.2.0", # Added .0
        "key": "mplsFecIndexNext",
        "delay": "1h", "history": "7d", "trends": "365d",
        "value_type": "UNSIGNED",
        "description": "Appropriate value for mplsFecIndex when creating entries. 0 means no unassigned entries. (mplsFecIndexNext)",
        "tags": [{"tag": "Application", "value": "MPLS_LDP"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "MPLS LDP LSP FEC Last Change",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.3.9.0", # Added .0
        "key": "mplsLdpLspFecLastChange",
        "delay": "5m", "history": "7d", "trends": "365d",
        "value_type": "UNSIGNED", "units": "unixtime",
        "description": "SysUpTime of the most recent add/delete or change to mplsLdpLspFecTable. (mplsLdpLspFecLastChange)",
        "tags": [{"tag": "Application", "value": "MPLS_LDP"}]
    }
]

# Add defined scalar items to the template
ldp_template_object["items"].extend(scalar_items_to_add)

# Save the updated template
try:
    with open(ldp_template_file, "w") as f:
        json.dump(ldp_data, f, indent=4)
    print(f"Successfully added {len(scalar_items_to_add)} MPLS LDP scalar items to {ldp_template_file}")
except IOError:
    print(f"Error: Could not write to {ldp_template_file}.")
    exit(1)

# For verification:
# with open(ldp_template_file, "r") as f:
#     print(f"Content of {ldp_template_file} after adding LDP scalar items:")
#     # print(f.read()) # Potentially large output
#     data = json.load(f)
#     print(f"Number of items: {len(data['zabbix_export']['templates'][0]['items'])}")
#     for item in data['zabbix_export']['templates'][0]['items']:
#         print(f"  Item: {item['name']}, Key: {item['key']}, OID: {item['snmp_oid']}")
