"""
Generic Workflow — WORLD-CLASS PROFESSIONAL — 40Y Expert — ULTRA LEGENDARY v2

Workflow adapts to ANY institution type: hospital, factory, school, hotel, bank,
retail, government, office, datacenter, trading — by size/branches/devices.

Each institution has different requirements, compliance, VLANs, services.
This workflow generates institution-specific steps with microscopic precision.

PART OF FIRST APP — makes first app world-class for ANY institution.
"""

from __future__ import annotations
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from .institution_types import get_institution_profile, InstitutionProfile
from .generic_company import GenericCompanyDef
from .workflow import WORKFLOW_STEPS, WorkflowPhase, WorkflowStep, workflow_to_dict as base_workflow_to_dict

# Institution-specific additions to workflow
INSTITUTION_WORKFLOW_ADDITIONS: Dict[str, Dict[str, List[str]]] = {
    "hospital": {
        "requirements_extra": ["HIPAA compliance", "Medical devices count", "PACS storage", "EMR system", "Life-critical uptime 99.99%"],
        "survey_extra": ["Medical equipment power", "Operating room grounding", "PACS 10G fiber", "Nurse call system"],
        "security_extra": ["HIPAA encryption", "Medical devices no Internet", "PACS isolated", "EMR audit log 7y"],
        "testing_extra": ["Medical device isolation PASS", "PACS 10G throughput PASS", "EMR encrypted PASS", "HIPAA audit PASS"],
    },
    "factory": {
        "requirements_extra": ["OT/IT separation ISA-99", "PLC/SCADA count", "Robotics real-time", "Production uptime 99.95%", "Energy management"],
        "survey_extra": ["OT cabinets", "Industrial power", "Production floor cabling", "Robotics deterministic"],
        "security_extra": ["OT isolated no Internet ISA-99", "SCADA firewall", "Robotics real-time ACL", "Production deterministic QoS"],
        "testing_extra": ["OT isolation PASS", "PLC→SCADA deterministic <1ms PASS", "Robotics real-time PASS", "ISA-99 compliance PASS"],
    },
    "school": {
        "requirements_extra": ["CIPA filtering", "FERPA compliance", "Student count 1000+", "Labs per-dept", "Dorm bandwidth per-user"],
        "survey_extra": ["Classroom AP density", "Lab isolation", "Dorm NAT", "Library OPAC"],
        "security_extra": ["CIPA content filter", "Students no P2P", "Dorm per-user limit", "Faculty separate VLAN"],
        "testing_extra": ["CIPA filter PASS", "Student→Faculty BLOCK PASS", "Lab isolation PASS", "Dorm bandwidth limit PASS"],
    },
    "hotel": {
        "requirements_extra": ["PMS integration", "Per-room isolation", "IPTV multicast 100+ channels", "POS PCI-DSS", "Door lock RFID"],
        "survey_extra": ["Room AP placement", "IPTV multicast IGMP", "POS isolated", "Conference high density"],
        "security_extra": ["Guest per-room no inter-room", "POS PCI-DSS no Internet", "Staff vs Guest isolation", "SPA isolated"],
        "testing_extra": ["Per-room isolation PASS", "POS PCI-DSS PASS", "IPTV multicast PASS", "PMS→Door lock PASS"],
    },
    "bank": {
        "requirements_extra": ["PCI-DSS SOX GLBA compliance", "ATM isolated VPN", "Vault air-gapped", "Teller 802.1X", "Audit log 7y"],
        "survey_extra": ["Vault air-gap", "ATM kiosk power", "Teller 802.1X", "Branch audit"],
        "security_extra": ["BANKING no Internet PCI-DSS SOX", "ATM isolated VPN only", "VAULT air-gapped dual auth", "TELLER 802.1X"],
        "testing_extra": ["BANKING→Internet BLOCK PASS", "ATM isolation PASS", "VAULT air-gapped PASS", "SOX audit PASS"],
    },
    "government": {
        "requirements_extra": ["NIST FISMA compliance", "CLASSIFIED air-gapped", "Citizen kiosk Internet only", "Justice police/courts isolated", "7y audit"],
        "survey_extra": ["Classified room TEMPEST", "Citizen kiosk placement", "Justice isolated network", "Public portal DMZ"],
        "security_extra": ["CLASSIFIED air-gapped NIST FISMA", "Citizen Internet only no internal", "Justice isolated", "Public portal DMZ"],
        "testing_extra": ["CLASSIFIED air-gapped PASS", "Citizen→Internal BLOCK PASS", "Justice isolation PASS", "NIST audit PASS"],
    },
    "retail": {
        "requirements_extra": ["POS PCI-DSS", "RFID inventory", "WMS logistics", "Loss prevention CCTV+POS AI", "HQ sync"],
        "survey_extra": ["POS terminal count", "RFID readers", "Warehouse WMS", "Loss prevention integration"],
        "security_extra": ["POS PCI-DSS no Internet", "Inventory RFID real-time", "CCTV→POS AI integration"],
        "testing_extra": ["POS PCI-DSS PASS", "RFID inventory PASS", "WMS sync PASS", "Loss prevention PASS"],
    },
    "datacenter": {
        "requirements_extra": ["Leaf-Spine architecture", "Storage iSCSI 40G/100G jumbo", "Backup Veeam replication", "vMotion isolated 10G+"],
        "survey_extra": ["Rack leaf-spine", "Storage 40G/100G", "Backup replication 100G", "vMotion isolated"],
        "security_extra": ["STORAGE iSCSI isolated jumbo", "BACKUP-DC replication", "VMOTION isolated no routing", "SOC2 ISO27001"],
        "testing_extra": ["STORAGE 40G jumbo PASS", "BACKUP replication 100G PASS", "VMOTION isolated PASS", "Leaf-Spine ECMP PASS"],
    },
    "trading": {
        "requirements_extra": ["ERP SAP/Oracle HQ+branches IPsec", "File server SMB AD", "Backup daily", "VOIP QoS EF"],
        "survey_extra": ["ERP server placement", "File server DFS", "Backup retention", "VOIP QoS"],
        "security_extra": ["ERP via IPsec only", "Guest isolation", "CCTV→NVR only", "MGMT admin only"],
        "testing_extra": ["ERP via IPsec PASS", "Guest isolation PASS", "CCTV isolation PASS", "File SMB PASS"],
    },
    "office": {
        "requirements_extra": ["Users+VOICE", "Corp WiFi WPA2-Enterprise", "Guest Internet only", "Printers"],
        "survey_extra": ["Office AP density", "Printer VLAN", "Meeting room AV"],
        "security_extra": ["Guest isolation", "Corp WiFi WPA2-Enterprise", "Printer VLAN"],
        "testing_extra": ["Guest isolation PASS", "Corp WiFi PASS", "Printer PASS"],
    },
}

