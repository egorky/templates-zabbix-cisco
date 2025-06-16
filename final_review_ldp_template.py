import json
import re

ldp_template_file = "zabbix_mpls_ldp_template.json"
review_notes = []
issues_found = 0

def check_uuid_format(uuid_str, field_name):
    global issues_found
    if not isinstance(uuid_str, str) or len(uuid_str) != 32 or not all(c in '0123456789abcdefABCDEF' for c in uuid_str):
        review_notes.append(f"FAILURE: UUID format error for {field_name}: '{uuid_str}'")
        issues_found +=1
        return False
    return True

def check_value_type(v_type, field_name):
    global issues_found
    valid_types = ["FLOAT", "CHAR", "LOG", "UNSIGNED", "TEXT", "BINARY"]
    if v_type not in valid_types:
        review_notes.append(f"FAILURE: Invalid value_type for {field_name}: '{v_type}'")
        issues_found +=1
        return False
    return True

try:
    with open(ldp_template_file, "r") as f:
        ldp_data = json.load(f)
except FileNotFoundError:
    review_notes.append(f"CRITICAL: {ldp_template_file} not found.")
    print("\n".join(review_notes))
    exit(1)
except json.JSONDecodeError:
    review_notes.append(f"CRITICAL: Could not decode JSON from {ldp_template_file}.")
    print("\n".join(review_notes))
    exit(1)

review_notes.append(f"--- Reviewing {ldp_template_file} ---")

# 1. Basic Structure
if not ldp_data.get("zabbix_export"):
    review_notes.append("FAILURE: Missing 'zabbix_export' root object.")
    issues_found +=1
