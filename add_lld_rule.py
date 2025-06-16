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

if "discovery_rules" not in bfd_template_object:
    bfd_template_object["discovery_rules"] = []

item_prototypes = [
    {
        "uuid": str(uuid.uuid4()),
        "name": "BFD Session {#SNMPVALUE}: Application ID",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.4.1.9.10.137.1.2.1.2.{#SNMPINDEX}",
        "key": "ciscoBfdSessApplicationId[{#SNMPINDEX}]",
        "delay": "5m", "history": "7d", "trends": "365d",
        "description": "Application ID for BFD session {#SNMPVALUE}.",
        "tags": [{"tag": "Application", "value": "BFD"}, {"tag": "BFD Session", "value": "{#SNMPVALUE}"}]
    },
    {
        "uuid": str(uuid.uuid4()),
        "name": "BFD Session {#SNMPVALUE}: Local Discriminator",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.4.1.9.10.137.1.2.1.3.{#SNMPINDEX}",
        "key": "ciscoBfdSessDiscriminator[{#SNMPINDEX}]",
        "delay": "5m", "history": "7d", "trends": "365d",
        "description": "Local discriminator for BFD session {#SNMPVALUE}.",
        "tags": [{"tag": "Application", "value": "BFD"}, {"tag": "BFD Session", "value": "{#SNMPVALUE}"}]
    },
    {
        "uuid": str(uuid.uuid4()),
        "name": "BFD Session {#SNMPVALUE}: Remote Discriminator",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.4.1.9.10.137.1.2.1.4.{#SNMPINDEX}",
        "key": "ciscoBfdSessRemoteDiscr[{#SNMPINDEX}]",
        "delay": "5m", "history": "7d", "trends": "365d",
        "description": "Remote discriminator for BFD session {#SNMPVALUE}.",
        "tags": [{"tag": "Application", "value": "BFD"}, {"tag": "BFD Session", "value": "{#SNMPVALUE}"}]
    },
    {
        "uuid": str(uuid.uuid4()),
        "name": "BFD Session {#SNMPVALUE}: UDP Port",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.4.1.9.10.137.1.2.1.5.{#SNMPINDEX}",
        "key": "ciscoBfdSessUdpPort[{#SNMPINDEX}]",
        "delay": "1h", "history": "7d", "trends": "365d",
        "description": "UDP Port for BFD session {#SNMPVALUE}. Default is well-known port.",
        "tags": [{"tag": "Application", "value": "BFD"}, {"tag": "BFD Session", "value": "{#SNMPVALUE}"}]
    },
    {
        "uuid": str(uuid.uuid4()),
        "name": "BFD Session {#SNMPVALUE}: State",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.4.1.9.10.137.1.2.1.6.{#SNMPINDEX}",
        "key": "ciscoBfdSessState[{#SNMPINDEX}]",
        "delay": "1m", "history": "7d", "trends": "365d",
        "description": "Perceived state of BFD session {#SNMPVALUE}. (1:adminDown, 2:down, 3:init, 4:up)",
        "valuemap": {"name": "SNMP BFD Session State"},
        "tags": [{"tag": "Application", "value": "BFD"}, {"tag": "BFD Session", "value": "{#SNMPVALUE}"}]
    },
    {
        "uuid": str(uuid.uuid4()),
        "name": "BFD Session {#SNMPVALUE}: Remote Heard Flag",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.4.1.9.10.137.1.2.1.7.{#SNMPINDEX}",
        "key": "ciscoBfdSessRemoteHeardFlag[{#SNMPINDEX}]",
        "delay": "1m", "history": "7d", "trends": "0d", # Often boolean, trends might not be needed
        "description": "Status of BFD packet reception from the remote system for session {#SNMPVALUE}. (1:true, 0:false). Applicable for BFD version 0.",
        "valuemap": {"name": "SNMP Boolean"},
        "tags": [{"tag": "Application", "value": "BFD"}, {"tag": "BFD Session", "value": "{#SNMPVALUE}"}]
    },
    {
        "uuid": str(uuid.uuid4()),
        "name": "BFD Session {#SNMPVALUE}: Diagnostic Code",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.4.1.9.10.137.1.2.1.8.{#SNMPINDEX}", # Note: MIB says 'accessible only for notifications'
        "key": "ciscoBfdSessDiag[{#SNMPINDEX}]",
        "delay": "5m", "history": "7d", "trends": "365d",
        "description": "Diagnostic code for last session transition for BFD session {#SNMPVALUE}.",
        "valuemap": {"name": "SNMP BFD Session Diag"},
        "tags": [{"tag": "Application", "value": "BFD"}, {"tag": "BFD Session", "value": "{#SNMPVALUE}"}]
    },
    {
        "uuid": str(uuid.uuid4()),
        "name": "BFD Session {#SNMPVALUE}: Operational Mode",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.4.1.9.10.137.1.2.1.9.{#SNMPINDEX}",
        "key": "ciscoBfdSessOperMode[{#SNMPINDEX}]",
        "delay": "5m", "history": "7d", "trends": "365d",
        "description": "Current operating mode of BFD session {#SNMPVALUE}. (1:asyncModeWEchoFun, 2:asynchModeWOEchoFun)",
        "valuemap": {"name": "SNMP BFD Session OperMode"},
        "tags": [{"tag": "Application", "value": "BFD"}, {"tag": "BFD Session", "value": "{#SNMPVALUE}"}]
    },
    {
        "uuid": str(uuid.uuid4()),
        "name": "BFD Session {#SNMPVALUE}: Address Type",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.4.1.9.10.137.1.2.1.13.{#SNMPINDEX}",
        "key": "ciscoBfdSessAddrType[{#SNMPINDEX}]",
        "delay": "1h", "history": "7d", "trends": "365d",
        "description": "IP address type for BFD session {#SNMPVALUE}. (0:unknown, 1:ipv4, 2:ipv6)",
        "valuemap": {"name": "SNMP BFD Address Type"},
        "tags": [{"tag": "Application", "value": "BFD"}, {"tag": "BFD Session", "value": "{#SNMPVALUE}"}]
    },
    {
        "uuid": str(uuid.uuid4()),
        "name": "BFD Session {#SNMPVALUE}: Address",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.4.1.9.10.137.1.2.1.14.{#SNMPINDEX}",
        "key": "ciscoBfdSessAddr[{#SNMPINDEX}]",
        "delay": "1h", "history": "7d", "trends": "0d", "value_type": "CHAR", # IP Address as string
        "description": "IP address associated with BFD session {#SNMPVALUE}.",
        "tags": [{"tag": "Application", "value": "BFD"}, {"tag": "BFD Session", "value": "{#SNMPVALUE}"}]
    },
    {
        "uuid": str(uuid.uuid4()),
        "name": "BFD Session {#SNMPVALUE}: Desired Min Tx Interval",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.4.1.9.10.137.1.2.1.15.{#SNMPINDEX}",
        "key": "ciscoBfdSessDesiredMinTxInterval[{#SNMPINDEX}]",
        "delay": "5m", "history": "7d", "trends": "365d", "units": "µs",
        "description": "Desired minimum transmit interval in microseconds for BFD session {#SNMPVALUE}.",
        "tags": [{"tag": "Application", "value": "BFD"}, {"tag": "BFD Session", "value": "{#SNMPVALUE}"}]
    },
    {
        "uuid": str(uuid.uuid4()),
        "name": "BFD Session {#SNMPVALUE}: Required Min Rx Interval",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.4.1.9.10.137.1.2.1.16.{#SNMPINDEX}",
        "key": "ciscoBfdSessReqMinRxInterval[{#SNMPINDEX}]",
        "delay": "5m", "history": "7d", "trends": "365d", "units": "µs",
        "description": "Required minimum receive interval in microseconds for BFD session {#SNMPVALUE}.",
        "tags": [{"tag": "Application", "value": "BFD"}, {"tag": "BFD Session", "value": "{#SNMPVALUE}"}]
    },
    {
        "uuid": str(uuid.uuid4()),
        "name": "BFD Session {#SNMPVALUE}: Required Min Echo Rx Interval",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.4.1.9.10.137.1.2.1.17.{#SNMPINDEX}",
        "key": "ciscoBfdSessReqMinEchoRxInterval[{#SNMPINDEX}]",
        "delay": "5m", "history": "7d", "trends": "365d", "units": "µs",
        "description": "Required minimum echo receive interval in microseconds for BFD session {#SNMPVALUE}.",
        "tags": [{"tag": "Application", "value": "BFD"}, {"tag": "BFD Session", "value": "{#SNMPVALUE}"}]
    },
    {
        "uuid": str(uuid.uuid4()),
        "name": "BFD Session {#SNMPVALUE}: Detection Multiplier",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.4.1.9.10.137.1.2.1.18.{#SNMPINDEX}",
        "key": "ciscoBfdSessDetectMult[{#SNMPINDEX}]",
        "delay": "5m", "history": "7d", "trends": "365d",
        "description": "Detection time multiplier for BFD session {#SNMPVALUE}.",
        "tags": [{"tag": "Application", "value": "BFD"}, {"tag": "BFD Session", "value": "{#SNMPVALUE}"}]
    },
    {
        "uuid": str(uuid.uuid4()),
        "name": "BFD Session {#SNMPVALUE}: Version Number",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.4.1.9.10.137.1.2.1.23.{#SNMPINDEX}",
        "key": "ciscoBfdSessVersionNumber[{#SNMPINDEX}]",
        "delay": "1h", "history": "7d", "trends": "365d",
        "description": "BFD protocol version number for session {#SNMPVALUE}.",
        "tags": [{"tag": "Application", "value": "BFD"}, {"tag": "BFD Session", "value": "{#SNMPVALUE}"}]
    },
    {
        "uuid": str(uuid.uuid4()),
        "name": "BFD Session {#SNMPVALUE}: Type",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.4.1.9.10.137.1.2.1.24.{#SNMPINDEX}",
        "key": "ciscoBfdSessType[{#SNMPINDEX}]",
        "delay": "1h", "history": "7d", "trends": "365d",
        "description": "Type of BFD session {#SNMPVALUE}.", # Consider a valuemap if values are known
        "tags": [{"tag": "Application", "value": "BFD"}, {"tag": "BFD Session", "value": "{#SNMPVALUE}"}]
    },
    {
        "uuid": str(uuid.uuid4()),
        "name": "BFD Session {#SNMPVALUE}: Interface IfIndex",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.4.1.9.10.137.1.2.1.25.{#SNMPINDEX}",
        "key": "ciscoBfdSessInterface[{#SNMPINDEX}]",
        "delay": "1h", "history": "7d", "trends": "365d",
        "description": "Interface IfIndex for BFD session {#SNMPVALUE}.",
        "tags": [{"tag": "Application", "value": "BFD"}, {"tag": "BFD Session", "value": "{#SNMPVALUE}"}]
    }
]

trigger_prototypes = [
    {
        "uuid": str(uuid.uuid4()),
        "expression": f"(last(/{bfd_template_object['name']}/ciscoBfdSessState[{{#SNMPINDEX}}])=2 or last(/{bfd_template_object['name']}/ciscoBfdSessState[{{#SNMPINDEX}}])=1)",
        "name": "BFD Session {#SNMPVALUE} is Down/AdminDown",
        "priority": "HIGH", # Can be 2 (Warning), 3 (Average), 4 (High), 5 (Disaster)
        "description": "BFD Session with index {#SNMPINDEX} (Value from discovery: {#SNMPVALUE}) has entered a down(2) or administratively down(1) state.",
        "tags": [{"tag": "BFD Failure", "value": "{#SNMPVALUE}"}]
    }
]

bfd_session_discovery_rule = {
    "uuid": str(uuid.uuid4()),
    "name": "BFD Sessions",
    "type": "SNMP_AGENT",
    "snmp_oid": "discovery[{#SNMPVALUE},.1.3.6.1.4.1.9.10.137.1.2.1.1]", # ciscoBfdSessIndex
    "key": "bfdSessIndex",
    "delay": "5m",
    "lifetime": "1h", # How long to keep discovered items that are no longer found
    "description": "Discovery of BFD sessions from ciscoBfdSessTable using ciscoBfdSessIndex.",
    "item_prototypes": item_prototypes,
    "trigger_prototypes": trigger_prototypes,
    "tags": [{"tag": "Discovery", "value": "BFD Sessions"}]
}

bfd_template_object["discovery_rules"].append(bfd_session_discovery_rule)

try:
    with open(bfd_template_file, "w") as f:
        json.dump(bfd_data, f, indent=4)
    print(f"Successfully added BFD Session Table discovery rule and item prototypes to {bfd_template_file}")
except IOError:
    print(f"Error: Could not write to {bfd_template_file}.")
    exit(1)

# For verification:
# with open(bfd_template_file, "r") as f:
#     print(f"Content of {bfd_template_file} after adding BFD Session discovery:")
#     print(f.read())
