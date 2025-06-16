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

# {#SNMPENTITYKEY} will represent the instance identifier part of the OID,
# which for mplsLdpEntityTable includes both mplsLdpEntityLdpId and mplsLdpEntityIndex.
# Example: if LDP ID is 1.2.3.4:0 and EntityIndex is 10, SNMPENTITYKEY might be "1.2.3.4.0.10"
# (actual representation depends on SNMP agent).
# The OIDs for item prototypes will be ColumnOID.{#SNMPENTITYKEY}.

entity_item_prototypes = [
    # --- mplsLdpEntityEntry ---
    {
        "uuid": uuid.uuid4().hex,
        "name": "LDP Entity [{#SNMPENTITYKEY}]: LDP ID",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.2.3.1.1.{#SNMPENTITYKEY}", # mplsLdpEntityLdpId
        "key": "mplsLdpEntityLdpId[{#SNMPENTITYKEY}]",
        "delay": "1h", "history": "7d", "trends": "0d", "value_type": "TEXT",
        "description": "The LDP identifier for entity represented by mplsLdpEntityIndex {#SNMPENTITYKEY}. (mplsLdpEntityLdpId)",
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Entity"}, {"tag": "LDP_Entity_Key", "value": "{#SNMPENTITYKEY}"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "LDP Entity [{#SNMPENTITYKEY}]: Protocol Version",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.2.3.1.3.{#SNMPENTITYKEY}", # mplsLdpEntityProtocolVersion
        "key": "mplsLdpEntityProtocolVersion[{#SNMPENTITYKEY}]",
        "delay": "1h", "history": "7d", "trends": "365d", "value_type": "UNSIGNED",
        "description": "LDP protocol version for entity {#SNMPENTITYKEY}. (mplsLdpEntityProtocolVersion)",
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Entity"}, {"tag": "LDP_Entity_Key", "value": "{#SNMPENTITYKEY}"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "LDP Entity [{#SNMPENTITYKEY}]: Admin Status",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.2.3.1.4.{#SNMPENTITYKEY}", # mplsLdpEntityAdminStatus
        "key": "mplsLdpEntityAdminStatus[{#SNMPENTITYKEY}]",
        "delay": "5m", "history": "7d", "trends": "365d", "value_type": "UNSIGNED",
        "description": "Administrative status of LDP Entity {#SNMPENTITYKEY}. (mplsLdpEntityAdminStatus)",
        "valuemap": {"name": "MPLS LDP Entity Admin Status"},
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Entity"}, {"tag": "LDP_Entity_Key", "value": "{#SNMPENTITYKEY}"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "LDP Entity [{#SNMPENTITYKEY}]: Operational Status",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.2.3.1.5.{#SNMPENTITYKEY}", # mplsLdpEntityOperStatus
        "key": "mplsLdpEntityOperStatus[{#SNMPENTITYKEY}]",
        "delay": "1m", "history": "7d", "trends": "365d", "value_type": "UNSIGNED",
        "description": "Operational status of LDP Entity {#SNMPENTITYKEY}. (mplsLdpEntityOperStatus)",
        "valuemap": {"name": "MPLS LDP Entity Oper Status"},
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Entity"}, {"tag": "LDP_Entity_Key", "value": "{#SNMPENTITYKEY}"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "LDP Entity [{#SNMPENTITYKEY}]: TCP Port",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.2.3.1.6.{#SNMPENTITYKEY}", # mplsLdpEntityTcpPort
        "key": "mplsLdpEntityTcpPort[{#SNMPENTITYKEY}]",
        "delay": "1h", "history": "7d", "trends": "365d", "value_type": "UNSIGNED",
        "description": "LDP TCP Port for entity {#SNMPENTITYKEY}. (mplsLdpEntityTcpPort)",
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Entity"}, {"tag": "LDP_Entity_Key", "value": "{#SNMPENTITYKEY}"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "LDP Entity [{#SNMPENTITYKEY}]: UDP Discovery Port",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.2.3.1.7.{#SNMPENTITYKEY}", # mplsLdpEntityUdpDscPort
        "key": "mplsLdpEntityUdpDscPort[{#SNMPENTITYKEY}]",
        "delay": "1h", "history": "7d", "trends": "365d", "value_type": "UNSIGNED",
        "description": "LDP UDP Discovery Port for entity {#SNMPENTITYKEY}. (mplsLdpEntityUdpDscPort)",
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Entity"}, {"tag": "LDP_Entity_Key", "value": "{#SNMPENTITYKEY}"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "LDP Entity [{#SNMPENTITYKEY}]: Max PDU Length",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.2.3.1.8.{#SNMPENTITYKEY}", # mplsLdpEntityMaxPduLength
        "key": "mplsLdpEntityMaxPduLength[{#SNMPENTITYKEY}]",
        "delay": "1h", "history": "7d", "trends": "365d", "value_type": "UNSIGNED", "units": "octets",
        "description": "Max PDU Length sent in Initialization Message for entity {#SNMPENTITYKEY}. (mplsLdpEntityMaxPduLength)",
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Entity"}, {"tag": "LDP_Entity_Key", "value": "{#SNMPENTITYKEY}"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "LDP Entity [{#SNMPENTITYKEY}]: KeepAlive Hold Timer",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.2.3.1.9.{#SNMPENTITYKEY}", # mplsLdpEntityKeepAliveHoldTimer
        "key": "mplsLdpEntityKeepAliveHoldTimer[{#SNMPENTITYKEY}]",
        "delay": "5m", "history": "7d", "trends": "365d", "value_type": "UNSIGNED", "units": "s",
        "description": "Proposed KeepAlive Hold Timer for entity {#SNMPENTITYKEY}. (mplsLdpEntityKeepAliveHoldTimer)",
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Entity"}, {"tag": "LDP_Entity_Key", "value": "{#SNMPENTITYKEY}"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "LDP Entity [{#SNMPENTITYKEY}]: Hello Hold Timer",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.2.3.1.10.{#SNMPENTITYKEY}", # mplsLdpEntityHelloHoldTimer
        "key": "mplsLdpEntityHelloHoldTimer[{#SNMPENTITYKEY}]",
        "delay": "5m", "history": "7d", "trends": "365d", "value_type": "UNSIGNED", "units": "s",
        "description": "Proposed Hello Hold Timer for entity {#SNMPENTITYKEY}. (mplsLdpEntityHelloHoldTimer)",
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Entity"}, {"tag": "LDP_Entity_Key", "value": "{#SNMPENTITYKEY}"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "LDP Entity [{#SNMPENTITYKEY}]: Init Session Threshold",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.2.3.1.11.{#SNMPENTITYKEY}", # mplsLdpEntityInitSessionThreshold
        "key": "mplsLdpEntityInitSessionThreshold[{#SNMPENTITYKEY}]",
        "delay": "1h", "history": "7d", "trends": "365d", "value_type": "UNSIGNED", # MIB says Integer32(0..100)
        "description": "Threshold for mplsLdpInitSessionThresholdExceeded notification for entity {#SNMPENTITYKEY}. (mplsLdpEntityInitSessionThreshold)",
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Entity"}, {"tag": "LDP_Entity_Key", "value": "{#SNMPENTITYKEY}"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "LDP Entity [{#SNMPENTITYKEY}]: Label Distribution Method",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.2.3.1.12.{#SNMPENTITYKEY}", # mplsLdpEntityLabelDistMethod
        "key": "mplsLdpEntityLabelDistMethod[{#SNMPENTITYKEY}]",
        "delay": "1h", "history": "7d", "trends": "365d", "value_type": "UNSIGNED",
        "description": "Label distribution method for entity {#SNMPENTITYKEY}. (mplsLdpEntityLabelDistMethod)",
        "valuemap": {"name": "MPLS LDP Label Dist Method"},
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Entity"}, {"tag": "LDP_Entity_Key", "value": "{#SNMPENTITYKEY}"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "LDP Entity [{#SNMPENTITYKEY}]: Label Retention Mode",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.2.3.1.13.{#SNMPENTITYKEY}", # mplsLdpEntityLabelRetentionMode
        "key": "mplsLdpEntityLabelRetentionMode[{#SNMPENTITYKEY}]",
        "delay": "1h", "history": "7d", "trends": "365d", "value_type": "UNSIGNED",
        "description": "Label retention mode for entity {#SNMPENTITYKEY}. (mplsLdpEntityLabelRetentionMode)",
        "valuemap": {"name": "MPLS LDP Label Retention Mode"},
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Entity"}, {"tag": "LDP_Entity_Key", "value": "{#SNMPENTITYKEY}"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "LDP Entity [{#SNMPENTITYKEY}]: Path Vector Limit",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.2.3.1.14.{#SNMPENTITYKEY}", # mplsLdpEntityPathVectorLimit
        "key": "mplsLdpEntityPathVectorLimit[{#SNMPENTITYKEY}]",
        "delay": "1h", "history": "7d", "trends": "365d", "value_type": "UNSIGNED", # MIB says Integer32(0..255)
        "description": "Path Vector Limit for loop detection for entity {#SNMPENTITYKEY}. (mplsLdpEntityPathVectorLimit)",
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Entity"}, {"tag": "LDP_Entity_Key", "value": "{#SNMPENTITYKEY}"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "LDP Entity [{#SNMPENTITYKEY}]: Hop Count Limit",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.2.3.1.15.{#SNMPENTITYKEY}", # mplsLdpEntityHopCountLimit
        "key": "mplsLdpEntityHopCountLimit[{#SNMPENTITYKEY}]",
        "delay": "1h", "history": "7d", "trends": "365d", "value_type": "UNSIGNED", # MIB says Integer32(0..255)
        "description": "Hop Count Limit for loop detection for entity {#SNMPENTITYKEY}. (mplsLdpEntityHopCountLimit)",
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Entity"}, {"tag": "LDP_Entity_Key", "value": "{#SNMPENTITYKEY}"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "LDP Entity [{#SNMPENTITYKEY}]: Transport Address Kind",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.2.3.1.16.{#SNMPENTITYKEY}", # mplsLdpEntityTransportAddrKind
        "key": "mplsLdpEntityTransportAddrKind[{#SNMPENTITYKEY}]",
        "delay": "1h", "history": "7d", "trends": "365d", "value_type": "UNSIGNED",
        "description": "Transport address kind (interface/loopback) for Hello messages for entity {#SNMPENTITYKEY}. (mplsLdpEntityTransportAddrKind)",
        "valuemap": {"name": "MPLS LDP Transport Addr Kind"},
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Entity"}, {"tag": "LDP_Entity_Key", "value": "{#SNMPENTITYKEY}"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "LDP Entity [{#SNMPENTITYKEY}]: Targeted Peer",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.2.3.1.17.{#SNMPENTITYKEY}", # mplsLdpEntityTargetPeer
        "key": "mplsLdpEntityTargetPeer[{#SNMPENTITYKEY}]",
        "delay": "1h", "history": "7d", "trends": "365d", "value_type": "UNSIGNED",
        "description": "Whether LDP entity {#SNMPENTITYKEY} uses a targeted peer (true/false). (mplsLdpEntityTargetPeer)",
        "valuemap": {"name": "TruthValue"},
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Entity"}, {"tag": "LDP_Entity_Key", "value": "{#SNMPENTITYKEY}"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "LDP Entity [{#SNMPENTITYKEY}]: Target Peer Addr Type",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.2.3.1.18.{#SNMPENTITYKEY}", # mplsLdpEntityTargetPeerAddrType
        "key": "mplsLdpEntityTargetPeerAddrType[{#SNMPENTITYKEY}]",
        "delay": "1h", "history": "7d", "trends": "365d", "value_type": "UNSIGNED",
        "description": "Address type for Extended Discovery target peer for entity {#SNMPENTITYKEY}. (mplsLdpEntityTargetPeerAddrType)",
        "valuemap": {"name": "InetAddressType"}, # Generic valuemap
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Entity"}, {"tag": "LDP_Entity_Key", "value": "{#SNMPENTITYKEY}"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "LDP Entity [{#SNMPENTITYKEY}]: Target Peer Addr",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.2.3.1.19.{#SNMPENTITYKEY}", # mplsLdpEntityTargetPeerAddr
        "key": "mplsLdpEntityTargetPeerAddr[{#SNMPENTITYKEY}]",
        "delay": "1h", "history": "7d", "trends": "0d", "value_type": "TEXT",
        "description": "Address for Extended Discovery target peer for entity {#SNMPENTITYKEY}. (mplsLdpEntityTargetPeerAddr)",
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Entity"}, {"tag": "LDP_Entity_Key", "value": "{#SNMPENTITYKEY}"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "LDP Entity [{#SNMPENTITYKEY}]: Label Type",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.2.3.1.20.{#SNMPENTITYKEY}", # mplsLdpEntityLabelType
        "key": "mplsLdpEntityLabelType[{#SNMPENTITYKEY}]",
        "delay": "1h", "history": "7d", "trends": "365d", "value_type": "UNSIGNED",
        "description": "Optional parameters for LDP Initialization Message for entity {#SNMPENTITYKEY}. (mplsLdpEntityLabelType)",
        "valuemap": {"name": "MPLS LDP Label Type"},
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Entity"}, {"tag": "LDP_Entity_Key", "value": "{#SNMPENTITYKEY}"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "LDP Entity [{#SNMPENTITYKEY}]: Discontinuity Time",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.2.3.1.21.{#SNMPENTITYKEY}", # mplsLdpEntityDiscontinuityTime
        "key": "mplsLdpEntityDiscontinuityTime[{#SNMPENTITYKEY}]",
        "delay": "5m", "history": "7d", "trends": "365d", "value_type": "UNSIGNED", "units": "unixtime",
        "description": "SysUpTime of the most recent counter discontinuity for entity {#SNMPENTITYKEY}. (mplsLdpEntityDiscontinuityTime)",
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Entity"}, {"tag": "LDP_Entity_Key", "value": "{#SNMPENTITYKEY}"}]
    },
    # --- mplsLdpEntityStatsEntry ---
    {
        "uuid": uuid.uuid4().hex,
        "name": "LDP Entity Stats [{#SNMPENTITYKEY}]: Session Attempts",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.2.4.1.1.{#SNMPENTITYKEY}", # mplsLdpEntityStatsSessionAttempts
        "key": "mplsLdpEntityStatsSessionAttempts[{#SNMPENTITYKEY}]",
        "delay": "5m", "history": "7d", "trends": "365d", "value_type": "UNSIGNED",
        "preprocessing": [{"type": "CHANGE_PER_SECOND", "parameters": [""]}], "units": "cps",
        "description": "Rate of failed session initializations for entity {#SNMPENTITYKEY}. (mplsLdpEntityStatsSessionAttempts)",
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Entity_Stats"}, {"tag": "LDP_Entity_Key", "value": "{#SNMPENTITYKEY}"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "LDP Entity Stats [{#SNMPENTITYKEY}]: Session Rejected No Hello Errors",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.2.4.1.2.{#SNMPENTITYKEY}", # mplsLdpEntityStatsSessionRejectedNoHelloErrors
        "key": "mplsLdpEntityStatsSessionRejectedNoHelloErrors[{#SNMPENTITYKEY}]",
        "delay": "5m", "history": "7d", "trends": "365d", "value_type": "UNSIGNED",
        "preprocessing": [{"type": "CHANGE_PER_SECOND", "parameters": [""]}], "units": "cps",
        "description": "Rate of Session Rejected/No Hello Error Notifications for entity {#SNMPENTITYKEY}. (mplsLdpEntityStatsSessionRejectedNoHelloErrors)",
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Entity_Stats"}, {"tag": "LDP_Entity_Key", "value": "{#SNMPENTITYKEY}"}]
    }
]

# Manually add the remaining 11 stats items to save space in this definition
# Base OID for stats: .1.3.6.1.2.1.10.166.4.1.2.4.1.
stats_oids_info = {
    "3": "SessionRejectedAdErrors", "4": "SessionRejectedMaxPduErrors", "5": "SessionRejectedLRErrors",
    "6": "BadLdpIdentifierErrors", "7": "BadPduLengthErrors", "8": "BadMessageLengthErrors",
    "9": "BadTlvLengthErrors", "10": "MalformedTlvValueErrors", "11": "KeepAliveTimerExpErrors",
    "12": "ShutdownReceivedNotifications", "13": "ShutdownSentNotifications"
}
for oid_leaf, name_suffix in stats_oids_info.items():
    item_name = f"LDP Entity Stats [{{#SNMPENTITYKEY}}]: {name_suffix.replace('Errors', ' Errors').replace('Notifications', ' Notifications')}"
    key_name = f"mplsLdpEntityStats{name_suffix}[{{#SNMPENTITYKEY}}]"
    full_oid = f".1.3.6.1.2.1.10.166.4.1.2.4.1.{oid_leaf}.{{#SNMPENTITYKEY}}"
    desc = f"Rate of {name_suffix.replace('Errors', ' Errors').replace('Notifications', ' Notifications')} for entity {{#SNMPENTITYKEY}}. (mplsLdpEntityStats{name_suffix})"

    entity_item_prototypes.append({
        "uuid": uuid.uuid4().hex,
        "name": item_name,
        "type": "SNMP_AGENT",
        "snmp_oid": full_oid,
        "key": key_name,
        "delay": "5m", "history": "7d", "trends": "365d", "value_type": "UNSIGNED",
        "preprocessing": [{"type": "CHANGE_PER_SECOND", "parameters": [""]}], "units": "cps",
        "description": desc,
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Entity_Stats"}, {"tag": "LDP_Entity_Key", "value": "{#SNMPENTITYKEY}"}]
    })


entity_trigger_prototypes = [
    {
        "uuid": uuid.uuid4().hex,
        "expression": f"(last(/{template['name']}/mplsLdpEntityOperStatus[{{#SNMPENTITYKEY}}])<>2)", # Not enabled (2)
        "name": "MPLS LDP Entity [{#SNMPENTITYKEY}] Operational Status is not Enabled",
        "priority": "WARNING",
        "description": "MPLS LDP Entity with key {#SNMPENTITYKEY} operational status is not 'enabled(2)'. Current state: {{ITEM.LASTVALUE}}.",
        "tags": [{"tag": "MPLS_LDP_Entity_Status", "value": "{#SNMPENTITYKEY}"}]
    }
]

ldp_entity_discovery_rule = {
    "uuid": uuid.uuid4().hex,
    "name": "MPLS LDP Entities",
    "type": "SNMP_AGENT",
    "snmp_oid": "discovery[{#SNMPENTITYKEY},.1.3.6.1.2.1.10.166.4.1.2.3.1.2]", # Discovering mplsLdpEntityIndex
    "key": "mplsLdpEntity.discovery",
    "delay": "1h", "lifetime": "30d",
    "description": "Discovery of MPLS LDP Entities (mplsLdpEntityTable) and their statistics (mplsLdpEntityStatsTable). {#SNMPENTITYKEY} is the combined LDP ID and Entity Index.",
    "item_prototypes": entity_item_prototypes,
    "trigger_prototypes": entity_trigger_prototypes
}

template["discovery_rules"].append(ldp_entity_discovery_rule)

try:
    with open(ldp_template_file, "w") as f:
        json.dump(ldp_data, f, indent=4)
    print(f"Successfully added MPLS LDP Entity discovery rule to {ldp_template_file}")
except IOError:
    print(f"Error: Could not write to {ldp_template_file}.")
    exit(1)