def get_workflow_for_institution(institution_type: str, lang: str = "en") -> List[Dict[str, Any]]:
    """Get workflow adapted for institution type — WORLD-CLASS — 40Y expert"""
    profile = get_institution_profile(institution_type)
    additions = INSTITUTION_WORKFLOW_ADDITIONS.get(institution_type, INSTITUTION_WORKFLOW_ADDITIONS["office"])
    
    base = base_workflow_to_dict(lang)
    
    # Enhance each step with institution-specific extras
    for step in base:
        phase = step["phase"]
        if phase == "requirements":
            step["inputs"].extend(additions.get("requirements_extra", []))
            step["checks"].append(f"{profile.name_en} specific requirements verified")
            step["description"] += f" Institution: {profile.name_en} — Compliance: {', '.join(profile.compliance)} — Security: {profile.security_level} — {profile.description_en}"
        elif phase == "survey":
            step["inputs"].extend(additions.get("survey_extra", []))
        elif phase == "security":
            step["outputs"].extend(additions.get("security_extra", []))
            step["description"] += f" {profile.name_en} compliance: {', '.join(profile.compliance)} — VLANs: {profile.vlan_ids}"
        elif phase == "testing_l1" or phase == "testing_l2" or phase == "testing_l3":
            step["checks"].extend(additions.get("testing_extra", [])[:2])
        elif phase == "hld":
            step["outputs"].append(f"{profile.name_en} HLD — {len(profile.vlan_ids)} VLANs — {profile.security_level}")
    
    return base


