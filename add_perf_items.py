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

if "discovery_rules" not in bfd_template_object or not bfd_template_object["discovery_rules"]:
    print("Error: No discovery rules found in the template to add performance items to.")
    exit(1)

# Find the existing "BFD Sessions" discovery rule (assuming key "bfdSessIndex")
bfd_sessions_rule = None
for rule in bfd_template_object["discovery_rules"]:
    if rule.get("key") == "bfdSessIndex":
        bfd_sessions_rule = rule
        break

if not bfd_sessions_rule:
    print("Error: 'BFD Sessions' discovery rule with key 'bfdSessIndex' not found.")
    exit(1)

if "item_prototypes" not in bfd_sessions_rule:
    bfd_sessions_rule["item_prototypes"] = []

performance_item_prototypes = [
    {
        "uuid": str(uuid.uuid4()),
        "name": "BFD Session {#SNMPVALUE}: Perf Pkts In",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.4.1.9.10.137.1.3.1.1.{#SNMPINDEX}",
        "key": "ciscoBfdSessPerfPktIn[{#SNMPINDEX}]",
        "delay": "1m", "history": "7d", "trends": "365d", "value_type": "INTEGER",
        "description": "Total BFD messages received for session {#SNMPVALUE}.",
        "tags": [{"tag": "Application", "value": "BFD"}, {"tag": "BFD Session", "value": "{#SNMPVALUE}"}, {"tag": "BFD Performance", "value": "PacketsIn"}]
    },
    {
        "uuid": str(uuid.uuid4()),
        "name": "BFD Session {#SNMPVALUE}: Perf Pkts Out",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.4.1.9.10.137.1.3.1.2.{#SNMPINDEX}",
        "key": "ciscoBfdSessPerfPktOut[{#SNMPINDEX}]",
        "delay": "1m", "history": "7d", "trends": "365d", "value_type": "INTEGER",
        "description": "Total BFD messages transmitted for session {#SNMPVALUE}.",
        "tags": [{"tag": "Application", "value": "BFD"}, {"tag": "BFD Session", "value": "{#SNMPVALUE}"}, {"tag": "BFD Performance", "value": "PacketsOut"}]
    },
    {
        "uuid": str(uuid.uuid4()),
        "name": "BFD Session {#SNMPVALUE}: Uptime",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.4.1.9.10.137.1.3.1.3.{#SNMPINDEX}",
        "key": "ciscoBfdSessUpTime[{#SNMPINDEX}]",
        "delay": "5m", "history": "7d", "trends": "365d", "units": "uptime", "value_type": "INTEGER",
        "description": "SysUpTime of the most recent session up event for session {#SNMPVALUE}.",
        "tags": [{"tag": "Application", "value": "BFD"}, {"tag": "BFD Session", "value": "{#SNMPVALUE}"}, {"tag": "BFD Performance", "value": "Uptime"}]
    },
    {
        "uuid": str(uuid.uuid4()),
        "name": "BFD Session {#SNMPVALUE}: Last Down Time",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.4.1.9.10.137.1.3.1.4.{#SNMPINDEX}",
        "key": "ciscoBfdSessPerfLastSessDownTime[{#SNMPINDEX}]",
        "delay": "5m", "history": "7d", "trends": "365d", "units": "uptime", "value_type": "INTEGER",
        "description": "SysUpTime of the most recent session down event for session {#SNMPVALUE}.",
        "tags": [{"tag": "Application", "value": "BFD"}, {"tag": "BFD Session", "value": "{#SNMPVALUE}"}, {"tag": "BFD Performance", "value": "LastDownTime"}]
    },
    {
        "uuid": str(uuid.uuid4()),
        "name": "BFD Session {#SNMPVALUE}: Session Up Count",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.4.1.9.10.137.1.3.1.6.{#SNMPINDEX}",
        "key": "ciscoBfdSessPerfSessUpCount[{#SNMPINDEX}]",
        "delay": "5m", "history": "7d", "trends": "365d", "value_type": "INTEGER",
        "description": "Number of times session {#SNMPVALUE} has gone to 'up' state since router reboot.",
        "tags": [{"tag": "Application", "value": "BFD"}, {"tag": "BFD Session", "value": "{#SNMPVALUE}"}, {"tag": "BFD Performance", "value": "UpCount"}]
    },
    {
        "uuid": str(uuid.uuid4()),
        "name": "BFD Session {#SNMPVALUE}: Perf Pkts In (HC)",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.4.1.9.10.137.1.3.1.8.{#SNMPINDEX}",
        "key": "ciscoBfdSessPerfPktInHC[{#SNMPINDEX}]",
        "delay": "1m", "history": "7d", "trends": "365d", "value_type": "INTEGER", # Assuming Counter64, Zabbix handles it
        "description": "Total BFD messages received for session {#SNMPVALUE} (High Capacity).",
        "tags": [{"tag": "Application", "value": "BFD"}, {"tag": "BFD Session", "value": "{#SNMPVALUE}"}, {"tag": "BFD Performance", "value": "PacketsInHC"}]
    },
    {
        "uuid": str(uuid.uuid4()),
        "name": "BFD Session {#SNMPVALUE}: Perf Pkts Out (HC)",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.4.1.9.10.137.1.3.1.9.{#SNMPINDEX}",
        "key": "ciscoBfdSessPerfPktOutHC[{#SNMPINDEX}]",
        "delay": "1m", "history": "7d", "trends": "365d", "value_type": "INTEGER", # Assuming Counter64
        "description": "Total BFD messages transmitted for session {#SNMPVALUE} (High Capacity).",
        "tags": [{"tag": "Application", "value": "BFD"}, {"tag": "BFD Session", "value": "{#SNMPVALUE}"}, {"tag": "BFD Performance", "value": "PacketsOutHC"}]
    }
]

# Add dependent items for HC counters
dependent_item_prototypes = [
    {
        "uuid": str(uuid.uuid4()),
        "name": "BFD Session {#SNMPVALUE}: Perf Pkts In Rate (HC)",
        "type": "DEPENDENT",
        "key": "ciscoBfdSessPerfPktInRateHC[{#SNMPINDEX}]",
        "delay": "0", # Dependent items are calculated by Zabbix server
        "history": "7d", "trends": "365d", "value_type": "FLOAT", "units": "cps",
        "description": "Rate of BFD messages received for session {#SNMPVALUE} (High Capacity).",
        "preprocessing": [{"type": "CHANGE_PER_SECOND", "parameters": [""]}],
        "master_item": {"key": "ciscoBfdSessPerfPktInHC[{#SNMPINDEX}]"},
        "tags": [{"tag": "Application", "value": "BFD"}, {"tag": "BFD Session", "value": "{#SNMPVALUE}"}, {"tag": "BFD Performance", "value": "PacketsInRateHC"}]
    },
    {
        "uuid": str(uuid.uuid4()),
        "name": "BFD Session {#SNMPVALUE}: Perf Pkts Out Rate (HC)",
        "type": "DEPENDENT",
        "key": "ciscoBfdSessPerfPktOutRateHC[{#SNMPINDEX}]",
        "delay": "0",
        "history": "7d", "trends": "365d", "value_type": "FLOAT", "units": "cps",
        "description": "Rate of BFD messages transmitted for session {#SNMPVALUE} (High Capacity).",
        "preprocessing": [{"type": "CHANGE_PER_SECOND", "parameters": [""]}],
        "master_item": {"key": "ciscoBfdSessPerfPktOutHC[{#SNMPINDEX}]"},
        "tags": [{"tag": "Application", "value": "BFD"}, {"tag": "BFD Session", "value": "{#SNMPVALUE}"}, {"tag": "BFD Performance", "value": "PacketsOutRateHC"}]
    }
]

bfd_sessions_rule["item_prototypes"].extend(performance_item_prototypes)
bfd_sessions_rule["item_prototypes"].extend(dependent_item_prototypes)


try:
    with open(bfd_template_file, "w") as f:
        json.dump(bfd_data, f, indent=4)
    print(f"Successfully added BFD Session Performance item prototypes to the existing 'BFD Sessions' discovery rule in {bfd_template_file}")
except IOError:
    print(f"Error: Could not write to {bfd_template_file}.")
    exit(1)

# For verification:
# with open(bfd_template_file, "r") as f:
#     print(f"Content of {bfd_template_file} after adding performance items:")
#     print(f.read())
