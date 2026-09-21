"""
Al-Nour Trading & Services — REAL company spec — 40Y expert — ULTRA LEGENDARY
HQ + 3 branches — from zero to handover — microscopic precision

This file is the SINGLE SOURCE OF TRUTH for the entire project.
Every other file (fabric, configs, docs, testing) derives from here.
No hallucinations, no randomness — REAL engineering.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass(frozen=True)
class SiteSpec:
    site_id: str
    name: str
    name_ar: str
    employees: int
    user_devices: int
    ip_phones: int
    aps: int
    cctv: int
    printers: int
    supernet: str  # e.g. 10.10.0.0/16
    vlans: List[int]
    is_hq: bool = False

@dataclass(frozen=True)
class VlanDef:
    vlan_id: int
    name: str
    name_ar: str
    purpose: str
    subnet_template: str  # e.g. 10.{site_octet}.10.0/24 with {site_octet} replaced
    gateway_template: str
    description: str
    qos: bool = False
    voice: bool = False
    isolated: bool = False

@dataclass(frozen=True)
class CompanyDef:
    name: str
    name_ar: str
    domain: str
    hq: SiteSpec
    branches: List[SiteSpec]
    @property
    def all_sites(self) -> List[SiteSpec]:
        return [self.hq] + self.branches
    @property
    def total_employees(self) -> int:
        return sum(s.employees for s in self.all_sites)
    @property
    def total_devices(self) -> int:
        # Network infra estimate: HQ 2 edge + 2 fw + 2 core + ~12 access + servers
        # BR1: 1 fw + 3 sw, BR2: 1 fw + 2 sw, BR3: 1 fw + 2 sw
        return 2+2+2+12 + 1+3 + 1+2 + 1+2 + 24+8+6+4 + 12+4+3+2  # infra + cctv + aps

# ── VLAN Plan — GLOBAL — HQ + Branches share same VLAN IDs ──────────────
VLAN_PLAN: Dict[int, VlanDef] = {
    10: VlanDef(10, "USERS", "المستخدمين", "Employee data", "10.{octet}.10.0/24", "10.{octet}.10.1", "Employee workstations, laptops — 802.1X optional"),
    20: VlanDef(20, "VOICE", "الصوت", "VoIP", "10.{octet}.20.0/24", "10.{octet}.20.1", "IP Phones — Voice VLAN, QoS EF, PoE", qos=True, voice=True),
    30: VlanDef(30, "SERVERS", "الخوادم", "Servers", "10.{octet}.30.0/24", "10.{octet}.30.1", "AD, DNS, DHCP, ERP, File, Backup, NMS — HQ only for most"),
    40: VlanDef(40, "MANAGEMENT", "الإدارة", "Management", "10.{octet}.40.0/24", "10.{octet}.40.1", "Switch mgmt, AP mgmt, FW mgmt, controllers — admin only"),
    50: VlanDef(50, "PRINTERS", "الطابعات", "Printers", "10.{octet}.50.0/24", "10.{octet}.50.1", "Network printers, MFPs"),
    60: VlanDef(60, "CCTV", "الكاميرات", "CCTV", "10.{octet}.60.0/24", "10.{octet}.60.1", "IP Cameras, NVR — isolated, ALLOW to NVR only", isolated=True),
    70: VlanDef(70, "CORP-WIFI", "واي فاي الشركة", "Corporate Wi-Fi", "10.{octet}.70.0/24", "10.{octet}.70.1", "Corporate SSID Company-Corp — WPA2-Enterprise, VLAN 70"),
    80: VlanDef(80, "GUEST", "الضيوف", "Guest Wi-Fi", "10.{octet}.80.0/24", "10.{octet}.80.1", "Guest SSID Company-Guest — captive portal, Internet only, isolated", isolated=True),
    90: VlanDef(90, "IOT", "إنترنت الأشياء", "IoT", "10.{octet}.90.0/24", "10.{octet}.90.1", "IoT devices — HQ only, isolated"),
}

# ── Sites ─────────────────────────────────────────────────────────────────
HQ_SITE = SiteSpec(
    site_id="HQ",
    name="Headquarters",
    name_ar="المقر الرئيسي",
    employees=180,
    user_devices=220,
    ip_phones=120,
    aps=12,
    cctv=24,
    printers=8,
    supernet="10.10.0.0/16",
    vlans=[10,20,30,40,50,60,70,80,90],
    is_hq=True,
)

BRANCH_SITES = [
    SiteSpec(
        site_id="BR01",
        name="Branch 1 — Industrial District",
        name_ar="الفرع 1 — المنطقة الصناعية",
        employees=60,
        user_devices=70,
        ip_phones=35,
        aps=4,
        cctv=8,
        printers=3,
        supernet="10.11.0.0/16",
        vlans=[10,20,40,50,60,70,80],
    ),
    SiteSpec(
        site_id="BR02",
        name="Branch 2 — Commercial District",
        name_ar="الفرع 2 — المنطقة التجارية",
        employees=40,
        user_devices=48,
        ip_phones=25,
        aps=3,
        cctv=6,
        printers=2,
        supernet="10.12.0.0/16",
        vlans=[10,20,40,50,60,70,80],
    ),
    SiteSpec(
        site_id="BR03",
        name="Branch 3 — Port Area",
        name_ar="الفرع 3 — منطقة الميناء",
        employees=25,
        user_devices=30,
        ip_phones=15,
        aps=2,
        cctv=4,
        printers=1,
        supernet="10.13.0.0/16",
        vlans=[10,20,40,50,60,70,80],
    ),
]

AL_NOUR_COMPANY = CompanyDef(
    name="Al-Nour Trading & Services",
    name_ar="شركة النور للتجارة والخدمات",
    domain="alnour.local",
    hq=HQ_SITE,
    branches=BRANCH_SITES,
)

# ── IP Plan — per site octet mapping ──────────────────────────────────────
# HQ 10.10.x, BR01 10.11.x, BR02 10.12.x, BR03 10.13.x
SITE_OCTET = {
    "HQ": 10,
    "BR01": 11,
    "BR02": 12,
    "BR03": 13,
}

def site_subnet(site_id: str, vlan_id: int) -> str:
    octet = SITE_OCTET[site_id]
    v = VLAN_PLAN[vlan_id]
    return v.subnet_template.format(octet=octet)

def site_gateway(site_id: str, vlan_id: int) -> str:
    octet = SITE_OCTET[site_id]
    v = VLAN_PLAN[vlan_id]
    return v.gateway_template.format(octet=octet)

IP_PLAN = {
    "HQ": {vid: site_subnet("HQ", vid) for vid in HQ_SITE.vlans},
    "BR01": {vid: site_subnet("BR01", vid) for vid in BRANCH_SITES[0].vlans},
    "BR02": {vid: site_subnet("BR02", vid) for vid in BRANCH_SITES[1].vlans},
    "BR03": {vid: site_subnet("BR03", vid) for vid in BRANCH_SITES[2].vlans},
}

# ── WAN Design ────────────────────────────────────────────────────────────
WAN_DESIGN = {
    "type": "IPsec Site-to-Site + SD-WAN ready",
    "topology": "Hub & Spoke — HQ hub, branches spokes",
    "hq_wan": ["10.10.100.0/30 ISP1", "10.10.101.0/30 ISP2"],
    "tunnels": [
        {"from": "HQ", "to": "BR01", "subnet": "10.255.1.0/30", "ipsec": True},
        {"from": "HQ", "to": "BR02", "subnet": "10.255.2.0/30", "ipsec": True},
        {"from": "HQ", "to": "BR03", "subnet": "10.255.3.0/30", "ipsec": True},
    ],
    "routing": "OSPF + static for Internet, IPsec for inter-site",
    "policy": "BR→HQ ALLOW for ERP/DNS/AD, GUEST→HQ DENY, BR↔BR DENY by default",
}

# ── Services — HQ ─────────────────────────────────────────────────────────
SERVICES = {
    "AD": ["AD01 10.10.30.10", "AD02 10.10.30.11"],
    "DNS": ["DNS01 10.10.30.10", "DNS02 10.10.30.11 — same as AD"],
    "DHCP": ["DHCP01 10.10.30.10", "DHCP02 10.10.30.11 — split scope"],
    "ERP": ["ERP01 10.10.30.20 — TCP 443, 1433"],
    "FILE": ["FILE01 10.10.30.21 — SMB 445"],
    "BACKUP": ["BACKUP01 10.10.30.22 — Veeam"],
    "NMS": ["NMS01 10.10.30.30 — SNMP, Syslog, NetFlow"],
    "SYSLOG": ["SYSLOG01 10.10.30.31 — UDP 514"],
    "NVR": ["NVR01 10.10.30.40 — HQ CCTV, BR NVR local + central"],
    "WLC": ["WLC01 10.10.40.5 — Wireless Controller"],
}

# ── Physical Inventory — REAL ─────────────────────────────────────────────
PHYSICAL_INVENTORY = {
    "HQ": {
        "EDGE": ["EDGE-01 — Cisco ISR 4331 — ISP1", "EDGE-02 — Cisco ISR 4331 — ISP2"],
        "FIREWALL": ["FW-01 — Fortinet FG-100F — HA Active", "FW-02 — Fortinet FG-100F — HA Passive"],
        "CORE": ["CORE-01 — Cisco C9500-24Q — StackWise Virtual", "CORE-02 — Cisco C9500-24Q — StackWise Virtual"],
        "ACCESS": [f"ACC-HQ-{i:02d} — Cisco C9300-48P — PoE+ — {['USERS/VOICE','CCTV/WIFI','SERVERS/MGMT'][i%3]}" for i in range(1, 13)],
        "SERVERS": ["AD01/02, DNS, DHCP, ERP, FILE, BACKUP, NMS, SYSLOG, NVR"],
        "WIRELESS": ["WLC-01 + 12x Cisco 3802 APs"],
        "CCTV": ["24x Hikvision DS-2CD2143 + NVR DS-7732"],
        "UPS": ["APC SRT10KXLT — 10kVA — 30min"],
    },
    "BR01": {
        "FIREWALL": ["FW-BR01-01 — Fortinet FG-60F"],
        "SWITCHES": ["SW-BR01-01 — C9300-48P — PoE+", "SW-BR01-02 — C9300-48P — PoE+", "SW-BR01-03 — C9300-24P — PoE+"],
        "WIRELESS": ["4x Cisco 3802 APs — via WLC HQ"],
        "CCTV": ["8x Hikvision + NVR local"],
    },
    "BR02": {
        "FIREWALL": ["FW-BR02-01 — Fortinet FG-60F"],
        "SWITCHES": ["SW-BR02-01 — C9300-48P — PoE+", "SW-BR02-02 — C9300-24P — PoE+"],
        "WIRELESS": ["3x Cisco 3802 APs"],
        "CCTV": ["6x Hikvision + NVR local"],
    },
    "BR03": {
        "FIREWALL": ["FW-BR03-01 — Fortinet FG-60F"],
        "SWITCHES": ["SW-BR03-01 — C9300-24P — PoE+", "SW-BR03-02 — C9300-24P — PoE+"],
        "WIRELESS": ["2x Cisco 3802 APs"],
        "CCTV": ["4x Hikvision + NVR local"],
    },
}