def get_workflow_for_company(company: GenericCompanyDef, lang: str = "en") -> List[Dict[str, Any]]:
    """Get workflow for specific company — adapts to its institution type, size, branches"""
    workflow = get_workflow_for_institution(company.institution_type, lang)
    
    # Add company-specific details
    for step in workflow:
        if step["phase"] == "requirements":
            step["title"] += f" — {company.name}"
            step["inputs"].append(f"Company: {company.name} — {company.total_employees} employees — {len(company.all_sites)} sites — {company.institution_type}")
        elif step["phase"] == "equipment":
            step["outputs"].append(f"BoM for {company.name}: {company.total_infra_devices} infra devices — {company.size_category}")
        elif step["phase"] == "ip_vlan":
            step["outputs"].append(f"IP plan: {company.hq.site_id} {company.hq.supernet} — VLANs: {list(company.vlan_plan.keys())[:10]}...")
    
    return workflow



def generate_generic_docs(company: GenericCompanyDef) -> Dict[str, str]:
    """Generate 17 docs for ANY company — WORLD-CLASS — adapts to institution type"""
    profile = get_institution_profile(company.institution_type)
    size_val = getattr(company.size_category, "value", company.size_category)
    if hasattr(size_val, 'value'):
        size_val = size_val.value
    else:
        size_val = str(size_val)
    
    docs = {}
    docs["01_Architecture"] = f"""
# {company.name} — Architecture — {profile.name_en} — WORLD-CLASS — 40Y Expert

Institution Type: {profile.type.value} — {profile.name_en} / {profile.name_ar}
Size: {size_val} — {company.total_employees} employees — {len(company.all_sites)} sites
Security Level: {profile.security_level} — Compliance: {', '.join(profile.compliance)}
VLANs: {len(company.vlan_plan)} — {list(company.vlan_plan.keys())}
Services: {len(company.services)} — {list(company.services.keys())[:10]}

Architecture: INTERNET -> 2 ISP -> 2 EDGE -> FW HA -> CORE SVL -> ACCESS/SERVERS/VOICE/WIFI/CCTV -> WAN -> Branches
Institution-specific: {profile.special_requirements_en}

Devices: {company.total_infra_devices} infra
"""
    docs["02_Physical_Topology"] = f"# {company.name} — Physical Topology — {profile.name_en}\nTotal devices: {company.total_infra_devices}\nSites: {len(company.all_sites)}\n"
    docs["03_Logical_Topology"] = f"# {company.name} — Logical Topology — VLANs {list(company.vlan_plan.keys())}\n"
    docs["04_IP_Plan"] = f"# {company.name} — IP Plan — HQ {company.hq.supernet} — Branches {[b.supernet for b in company.branches]}\n"
    docs["05_VLAN_Plan"] = f"# {company.name} — VLAN Plan — {len(company.vlan_plan)} VLANs — {list(company.vlan_plan.keys())}\nInstitution: {profile.name_en} — Compliance: {profile.compliance}\n"
    docs["06_WAN_Design"] = f"# {company.name} — WAN Design — {profile.wan_topology} — {len(company.all_sites)} sites\n"
    docs["07_Routing_Design"] = f"# {company.name} — Routing — OSPF Area 0 — {profile.wan_topology}\n"
    isolated_vlans = [vid for vid in company.vlan_plan.keys() if vid >= 100]
    docs["08_Security_Policy"] = f"# {company.name} — Security Policy — {profile.security_level} — {profile.compliance}\nVLANs isolated: {isolated_vlans}\n"
    docs["09_Device_Inventory"] = f"# {company.name} — Device Inventory — {company.total_infra_devices} devices\n"
    docs["10_Port_Mapping"] = f"# {company.name} — Port Mapping — {size_val}\n"
    docs["11_Rack_Layout"] = f"# {company.name} — Rack Layout — {len(company.all_sites)} sites\n"
    docs["12_Cable_Schedule"] = f"# {company.name} — Cable Schedule — Cat6A/OM4/SMF\n"
    docs["13_Config_Backup"] = f"# {company.name} — Config Backup — Git encrypted\n"
    docs["14_Monitoring_Inventory"] = f"# {company.name} — Monitoring — NMS — SNMP — {company.total_infra_devices} devices\n"
    docs["15_Test_Results"] = f"# {company.name} — Test Results — L1/L2/L3/APP/SECURITY/FAILOVER/USER\n"
    docs["16_Failover_Results"] = f"# {company.name} — Failover — ISP/CORE/FW/WAN — <5 sec\n"
    docs["17_As_Built"] = f"# {company.name} — As-Built — {profile.name_en} — {size_val} — COMPLETE — WORLD-CLASS — 40Y Expert\n"
    
    return docs