else:
    z_export = ldp_data["zabbix_export"]
    if not z_export.get("templates") or not isinstance(z_export["templates"], list) or len(z_export["templates"]) != 1:
        review_notes.append("FAILURE: 'templates' array issue (missing, not list, or not 1 template).")
        issues_found +=1
    else:
        template = z_export["templates"][0]

        # 2. Template Name & UUID
        if template.get("name") == "SNMP MPLS LDP":
            review_notes.append("SUCCESS: Template name is 'SNMP MPLS LDP'.")
        else:
            review_notes.append(f"FAILURE: Template name is '{template.get('name')}', expected 'SNMP MPLS LDP'.")
            issues_found +=1
        if check_uuid_format(template.get("uuid"), "Template UUID"):
             review_notes.append("SUCCESS: Template UUID format appears correct.")

        # 3. Content Spot Checks - Items
        found_lsr_id = any(item.get("key") == "mplsLdpLsrId" for item in template.get("items", []))
        if found_lsr_id:
            review_notes.append("SUCCESS: Scalar item 'mplsLdpLsrId' found.")
            # Check its value_type
            for item in template.get("items", []):
                if item.get("key") == "mplsLdpLsrId":
                    if check_value_type(item.get("value_type"), "mplsLdpLsrId value_type"):
                        review_notes.append(f"SUCCESS: mplsLdpLsrId value_type '{item.get('value_type')}' is valid.")
                    break
        else:
            review_notes.append("FAILURE: Scalar item 'mplsLdpLsrId' NOT found.")
            issues_found +=1

        # Content Spot Checks - Discovery Rules and LLD Macros
        discovery_rules_data = {
            "mplsLdpEntity.discovery": {"macro": "{#SNMPENTITYKEY}", "sample_item_key_part": "mplsLdpEntityLdpId"},
            "mplsLdpSession.discovery": {"macro": "{#LDPSESSIONKEY}", "sample_item_key_part": "mplsLdpPeerLabelDistMethod"},
            "mplsLdpHelloAdjacency.discovery": {"macro": "{#LDPHELLOADJKEY}", "sample_item_key_part": "mplsLdpHelloAdjacencyHoldTimeRem"}
        }
        for key, data in discovery_rules_data.items():
            rule_found = False
            for rule in template.get("discovery_rules", []):
                if rule.get("key") == key:
                    rule_found = True
                    review_notes.append(f"SUCCESS: Discovery rule '{key}' found.")
                    check_uuid_format(rule.get("uuid"), f"Discovery rule {key} UUID")

                    # Check LLD macro in a sample item prototype
                    item_proto_found = False
                    for proto in rule.get("item_prototypes", []):
                        if data["sample_item_key_part"] in proto.get("key",""):
                            item_proto_found = True
                            if data["macro"] in proto.get("key", "") and data["macro"] in proto.get("snmp_oid", ""):
                                review_notes.append(f"SUCCESS: LLD Macro '{data['macro']}' used correctly in item prototype '{proto.get('key')}' for rule '{key}'.")
                            else:
                                review_notes.append(f"FAILURE: LLD Macro '{data['macro']}' NOT used correctly in item prototype '{proto.get('key')}' for rule '{key}'.")
                                issues_found +=1
                            check_uuid_format(proto.get("uuid"), f"Item proto {proto.get('key')} UUID")
                            check_value_type(proto.get("value_type"), f"Item proto {proto.get('key')} value_type")
                            break
                    if not item_proto_found and rule.get("item_prototypes"): # only fail if protos exist but sample not found
                        review_notes.append(f"NOTE: Sample item prototype for rule '{key}' (containing '{data['sample_item_key_part']}') not found for detailed LLD macro check.")
                    elif not rule.get("item_prototypes"):
                         review_notes.append(f"NOTE: No item prototypes in rule '{key}' to check LLD Macros.")
                    break
            if not rule_found:
                review_notes.append(f"FAILURE: Discovery rule '{key}' NOT found.")
                issues_found +=1

        # Content Spot Checks - Value Maps
        found_session_state_vm = any(vm.get("name") == "MPLS LDP Session State" for vm in template.get("valuemaps", []))
        if found_session_state_vm:
            review_notes.append("SUCCESS: Value map 'MPLS LDP Session State' found.")
            for vm in template.get("valuemaps",[]):
                if vm.get("name") == "MPLS LDP Session State":
                    check_uuid_format(vm.get("uuid"), "Value map 'MPLS LDP Session State' UUID")
                    break
        else:
            review_notes.append("FAILURE: Value map 'MPLS LDP Session State' NOT found.")
            issues_found +=1

        # 5. Absence of BFD/OSPF Remnants
        template_str = json.dumps(template) # Crude check
        if "bfd" in template_str.lower() or "ospf" in template_str.lower():
            # Allow if it's part of the BFD template description (which is not the case here as it's LDP)
            # or if it's part of a specific item/key name that might be generically named (e.g. ciscoIetfBfdMib)
            # For LDP template, any "bfd" or "ospf" is suspicious unless it's a MIB name in a description.
            # The LDP description is "Template for monitoring MPLS LDP (Label Distribution Protocol) using SNMP, based on MPLS-LDP-STD-MIB (RFC 3815)."
            # So, if "bfd" or "ospf" appears, it's likely an issue.

            # Refined check: Only flag if "bfd" or "ospf" is NOT part of a known allowed context (like a MIB name in a description)
            allowed_contexts = ["ciscoIetfBfdMIB", "OSPF-MIB"] # Add more if needed
            suspicious_found = False
            if "bfd" in template_str.lower():
                if not any(allowed_context.lower().replace("bfd", "bfd") in template_str.lower() for allowed_context in allowed_contexts if "bfd" in allowed_context.lower()):
                    suspicious_found = True
            if "ospf" in template_str.lower():
                 if not any(allowed_context.lower().replace("ospf", "ospf") in template_str.lower() for allowed_context in allowed_contexts if "ospf" in allowed_context.lower()):
                    suspicious_found = True

            if suspicious_found:
                 review_notes.append(f"WARNING: Potential 'bfd' or 'ospf' string found in template JSON outside of known allowed contexts (e.g., MIB names in descriptions). Manual check recommended.")
            else:
                review_notes.append("SUCCESS: 'bfd' or 'ospf' strings found are within known allowed contexts (e.g., MIB names in descriptions) or not present.")

        else:
            review_notes.append("SUCCESS: No obvious 'bfd' or 'ospf' remnants found in template string.")


if issues_found > 0:
    review_notes.append(f"\nReview finished with {issues_found} failure(s).")
else:
    review_notes.append("\nReview finished. All spot checks passed or noted.")

print("\n".join(review_notes))
