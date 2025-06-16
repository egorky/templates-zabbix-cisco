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

# {#LDPSESSIONKEY} will be EntityLdpId.EntityIndex.PeerLdpId from discovery
session_item_prototypes = [
    # --- mplsLdpPeerEntry ---
    {
        "uuid": uuid.uuid4().hex,
        "name": "LDP Session Peer [{#LDPSESSIONKEY}]: Label Dist Method",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.3.2.1.2.{#LDPSESSIONKEY}", # mplsLdpPeerLabelDistMethod
        "key": "mplsLdpPeerLabelDistMethod[{#LDPSESSIONKEY}]",
        "delay": "1h", "history": "7d", "trends": "365d", "value_type": "UNSIGNED",
        "description": "Label distribution method for LDP Peer in session {#LDPSESSIONKEY}. (mplsLdpPeerLabelDistMethod)",
        "valuemap": {"name": "MPLS LDP Label Dist Method"},
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Session"}, {"tag": "LDP_Session_Key", "value": "{#LDPSESSIONKEY}"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "LDP Session Peer [{#LDPSESSIONKEY}]: Path Vector Limit",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.3.2.1.3.{#LDPSESSIONKEY}", # mplsLdpPeerPathVectorLimit
        "key": "mplsLdpPeerPathVectorLimit[{#LDPSESSIONKEY}]",
        "delay": "1h", "history": "7d", "trends": "365d", "value_type": "UNSIGNED",
        "description": "Path Vector Limit for loop detection for Peer in session {#LDPSESSIONKEY}. (mplsLdpPeerPathVectorLimit)",
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Session"}, {"tag": "LDP_Session_Key", "value": "{#LDPSESSIONKEY}"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "LDP Session Peer [{#LDPSESSIONKEY}]: Transport Addr Type",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.3.2.1.4.{#LDPSESSIONKEY}", # mplsLdpPeerTransportAddrType
        "key": "mplsLdpPeerTransportAddrType[{#LDPSESSIONKEY}]",
        "delay": "1h", "history": "7d", "trends": "365d", "value_type": "UNSIGNED",
        "description": "Transport address type for Peer in session {#LDPSESSIONKEY}. (mplsLdpPeerTransportAddrType)",
        "valuemap": {"name": "InetAddressType"},
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Session"}, {"tag": "LDP_Session_Key", "value": "{#LDPSESSIONKEY}"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "LDP Session Peer [{#LDPSESSIONKEY}]: Transport Addr",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.3.2.1.5.{#LDPSESSIONKEY}", # mplsLdpPeerTransportAddr
        "key": "mplsLdpPeerTransportAddr[{#LDPSESSIONKEY}]",
        "delay": "1h", "history": "7d", "trends": "0d", "value_type": "TEXT",
        "description": "Transport address for Peer in session {#LDPSESSIONKEY}. (mplsLdpPeerTransportAddr)",
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Session"}, {"tag": "LDP_Session_Key", "value": "{#LDPSESSIONKEY}"}]
    },
    # --- mplsLdpSessionEntry ---
    {
        "uuid": uuid.uuid4().hex,
        "name": "LDP Session [{#LDPSESSIONKEY}]: State Last Change",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.3.3.1.1.{#LDPSESSIONKEY}", # mplsLdpSessionStateLastChange
        "key": "mplsLdpSessionStateLastChange[{#LDPSESSIONKEY}]",
        "delay": "5m", "history": "7d", "trends": "365d", "value_type": "UNSIGNED", "units": "unixtime",
        "description": "SysUpTime of last state change for session {#LDPSESSIONKEY}. (mplsLdpSessionStateLastChange)",
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Session"}, {"tag": "LDP_Session_Key", "value": "{#LDPSESSIONKEY}"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "LDP Session [{#LDPSESSIONKEY}]: State",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.3.3.1.2.{#LDPSESSIONKEY}", # mplsLdpSessionState
        "key": "mplsLdpSessionState[{#LDPSESSIONKEY}]",
        "delay": "1m", "history": "7d", "trends": "365d", "value_type": "UNSIGNED",
        "description": "Current state of LDP session {#LDPSESSIONKEY}. (mplsLdpSessionState)",
        "valuemap": {"name": "MPLS LDP Session State"},
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Session"}, {"tag": "LDP_Session_Key", "value": "{#LDPSESSIONKEY}"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "LDP Session [{#LDPSESSIONKEY}]: Role",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.3.3.1.3.{#LDPSESSIONKEY}", # mplsLdpSessionRole
        "key": "mplsLdpSessionRole[{#LDPSESSIONKEY}]",
        "delay": "1h", "history": "7d", "trends": "365d", "value_type": "UNSIGNED",
        "description": "Role (active/passive) of this LSR/LER in session {#LDPSESSIONKEY} establishment. (mplsLdpSessionRole)",
        "valuemap": {"name": "MPLS LDP Session Role"},
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Session"}, {"tag": "LDP_Session_Key", "value": "{#LDPSESSIONKEY}"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "LDP Session [{#LDPSESSIONKEY}]: Protocol Version",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.3.3.1.4.{#LDPSESSIONKEY}", # mplsLdpSessionProtocolVersion
        "key": "mplsLdpSessionProtocolVersion[{#LDPSESSIONKEY}]",
        "delay": "1h", "history": "7d", "trends": "365d", "value_type": "UNSIGNED",
        "description": "Negotiated LDP protocol version for session {#LDPSESSIONKEY}. (mplsLdpSessionProtocolVersion)",
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Session"}, {"tag": "LDP_Session_Key", "value": "{#LDPSESSIONKEY}"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "LDP Session [{#LDPSESSIONKEY}]: KeepAlive Hold Time Remaining",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.3.3.1.5.{#LDPSESSIONKEY}", # mplsLdpSessionKeepAliveHoldTimeRem
        "key": "mplsLdpSessionKeepAliveHoldTimeRem[{#LDPSESSIONKEY}]",
        "delay": "1m", "history": "7d", "trends": "365d", "value_type": "UNSIGNED", "units": "s", # MIB TimeInterval, but desc says seconds
        "description": "KeepAlive hold time remaining for session {#LDPSESSIONKEY}. (mplsLdpSessionKeepAliveHoldTimeRem)",
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Session"}, {"tag": "LDP_Session_Key", "value": "{#LDPSESSIONKEY}"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "LDP Session [{#LDPSESSIONKEY}]: KeepAlive Time",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.3.3.1.6.{#LDPSESSIONKEY}", # mplsLdpSessionKeepAliveTime
        "key": "mplsLdpSessionKeepAliveTime[{#LDPSESSIONKEY}]",
        "delay": "1h", "history": "7d", "trends": "365d", "value_type": "UNSIGNED", "units": "s",
        "description": "Negotiated KeepAlive Time for session {#LDPSESSIONKEY}. (mplsLdpSessionKeepAliveTime)",
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Session"}, {"tag": "LDP_Session_Key", "value": "{#LDPSESSIONKEY}"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "LDP Session [{#LDPSESSIONKEY}]: Max PDU Length",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.3.3.1.7.{#LDPSESSIONKEY}", # mplsLdpSessionMaxPduLength
        "key": "mplsLdpSessionMaxPduLength[{#LDPSESSIONKEY}]",
        "delay": "1h", "history": "7d", "trends": "365d", "value_type": "UNSIGNED", "units": "octets",
        "description": "Negotiated Max PDU Length for session {#LDPSESSIONKEY}. (mplsLdpSessionMaxPduLength)",
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Session"}, {"tag": "LDP_Session_Key", "value": "{#LDPSESSIONKEY}"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "LDP Session [{#LDPSESSIONKEY}]: Discontinuity Time",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.3.3.1.8.{#LDPSESSIONKEY}", # mplsLdpSessionDiscontinuityTime
        "key": "mplsLdpSessionDiscontinuityTime[{#LDPSESSIONKEY}]",
        "delay": "5m", "history": "7d", "trends": "365d", "value_type": "UNSIGNED", "units": "unixtime",
        "description": "SysUpTime of most recent counter discontinuity for session {#LDPSESSIONKEY}. (mplsLdpSessionDiscontinuityTime)",
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Session"}, {"tag": "LDP_Session_Key", "value": "{#LDPSESSIONKEY}"}]
    },
    # --- mplsLdpSessionStatsEntry ---
    {
        "uuid": uuid.uuid4().hex,
        "name": "LDP Session Stats [{#LDPSESSIONKEY}]: Unknown Message Type Errors",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.3.4.1.1.{#LDPSESSIONKEY}", # mplsLdpSessionStatsUnknownMesTypeErrors
        "key": "mplsLdpSessionStatsUnknownMesTypeErrors[{#LDPSESSIONKEY}]",
        "delay": "5m", "history": "7d", "trends": "365d", "value_type": "UNSIGNED",
        "preprocessing": [{"type": "CHANGE_PER_SECOND", "parameters": [""]}], "units": "cps",
        "description": "Rate of Unknown Message Type Errors for session {#LDPSESSIONKEY}. (mplsLdpSessionStatsUnknownMesTypeErrors)",
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Session_Stats"}, {"tag": "LDP_Session_Key", "value": "{#LDPSESSIONKEY}"}]
    },
    {
        "uuid": uuid.uuid4().hex,
        "name": "LDP Session Stats [{#LDPSESSIONKEY}]: Unknown TLV Errors",
        "type": "SNMP_AGENT",
        "snmp_oid": ".1.3.6.1.2.1.10.166.4.1.3.4.1.2.{#LDPSESSIONKEY}", # mplsLdpSessionStatsUnknownTlvErrors
        "key": "mplsLdpSessionStatsUnknownTlvErrors[{#LDPSESSIONKEY}]",
        "delay": "5m", "history": "7d", "trends": "365d", "value_type": "UNSIGNED",
        "preprocessing": [{"type": "CHANGE_PER_SECOND", "parameters": [""]}], "units": "cps",
        "description": "Rate of Unknown TLV Errors for session {#LDPSESSIONKEY}. (mplsLdpSessionStatsUnknownTlvErrors)",
        "tags": [{"tag": "Application", "value": "MPLS_LDP_Session_Stats"}, {"tag": "LDP_Session_Key", "value": "{#LDPSESSIONKEY}"}]
    }
]

session_trigger_prototypes = [
    {
        "uuid": uuid.uuid4().hex,
        "expression": f"(last(/{template['name']}/mplsLdpSessionState[{{#LDPSESSIONKEY}}])<>5)", # Not operational (5)
        "name": "MPLS LDP Session [{#LDPSESSIONKEY}] is not Operational",
        "priority": "HIGH",
        "description": "MPLS LDP Session with key {#LDPSESSIONKEY} is not 'operational(5)'. Current state: {{ITEM.LASTVALUE}}.",
        "tags": [{"tag": "MPLS_LDP_Session_Status", "value": "{#LDPSESSIONKEY}"}]
    }
]

ldp_session_discovery_rule = {
    "uuid": uuid.uuid4().hex,
    "name": "MPLS LDP Sessions",
    "type": "SNMP_AGENT",
    "snmp_oid": "discovery[{#LDPSESSIONKEY},.1.3.6.1.2.1.10.166.4.1.3.2.1.1]", # Discovering mplsLdpPeerLdpId instances
    "key": "mplsLdpSession.discovery",
    "delay": "1h", "lifetime": "30d",
    "description": "Discovery of MPLS LDP Peers (mplsLdpPeerTable), Sessions (mplsLdpSessionTable), and their statistics (mplsLdpSessionStatsTable). {#LDPSESSIONKEY} is EntityLdpId.EntityIndex.PeerLdpId.",
    "item_prototypes": session_item_prototypes,
    "trigger_prototypes": session_trigger_prototypes
}

template["discovery_rules"].append(ldp_session_discovery_rule)

try:
    with open(ldp_template_file, "w") as f:
        json.dump(ldp_data, f, indent=4)
    print(f"Successfully added MPLS LDP Session discovery rule to {ldp_template_file}")
except IOError:
    print(f"Error: Could not write to {ldp_template_file}.")
    exit(1)
