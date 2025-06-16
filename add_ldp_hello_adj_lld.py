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

if "discovery_rules" not in template:
    template["discovery_rules"] = []

# {#LDPHELLOADJKEY} will be EntityLdpId.EntityIndex.PeerLdpId.HelloAdjacencyIndex
hello_adj_item_prototypes = [
    {
        "uuid": uuid.uuid4().hex,
        "name": "LDP Hello Adjacency [{#LDPHELLOADJKEY}]: Hold Time Remaining",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.3.5.1.1.2.{#LDPHELLOADJKEY}", # mplsLdpHelloAdjacencyHoldTimeRem
        "key": "mplsLdpHelloAdjacencyHoldTimeRem[{#LDPHELLOADJKEY}]",
        "delay": "1m", "history": "7d", "trends": "365d", "value_type": "UNSIGNED", "units": "s",
        "description": "Time remaining for this Hello Adjacency [{#LDPHELLOADJKEY}] to receive its next Hello Message. (mplsLdpHelloAdjacencyHoldTimeRem)",
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Hello_Adj"}, {"tag": "LDP_Hello_Adj_Key", "value": "{#LDPHELLOADJKEY}"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "LDP Hello Adjacency [{#LDPHELLOADJKEY}]: Hold Time",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.3.5.1.1.3.{#LDPHELLOADJKEY}", # mplsLdpHelloAdjacencyHoldTime
        "key": "mplsLdpHelloAdjacencyHoldTime[{#LDPHELLOADJKEY}]",
        "delay": "1h", "history": "7d", "trends": "365d", "value_type": "UNSIGNED", "units": "s",
        "description": "Negotiated Hello hold time for adjacency {#LDPHELLOADJKEY}. 0 means default (15s Link, 45s Targeted), 65535 infinite. (mplsLdpHelloAdjacencyHoldTime)",
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Hello_Adj"}, {"tag": "LDP_Hello_Adj_Key", "value": "{#LDPHELLOADJKEY}"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "LDP Hello Adjacency [{#LDPHELLOADJKEY}]: Type",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.3.5.1.1.4.{#LDPHELLOADJKEY}", # mplsLdpHelloAdjacencyType
        "key": "mplsLdpHelloAdjacencyType[{#LDPHELLOADJKEY}]",
        "delay": "1h", "history": "7d", "trends": "365d", "value_type": "UNSIGNED",
        "description": "Type of Hello Adjacency (link or targeted) for {#LDPHELLOADJKEY}. (mplsLdpHelloAdjacencyType)",
        "valuemap": {"name": "MPLS LDP Hello Adjacency Type"},
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Hello_Adj"}, {"tag": "LDP_Hello_Adj_Key", "value": "{#LDPHELLOADJKEY}"}]
    }
]

# No specific triggers for this table in this pass, but could be added later (e.g., HoldTimeRem very low)
hello_adj_trigger_prototypes = []

ldp_hello_adj_discovery_rule = {
    "uuid": uuid.uuid4().hex,
    "name": "MPLS LDP Hello Adjacencies",
    "type": "SNMP_AGENT",
    "snmp_oid": "discovery[{#LDPHELLOADJKEY},.1.3.6.1.2.1.10.166.4.1.3.5.1.1.1]", # Discovering mplsLdpHelloAdjacencyIndex instances
    "key": "mplsLdpHelloAdjacency.discovery",
    "delay": "10m", "lifetime": "7d", # Adjust delay/lifetime as appropriate
    "description": "Discovery of MPLS LDP Hello Adjacencies (mplsLdpHelloAdjacencyTable). {#LDPHELLOADJKEY} is EntityLdpId.EntityIndex.PeerLdpId.HelloAdjacencyIndex.",
    "item_prototypes": hello_adj_item_prototypes,
    "trigger_prototypes": hello_adj_trigger_prototypes # Empty for now
}

template["discovery_rules"].append(ldp_hello_adj_discovery_rule)

try:
    with open(ldp_template_file, "w") as f:
        json.dump(ldp_data, f, indent=4)
    print(f"Successfully added MPLS LDP Hello Adjacencies discovery rule to {ldp_template_file}")
except IOError:
    print(f"Error: Could not write to {ldp_template_file}.")
    exit(1)
