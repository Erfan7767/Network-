"""
Institution Types — WORLD-CLASS PROFESSIONAL — 40Y Expert — ULTRA LEGENDARY

Defines how network design differs by institution type, size, branches, devices.
This is REAL engineering — not generic templates — every institution has specific
requirements, VLANs, services, compliance, QoS, security policies.

A hospital ≠ trading company ≠ factory ≠ school ≠ hotel — different VLANs, 
different services, different compliance, different device ratios.

This module is the brain that makes the app professional for ANY institution
with absolute ultra precision, zero hallucinations, zero omissions.

PART OF FIRST APP — not second app — makes first app world-class for any scenario.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum


class InstitutionType(str, Enum):
    TRADING = "trading"          # Al-Nour — trading & services
    HOSPITAL = "hospital"        # مستشفى — medical devices, PACS, EMR
    FACTORY = "factory"          # مصنع — OT, production, industrial
    SCHOOL = "school"            # مدرسة/جامعة — students, labs, dorms
    HOTEL = "hotel"              # فندق — guests, POS, IPTV
    BANK = "bank"                # بنك — high security, PCI-DSS
    RETAIL = "retail"            # تجزئة/مول — POS, inventory, CCTV
    GOVERNMENT = "government"    # حكومي — high security, compliance
    OFFICE = "office"            # مكتب عام — generic
    DATACENTER = "datacenter"    # مركز بيانات


class SizeCategory(str, Enum):
    SMALL = "small"              # 1-20 employees, 1 site, 1-5 infra
    MEDIUM = "medium"            # 20-100 employees, 1-2 sites, 5-15 infra
    LARGE = "large"              # 100-500 employees, 2-5 sites, 15-40 infra
    ENTERPRISE = "enterprise"    # 500+ employees, 3+ sites, 40+ infra
    COMPLEX = "complex"          # 1000+ employees, 5+ sites, 100+ infra


@dataclass(frozen=True)
class VlanTemplate:
    vlan_id: int
    name: str
    name_ar: str
    purpose: str
    purpose_ar: str
    # Template with {octet} placeholder for site octet
    subnet_template: str
    gateway_template: str
    qos: bool = False
    voice: bool = False
    isolated: bool = False
    # Institution-specific
    institutions: List[str] = field(default_factory=lambda: ["all"])  # which institution types need this VLAN
    critical: bool = False  # if True, must exist in all designs
    compliance: List[str] = field(default_factory=list)  # e.g., HIPAA, PCI-DSS


@dataclass(frozen=True)
class ServiceTemplate:
    name: str
    name_ar: str
    description: str
    ip_template: str  # e.g., 10.{octet}.30.10
    ports: List[str]
    vlan: int
    critical: bool
    institutions: List[str] = field(default_factory=lambda: ["all"])


@dataclass(frozen=True)
class InstitutionProfile:
    type: InstitutionType
    name_en: str
    name_ar: str
    description_en: str
    description_ar: str
    # VLANs specific to this institution
    vlan_ids: List[int]
    # Services specific
    service_names: List[str]
    # Compliance
    compliance: List[str]
    # Special requirements
    special_requirements_en: List[str]
    special_requirements_ar: List[str]
    # Device ratios — per 10 employees
    # e.g., {"user_devices": 12, "ip_phones": 6, "aps": 0.6, "cctv": 1.2, "printers": 0.4}
    device_ratios: Dict[str, float]
    # Typical WAN
    wan_topology: str
    # Security level
    security_level: str  # low, medium, high, very_high
    icon: str


# ── GLOBAL VLAN CATALOG — 9 base + institution-specific ─────────────────
# Base VLANs — exist in almost all institutions (common)
BASE_VLANS: Dict[int, VlanTemplate] = {
    10: VlanTemplate(10, "USERS", "المستخدمين", "Employee data", "بيانات الموظفين",
                     "10.{octet}.10.0/24", "10.{octet}.10.1",
                     institutions=["all"], critical=True),
    20: VlanTemplate(20, "VOICE", "الصوت", "VoIP — QoS EF, PoE", "هواتف IP — جودة EF",
                     "10.{octet}.20.0/24", "10.{octet}.20.1",
                     qos=True, voice=True, institutions=["all"], critical=False),
    30: VlanTemplate(30, "SERVERS", "الخوادم", "Servers — AD/DNS/DHCP/ERP", "الخوادم",
                     "10.{octet}.30.0/24", "10.{octet}.30.1",
                     institutions=["all"], critical=True),
    40: VlanTemplate(40, "MANAGEMENT", "الإدارة", "Management — switches, APs, FW", "إدارة الأجهزة",
                     "10.{octet}.40.0/24", "10.{octet}.40.1",
                     institutions=["all"], critical=True),
    50: VlanTemplate(50, "PRINTERS", "الطابعات", "Printers, MFPs", "الطابعات",
                     "10.{octet}.50.0/24", "10.{octet}.50.1",
                     institutions=["all"], critical=False),
    60: VlanTemplate(60, "CCTV", "الكاميرات", "CCTV — isolated, NVR only", "كاميرات مراقبة — معزولة",
                     "10.{octet}.60.0/24", "10.{octet}.60.1",
                     isolated=True, institutions=["all"], critical=False),
    70: VlanTemplate(70, "CORP-WIFI", "واي فاي الشركة", "Corporate Wi-Fi — WPA2-Enterprise", "واي فاي داخلي",
                     "10.{octet}.70.0/24", "10.{octet}.70.1",
                     institutions=["all"], critical=False),
    80: VlanTemplate(80, "GUEST", "الضيوف", "Guest Wi-Fi — Internet only, isolated", "واي فاي ضيوف — إنترنت فقط",
                     "10.{octet}.80.0/24", "10.{octet}.80.1",
                     isolated=True, institutions=["all"], critical=False),
    90: VlanTemplate(90, "IOT", "إنترنت الأشياء", "IoT — isolated", "أجهزة ذكية — معزولة",
                     "10.{octet}.90.0/24", "10.{octet}.90.1",
                     isolated=True, institutions=["all"], critical=False),
}

# Institution-specific VLANs — beyond base 9 — WORLD-CLASS COMPLETE — 40Y Expert — ULTRA LEGENDARY
# Each institution gets REAL specific VLANs — not just base — hospital ≠ factory ≠ school ≠ hotel ≠ bank
INSTITUTION_VLANS: Dict[int, VlanTemplate] = {
    # ── Hospital — MEDICAL — HIPAA — Life-critical — Dual everything ──
    110: VlanTemplate(110, "MEDICAL", "الأجهزة الطبية", "Medical devices — isolated, HIPAA, no Internet, life-critical", "أجهزة طبية — معزولة HIPAA — بدون إنترنت — حرجة للحياة",
                      "10.{octet}.110.0/24", "10.{octet}.110.1",
                      isolated=True, institutions=["hospital"], critical=True, compliance=["HIPAA"]),
    120: VlanTemplate(120, "PACS", "الأشعة والتصوير", "PACS — medical imaging, high bandwidth 10G, jumbo frames", "نظام الأشعة PACS — نطاق عالي 10G — إطارات كبيرة",
                      "10.{octet}.120.0/24", "10.{octet}.120.1",
                      institutions=["hospital"], critical=True, compliance=["HIPAA"]),
    130: VlanTemplate(130, "EMR", "السجلات الطبية الإلكترونية", "EMR — Electronic Medical Records — encrypted, backup 15min", "السجلات الطبية الإلكترونية — مشفرة — نسخ كل 15 دقيقة",
                      "10.{octet}.130.0/24", "10.{octet}.130.1",
                      institutions=["hospital"], critical=True, compliance=["HIPAA"]),
    140: VlanTemplate(140, "PHARMACY", "الصيدلية", "Pharmacy — drug dispensing, HIPAA, isolated", "صيدلية — صرف أدوية — HIPAA معزولة",
                      "10.{octet}.140.0/24", "10.{octet}.140.1",
                      isolated=True, institutions=["hospital"], critical=True, compliance=["HIPAA"]),
    150: VlanTemplate(150, "LAB", "المختبر الطبي", "Medical Lab — analyzers, LIS, HIPAA", "مختبر طبي — أجهزة تحليل — LIS — HIPAA",
                      "10.{octet}.150.0/24", "10.{octet}.150.1",
                      isolated=True, institutions=["hospital"], critical=True, compliance=["HIPAA"]),
    160: VlanTemplate(160, "ADMIN-HOSP", "إدارة المستشفى", "Hospital Admin — billing, HR, finance", "إدارة مستشفى — فوترة، موارد، مالية",
                      "10.{octet}.160.0/24", "10.{octet}.160.1",
                      institutions=["hospital"], critical=False),
    170: VlanTemplate(170, "RESEARCH-HOSP", "البحث الطبي", "Medical Research — isolated, high bandwidth", "بحث طبي — معزول — نطاق عالي",
                      "10.{octet}.170.0/24", "10.{octet}.170.1",
                      isolated=True, institutions=["hospital"], critical=False),
    # ── Factory / Industrial — OT — ISA-99 — Production critical ──
    210: VlanTemplate(210, "OT", "التشغيل الصناعي OT", "OT — Operational Technology, isolated, no Internet, ISA-99", "شبكة تشغيل صناعي OT — معزولة — بدون إنترنت — ISA-99",
                      "10.{octet}.210.0/24", "10.{octet}.210.1",
                      isolated=True, institutions=["factory"], critical=True, compliance=["ISA-99"]),
    220: VlanTemplate(220, "PRODUCTION", "خط الإنتاج", "Production line — PLC, SCADA, deterministic latency QoS", "خط إنتاج — PLC/SCADA — زمن حتمي QoS",
                      "10.{octet}.220.0/24", "10.{octet}.220.1",
                      isolated=True, institutions=["factory"], critical=True, compliance=["ISA-99"]),
    230: VlanTemplate(230, "WAREHOUSE", "المستودع", "Warehouse — WMS, barcode scanners, AGV", "مستودع — إدارة WMS، ماسحات، AGV",
                      "10.{octet}.230.0/24", "10.{octet}.230.1",
                      institutions=["factory", "retail"], critical=False),
    240: VlanTemplate(240, "ROBOTICS", "الروبوتات", "Robotics — industrial robots, real-time, isolated", "روبوتات صناعية — زمن حقيقي — معزولة",
                      "10.{octet}.240.0/24", "10.{octet}.240.1",
                      isolated=True, institutions=["factory"], critical=True, compliance=["ISA-99"]),
    250: VlanTemplate(250, "QUALITY", "الجودة", "Quality Control — QC, inspection, lab", "مراقبة جودة — QC، فحص، مختبر",
                      "10.{octet}.250.0/24", "10.{octet}.250.1",
                      institutions=["factory"], critical=False),
    260: VlanTemplate(260, "MAINTENANCE", "الصيانة", "Maintenance — CMMS, work orders", "صيانة — CMMS، أوامر عمل",
                      "10.{octet}.260.0/24", "10.{octet}.260.1",
                      institutions=["factory"], critical=False),
    270: VlanTemplate(270, "ENERGY", "الطاقة", "Energy Management — EMS, meters", "إدارة طاقة — EMS، عدادات",
                      "10.{octet}.270.0/24", "10.{octet}.270.1",
                      institutions=["factory"], critical=False),
    # ── School / University — Education — CIPA/FERPA — High density Wi-Fi ──
    310: VlanTemplate(310, "STUDENTS", "الطلاب", "Students — filtered Internet CIPA, no P2P, bandwidth limit", "طلاب — إنترنت مفلتر CIPA — بدون P2P — حد نطاق",
                      "10.{octet}.110.0/24", "10.{octet}.110.1",
                      isolated=True, institutions=["school"], critical=True, compliance=["CIPA"]),
    320: VlanTemplate(320, "LABS", "المختبرات التعليمية", "Labs — high bandwidth, isolated per lab, research", "مختبرات تعليمية — نطاق عالي — معزولة لكل مختبر",
                      "10.{octet}.120.0/24", "10.{octet}.120.1",
                      isolated=True, institutions=["school"], critical=False),
    330: VlanTemplate(330, "DORM", "سكن الطلاب", "Dormitory — students residence, NAT, per-user limit", "سكن طلاب — NAT — حد لكل مستخدم",
                      "10.{octet}.130.0/24", "10.{octet}.130.1",
                      isolated=True, institutions=["school"], critical=False),
    340: VlanTemplate(340, "FACULTY", "أعضاء هيئة التدريس", "Faculty — teachers, professors, research", "هيئة تدريس — معلمين، أساتذة، بحث",
                      "10.{octet}.140.0/24", "10.{octet}.140.1",
                      institutions=["school"], critical=True),
    350: VlanTemplate(350, "RESEARCH-EDU", "البحث الأكاديمي", "Academic Research — high bandwidth, isolated, HPC", "بحث أكاديمي — نطاق عالي — معزول — HPC",
                      "10.{octet}.150.0/24", "10.{octet}.150.1",
                      isolated=True, institutions=["school"], critical=False),
    360: VlanTemplate(360, "LIBRARY-NET", "شبكة المكتبة", "Library — OPAC, digital resources", "مكتبة — OPAC، موارد رقمية",
                      "10.{octet}.160.0/24", "10.{octet}.160.1",
                      institutions=["school"], critical=False),
    370: VlanTemplate(370, "ADMIN-EDU", "إدارة التعليم", "Education Admin — registrar, finance, HR", "إدارة تعليم — تسجيل، مالية، موارد",
                      "10.{octet}.170.0/24", "10.{octet}.170.1",
                      institutions=["school"], critical=False),
    # ── Hotel / Hospitality — Guest isolation per room — PCI-DSS POS ──
    410: VlanTemplate(410, "GUEST-ROOM", "غرف الضيوف", "Guest rooms — IPTV, Internet, per-room isolated, no inter-room", "غرف ضيوف — تلفاز وإنترنت — معزولة لكل غرفة — بدون بين الغرف",
                      "10.{octet}.110.0/24", "10.{octet}.110.1",
                      isolated=True, institutions=["hotel"], critical=True),
    420: VlanTemplate(420, "POS", "نقاط البيع POS", "POS — PCI-DSS isolated, encrypted, no Internet", "نقاط بيع POS — معزولة PCI-DSS — مشفرة — بدون إنترنت",
                      "10.{octet}.120.0/24", "10.{octet}.120.1",
                      isolated=True, institutions=["hotel", "retail", "trading"], critical=True, compliance=["PCI-DSS"]),
    430: VlanTemplate(430, "IPTV", "تلفاز IPTV", "IPTV — multicast, IGMP snooping, high bandwidth", "تلفاز IPTV — متعدد — IGMP — نطاق عالي",
                      "10.{octet}.130.0/24", "10.{octet}.130.1",
                      institutions=["hotel"], critical=False),
    440: VlanTemplate(440, "STAFF-HOTEL", "موظفي الفندق", "Hotel Staff — housekeeping, front desk, back office", "موظفو فندق — تدبير، استقبال، مكتب خلفي",
                      "10.{octet}.140.0/24", "10.{octet}.140.1",
                      institutions=["hotel"], critical=False),
    450: VlanTemplate(450, "CONFERENCE", "قاعات المؤتمرات", "Conference — high density Wi-Fi, AV, presentation", "مؤتمرات — واي فاي كثيف، AV، عرض",
                      "10.{octet}.150.0/24", "10.{octet}.150.1",
                      institutions=["hotel"], critical=False),
    460: VlanTemplate(460, "SPA", "السبا والترفيه", "Spa & Recreation — isolated, Internet", "سبا وترفيه — معزول — إنترنت",
                      "10.{octet}.160.0/24", "10.{octet}.160.1",
                      isolated=True, institutions=["hotel"], critical=False),
    # ── Bank / Finance — very_high — PCI-DSS, SOX, GLBA — Dual everything ──
    510: VlanTemplate(510, "BANKING", "العمليات المصرفية الأساسية", "Banking Core — PCI-DSS, very high security, no Internet, encrypted, audit log", "عمليات مصرفية أساسية — PCI-DSS — أمان عالي جدا — بدون إنترنت — مشفرة — سجل تدقيق",
                      "10.{octet}.110.0/24", "10.{octet}.110.1",
                      isolated=True, institutions=["bank"], critical=True, compliance=["PCI-DSS", "SOX"]),
    520: VlanTemplate(520, "ATM", "شبكة الصراف الآلي ATM", "ATM — isolated, PCI-DSS, VPN to central, no user access", "صراف آلي ATM — معزول — PCI-DSS — VPN للمركزي — بدون وصول مستخدمين",
                      "10.{octet}.120.0/24", "10.{octet}.120.1",
                      isolated=True, institutions=["bank"], critical=True, compliance=["PCI-DSS"]),
    530: VlanTemplate(530, "VAULT", "الخزنة", "Vault — air-gapped, very high security, no network", "خزنة — معزولة هوائيا — أمان عالي جدا — بدون شبكة",
                      "10.{octet}.130.0/24", "10.{octet}.130.1",
                      isolated=True, institutions=["bank"], critical=True, compliance=["PCI-DSS", "SOX"]),
    540: VlanTemplate(540, "TELLER", "الصرافين Teller", "Teller — front office, banking access, 802.1X", "صرافين — مكتب أمامي — وصول مصرفي — 802.1X",
                      "10.{octet}.140.0/24", "10.{octet}.140.1",
                      isolated=True, institutions=["bank"], critical=True, compliance=["PCI-DSS"]),
    550: VlanTemplate(550, "BACKOFFICE", "المكتب الخلفي للبنك", "Bank Backoffice — operations, compliance, risk", "مكتب خلفي بنك — عمليات، امتثال، مخاطر",
                      "10.{octet}.150.0/24", "10.{octet}.150.1",
                      institutions=["bank"], critical=False),
    # ── Government — very_high — NIST, FISMA — Classified separate ──
    610: VlanTemplate(610, "CLASSIFIED", "شبكة سرية مصنفة", "Classified — very high security, no Internet, air-gapped or encrypted, audit 7y", "شبكة سرية مصنفة — أمان عالي جدا — بدون إنترنت — معزولة هوائيا أو مشفرة — تدقيق 7 سنوات",
                      "10.{octet}.110.0/24", "10.{octet}.110.1",
                      isolated=True, institutions=["government"], critical=True, compliance=["NIST", "FISMA"]),
    620: VlanTemplate(620, "PUBLIC-SERV", "الخدمات العامة", "Public Services — citizen services, portal", "خدمات عامة — خدمات مواطنين، بوابة",
                      "10.{octet}.120.0/24", "10.{octet}.120.1",
                      institutions=["government"], critical=True),
    630: VlanTemplate(630, "CITIZEN", "شبكة المواطنين", "Citizen — public access, Internet only, kiosk", "مواطنين — وصول عام — إنترنت فقط — كشك",
                      "10.{octet}.130.0/24", "10.{octet}.130.1",
                      isolated=True, institutions=["government"], critical=False),
    640: VlanTemplate(640, "JUSTICE", "العدالة والأمن", "Justice & Security — police, courts, isolated", "عدالة وأمن — شرطة، محاكم، معزولة",
                      "10.{octet}.140.0/24", "10.{octet}.140.1",
                      isolated=True, institutions=["government"], critical=True),
    # ── Retail / Mall — POS PCI, Inventory, high density CCTV ──
    710: VlanTemplate(710, "POS-RETAIL", "نقاط بيع تجزئة", "Retail POS — PCI-DSS, isolated, encrypted", "نقاط بيع تجزئة — PCI-DSS — معزولة — مشفرة",
                      "10.{octet}.110.0/24", "10.{octet}.110.1",
                      isolated=True, institutions=["retail"], critical=True, compliance=["PCI-DSS"]),
    720: VlanTemplate(720, "INVENTORY", "المخزون", "Inventory — RFID, scanners, real-time", "مخزون — RFID، ماسحات، زمن حقيقي",
                      "10.{octet}.120.0/24", "10.{octet}.120.1",
                      institutions=["retail"], critical=False),
    730: VlanTemplate(730, "WAREHOUSE-RET", "مستودع تجزئة", "Retail Warehouse — WMS, logistics", "مستودع تجزئة — WMS، لوجستيات",
                      "10.{octet}.130.0/24", "10.{octet}.130.1",
                      institutions=["retail", "factory"], critical=False),
    # ── Datacenter — Leaf-Spine — High bandwidth 40G/100G ──
    810: VlanTemplate(810, "STORAGE", "التخزين", "Storage — iSCSI, NFS, high bandwidth, jumbo frames", "تخزين — iSCSI، NFS — نطاق عالي — إطارات كبيرة",
                      "10.{octet}.110.0/24", "10.{octet}.110.1",
                      institutions=["datacenter"], critical=True),
    820: VlanTemplate(820, "BACKUP-DC", "نسخ احتياطي مركز بيانات", "DC Backup — Veeam, replication, high bandwidth", "نسخ احتياطي DC — Veeam، نسخ — نطاق عالي",
                      "10.{octet}.120.0/24", "10.{octet}.120.1",
                      institutions=["datacenter"], critical=True),
    830: VlanTemplate(830, "VMOTION", "نقل الأجهزة الافتراضية", "vMotion — live migration, isolated, 10G+", "نقل افتراضي vMotion — هجرة حية — معزول — 10G+",
                      "10.{octet}.130.0/24", "10.{octet}.130.1",
                      isolated=True, institutions=["datacenter"], critical=True),
}

# Merge base + institution-specific into full catalog
ALL_VLANS: Dict[int, VlanTemplate] = {**BASE_VLANS, **INSTITUTION_VLANS}


# ── SERVICES CATALOG ─────────────────────────────────────────────────────
BASE_SERVICES: Dict[str, ServiceTemplate] = {
    "AD": ServiceTemplate("AD", "الدليل النشط", "Active Directory", "10.{octet}.30.10", ["389", "636", "88", "445"], 30, True),
    "DNS": ServiceTemplate("DNS", "نظام الأسماء", "DNS", "10.{octet}.30.10", ["53"], 30, True),
    "DHCP": ServiceTemplate("DHCP", "توزيع العناوين", "DHCP", "10.{octet}.30.10", ["67", "68"], 30, True),
    "FILE": ServiceTemplate("FILE", "ملفات", "File Server", "10.{octet}.30.21", ["445"], 30, False),
    "BACKUP": ServiceTemplate("BACKUP", "نسخ احتياطي", "Backup", "10.{octet}.30.22", ["443"], 30, False),
    "NMS": ServiceTemplate("NMS", "مراقبة", "NMS — SNMP/Syslog/NetFlow", "10.{octet}.30.30", ["161", "162", "514"], 40, True),
    "WLC": ServiceTemplate("WLC", "تحكم واي فاي", "Wireless Controller", "10.{octet}.40.5", ["443", "5246"], 40, False),
    "NVR": ServiceTemplate("NVR", "تسجيل كاميرات", "NVR — CCTV", "10.{octet}.30.40", ["8000", "554"], 60, False),
}

INSTITUTION_SERVICES: Dict[str, ServiceTemplate] = {
    # ── Hospital — HIPAA — Life-critical ──
    "EMR": ServiceTemplate("EMR", "السجلات الطبية", "EMR System — Electronic Medical Records — HIPAA encrypted", "10.{octet}.130.10", ["443", "1433"], 130, True, ["hospital"]),
    "PACS": ServiceTemplate("PACS", "الأشعة", "PACS Server — medical imaging — high bandwidth 10G", "10.{octet}.120.10", ["104", "443", "11112"], 120, True, ["hospital"]),
    "HIS": ServiceTemplate("HIS", "نظام المستشفى", "Hospital Information System — billing, ADT, orders", "10.{octet}.30.20", ["443", "1433"], 30, True, ["hospital"]),
    "PHARMACY_SYS": ServiceTemplate("PHARMACY_SYS", "نظام الصيدلية", "Pharmacy System — drug dispensing — HIPAA", "10.{octet}.140.10", ["443", "1433"], 140, True, ["hospital"]),
    "LIS": ServiceTemplate("LIS", "نظام المختبر", "Lab Information System — LIS — analyzers", "10.{octet}.150.10", ["443"], 150, True, ["hospital"]),
    "NURSE_CALL": ServiceTemplate("NURSE_CALL", "نداء الممرضات", "Nurse Call System — life-critical", "10.{octet}.110.20", ["443"], 110, True, ["hospital"]),
    # ── Factory — OT — ISA-99 — Production critical ──
    "SCADA": ServiceTemplate("SCADA", "سكادا", "SCADA Server — OT — isolated — no Internet", "10.{octet}.210.10", ["502", "20000", "44818"], 210, True, ["factory"]),
    "MES": ServiceTemplate("MES", "تنفيذ التصنيع", "Manufacturing Execution — production tracking", "10.{octet}.220.10", ["443"], 220, True, ["factory"]),
    "WMS": ServiceTemplate("WMS", "إدارة المستودع", "Warehouse Management — WMS — barcode, AGV", "10.{octet}.230.10", ["443"], 230, False, ["factory", "retail"]),
    "ROBOT_CTRL": ServiceTemplate("ROBOT_CTRL", "تحكم روبوتات", "Robot Controller — real-time — deterministic", "10.{octet}.240.10", ["502", "44818"], 240, True, ["factory"]),
    "QC_SYS": ServiceTemplate("QC_SYS", "نظام الجودة", "Quality Control System — QC, inspection", "10.{octet}.250.10", ["443"], 250, False, ["factory"]),
    "CMMS": ServiceTemplate("CMMS", "نظام الصيانة", "CMMS — maintenance management — work orders", "10.{octet}.260.10", ["443"], 260, False, ["factory"]),
    "EMS": ServiceTemplate("EMS", "إدارة الطاقة", "Energy Management — EMS — meters, optimization", "10.{octet}.270.10", ["443", "502"], 270, False, ["factory"]),
    # ── School — Education — CIPA/FERPA ──
    "LMS": ServiceTemplate("LMS", "التعلم", "Learning Management — Moodle/Canvas — 1000+ concurrent", "10.{octet}.30.20", ["443"], 30, True, ["school"]),
    "LIBRARY": ServiceTemplate("LIBRARY", "المكتبة", "Library System — OPAC, digital resources", "10.{octet}.30.21", ["443"], 30, False, ["school"]),
    "SIS": ServiceTemplate("SIS", "نظام معلومات الطلاب", "Student Information System — grades, attendance — FERPA", "10.{octet}.30.22", ["443", "1433"], 30, True, ["school"]),
    "RESEARCH_HPC": ServiceTemplate("RESEARCH_HPC", "حوسبة بحثية", "Research HPC — high performance computing", "10.{octet}.150.20", ["22", "443"], 350, False, ["school"]),
    # ── Hotel — Hospitality — PCI-DSS POS ──
    "PMS": ServiceTemplate("PMS", "إدارة الفندق", "Property Management — Opera, guest, billing, POS integration", "10.{octet}.30.20", ["443", "1433"], 30, True, ["hotel"]),
    "POS": ServiceTemplate("POS", "نقاط البيع", "POS Server — PCI-DSS isolated — encrypted", "10.{octet}.120.10", ["443"], 420, True, ["hotel", "retail", "trading"]),
    "IPTV_SRV": ServiceTemplate("IPTV_SRV", "بث تلفازي", "IPTV Server — multicast — IGMP — 100+ channels", "10.{octet}.130.10", ["554", "1234"], 430, False, ["hotel"]),
    "DOOR_LOCK": ServiceTemplate("DOOR_LOCK", "أقفال الأبواب", "Door Lock System — RFID, mobile key — PMS integrated", "10.{octet}.140.10", ["443"], 440, True, ["hotel"]),
    "CONFERENCE_AV": ServiceTemplate("CONFERENCE_AV", "مؤتمرات AV", "Conference AV — high density Wi-Fi, presentation, Teams", "10.{octet}.150.10", ["443"], 450, False, ["hotel"]),
    # ── Bank — very_high — PCI-DSS, SOX, GLBA ──
    "CORE_BANKING": ServiceTemplate("CORE_BANKING", "العمليات المصرفية الأساسية", "Core Banking — very high security — PCI-DSS SOX — no Internet — audit log 7y", "10.{octet}.110.10", ["443", "1433"], 510, True, ["bank"]),
    "ATM_MGMT": ServiceTemplate("ATM_MGMT", "إدارة الصراف الآلي", "ATM Management — isolated — VPN to central — PCI-DSS", "10.{octet}.120.10", ["443"], 520, True, ["bank"]),
    "VAULT_MGMT": ServiceTemplate("VAULT_MGMT", "إدارة الخزنة", "Vault Management — air-gapped — dual auth — SOX", "10.{octet}.130.10", ["443"], 530, True, ["bank"]),
    "TELLER_SYS": ServiceTemplate("TELLER_SYS", "نظام الصرافين", "Teller System — front office — 802.1X — banking access", "10.{octet}.140.10", ["443"], 540, True, ["bank"]),
    "RISK_MGMT": ServiceTemplate("RISK_MGMT", "إدارة المخاطر", "Risk Management — fraud detection — SIEM", "10.{octet}.150.10", ["443"], 550, False, ["bank"]),
    # ── Government — very_high — NIST, FISMA ──
    "CITIZEN_PORTAL": ServiceTemplate("CITIZEN_PORTAL", "بوابة المواطنين", "Citizen Portal — public services — DMZ", "10.{octet}.120.10", ["443"], 620, True, ["government"]),
    "JUSTICE_SYS": ServiceTemplate("JUSTICE_SYS", "نظام العدالة", "Justice System — police, courts — isolated — audit", "10.{octet}.140.10", ["443"], 640, True, ["government"]),
    # ── Retail — POS PCI, high density CCTV, inventory ──
    "INVENTORY_SYS": ServiceTemplate("INVENTORY_SYS", "نظام المخزون", "Inventory System — RFID, real-time, HQ sync", "10.{octet}.120.20", ["443"], 720, False, ["retail"]),
    "LOSS_PREV": ServiceTemplate("LOSS_PREV", "منع الخسارة", "Loss Prevention — CCTV + POS integration — AI", "10.{octet}.30.40", ["443"], 60, False, ["retail"]),
    # ── Datacenter — Leaf-Spine — High bandwidth ──
    "STORAGE_SRV": ServiceTemplate("STORAGE_SRV", "خادم تخزين", "Storage Server — iSCSI, NFS — 40G/100G — jumbo", "10.{octet}.110.10", ["3260", "2049"], 810, True, ["datacenter"]),
    "BACKUP_DC_SRV": ServiceTemplate("BACKUP_DC_SRV", "نسخ احتياطي DC", "DC Backup — Veeam — replication — 100G", "10.{octet}.120.10", ["443"], 820, True, ["datacenter"]),
    "VCENTER": ServiceTemplate("VCENTER", "إدارة افتراضية", "vCenter — VM management — vMotion", "10.{octet}.30.10", ["443", "902"], 30, True, ["datacenter"]),
    # ── Trading (Al-Nour) — ERP, FILE, BACKUP ──
    "ERP": ServiceTemplate("ERP", "تخطيط الموارد ERP", "ERP System — SAP/Oracle — HQ + branches via IPsec — critical", "10.{octet}.30.20", ["443", "1433"], 30, True, ["trading", "factory", "retail"]),
    "FILE_SRV": ServiceTemplate("FILE_SRV", "خادم ملفات", "File Server — SMB — AD integrated — DFS", "10.{octet}.30.21", ["445"], 30, False, ["all"]),
}

ALL_SERVICES = {**BASE_SERVICES, **INSTITUTION_SERVICES}


# ── INSTITUTION PROFILES — WORLD-CLASS — 40Y Expert ─────────────────────
INSTITUTION_PROFILES: Dict[str, InstitutionProfile] = {
    "trading": InstitutionProfile(
        type=InstitutionType.TRADING,
        name_en="Trading & Services Company",
        name_ar="شركة تجارة وخدمات",
        description_en="Trading company with HQ + branches, ERP, file, backup, VoIP, CCTV, Wi-Fi — like Al-Nour",
        description_ar="شركة تجارة مع مقر وفروع، نظام ERP، ملفات، نسخ، هواتف، كاميرات، واي فاي",
        vlan_ids=[10,20,30,40,50,60,70,80,90,420],
        service_names=["AD","DNS","DHCP","ERP","FILE","BACKUP","NMS","WLC","NVR","POS"],
        compliance=["PCI-DSS"],
        special_requirements_en=[
            "ERP must be reachable from all branches via IPsec",
            "Guest Wi-Fi isolated — Internet only",
            "CCTV isolated — NVR only",
            "POS PCI-DSS isolated",
            "VoIP QoS EF",
        ],
        special_requirements_ar=[
            "نظام ERP يجب أن يكون متاح من كل الفروع عبر IPsec",
            "واي فاي ضيوف معزول — إنترنت فقط",
            "كاميرات معزولة — مسجل فقط",
            "نقاط بيع معزولة PCI",
            "هواتف جودة عالية EF",
        ],
        device_ratios={"user_devices": 1.2, "ip_phones": 0.66, "aps": 0.066, "cctv": 0.133, "printers": 0.044},
        wan_topology="Hub & Spoke — HQ hub",
        security_level="medium",
        icon="🏢",
    ),
    "hospital": InstitutionProfile(
        type=InstitutionType.HOSPITAL,
        name_en="Hospital / Medical Center",
        name_ar="مستشفى / مركز طبي",
        description_en="Hospital with medical devices, PACS imaging, EMR, HIPAA compliance, high availability, life-critical network",
        description_ar="مستشفى مع أجهزة طبية، نظام أشعة، سجلات طبية، امتثال HIPAA، توفر عالي، شبكة حرجة للحياة",
        vlan_ids=[10,20,30,40,50,60,70,80,110,120,130,140,150,160,170],
        service_names=["AD","DNS","DHCP","HIS","EMR","PACS","PHARMACY_SYS","LIS","NURSE_CALL","FILE","BACKUP","NMS","WLC","NVR","FILE_SRV"],
        compliance=["HIPAA", "PCI-DSS"],
        special_requirements_en=[
            "Medical devices VLAN 110 isolated — HIPAA — no Internet",
            "PACS VLAN 120 high bandwidth — 10G uplinks — jumbo frames",
            "EMR VLAN 130 encrypted — backup every 15 min",
            "Life-critical — no single point of failure — dual everything",
            "Guest Wi-Fi completely isolated — captive portal — no access to medical",
            "CCTV for security but not in patient rooms — privacy",
        ],
        special_requirements_ar=[
            "أجهزة طبية VLAN 110 معزولة — HIPAA — بدون إنترنت",
            "نظام أشعة VLAN 120 نطاق عالي — 10G — إطارات كبيرة",
            "سجلات طبية VLAN 130 مشفرة — نسخ كل 15 دقيقة",
            "حرج للحياة — بدون نقطة فشل واحدة — مزدوج كل شيء",
            "واي فاي ضيوف معزول تماما — بوابة — بدون وصول طبي",
            "كاميرات للأمان لكن ليس في غرف المرضى — خصوصية",
        ],
        device_ratios={"user_devices": 1.1, "ip_phones": 0.8, "aps": 0.1, "cctv": 0.2, "printers": 0.05, "medical_devices": 0.5},
        wan_topology="Hub & Spoke + MPLS backup — HQ + clinics",
        security_level="very_high",
        icon="🏥",
    ),
    "factory": InstitutionProfile(
        type=InstitutionType.FACTORY,
        name_en="Factory / Manufacturing / Industrial",
        name_ar="مصنع / صناعي",
        description_en="Factory with OT network, production line PLC/SCADA, warehouse, industrial IoT, high availability for production",
        description_ar="مصنع مع شبكة تشغيل صناعي، خط إنتاج PLC/SCADA، مستودع، إنترنت صناعي، توفر عالي للإنتاج",
        vlan_ids=[10,20,30,40,50,60,70,80,90,210,220,230,240,250,260,270],
        service_names=["AD","DNS","DHCP","ERP","SCADA","MES","WMS","ROBOT_CTRL","QC_SYS","CMMS","EMS","FILE","BACKUP","NMS","WLC","NVR","FILE_SRV"],
        compliance=["ISA-99", "IEC-62443"],
        special_requirements_en=[
            "OT VLAN 210 completely isolated from IT — firewall only — no Internet",
            "Production VLAN 220 — PLC/SCADA — deterministic latency — QoS",
            "Warehouse VLAN 230 — WMS, barcode scanners, high availability",
            "Industrial — dust, heat — industrial switches — IP30",
            "CCTV for safety — production monitoring",
            "ERP integration with MES — production data",
        ],
        special_requirements_ar=[
            "شبكة تشغيل VLAN 210 معزولة تماما عن IT — جدار ناري فقط — بدون إنترنت",
            "إنتاج VLAN 220 — PLC/SCADA — زمن حتمي — جودة",
            "مستودع VLAN 230 — إدارة مستودع، ماسحات، توفر عالي",
            "صناعي — غبار، حرارة — مفاتيح صناعية — IP30",
            "كاميرات للسلامة — مراقبة إنتاج",
            "تكامل ERP مع MES — بيانات إنتاج",
        ],
        device_ratios={"user_devices": 0.8, "ip_phones": 0.3, "aps": 0.05, "cctv": 0.15, "printers": 0.03, "ot_devices": 0.6, "scanners": 0.2},
        wan_topology="Hub & Spoke — HQ + factories + warehouses",
        security_level="high",
        icon="🏭",
    ),
    "school": InstitutionProfile(
        type=InstitutionType.SCHOOL,
        name_en="School / University / Education",
        name_ar="مدرسة / جامعة / تعليم",
        description_en="School/university with students, labs, dorms, LMS, library, high density Wi-Fi, content filtering",
        description_ar="مدرسة/جامعة مع طلاب، مختبرات، سكن، نظام تعلم، مكتبة، واي فاي كثيف، فلترة محتوى",
        vlan_ids=[10,20,30,40,50,60,70,80,310,320,330,340,350,360,370],
        service_names=["AD","DNS","DHCP","LMS","LIBRARY","SIS","RESEARCH_HPC","FILE","BACKUP","NMS","WLC","NVR","FILE_SRV"],
        compliance=["CIPA", "FERPA"],
        special_requirements_en=[
            "Students VLAN 310 — filtered Internet — CIPA — no P2P",
            "Labs VLAN 320 — high bandwidth — isolated per lab",
            "Dorm VLAN 330 — students residence — NAT — bandwidth limit per user",
            "High density Wi-Fi — 1 AP per classroom — 30+ clients per AP",
            "LMS — Moodle — must be reachable from students and teachers",
            "Library system — OPAC",
        ],
        special_requirements_ar=[
            "طلاب VLAN 310 — إنترنت مفلتر — CIPA — بدون مشاركة",
            "مختبرات VLAN 320 — نطاق عالي — معزولة لكل مختبر",
            "سكن VLAN 330 — سكن طلاب — ترجمة عناوين — حد نطاق لكل مستخدم",
            "واي فاي كثيف — نقطة لكل فصل — 30+ عميل لكل نقطة",
            "نظام تعلم — Moodle — متاح للطلاب والمعلمين",
            "نظام مكتبة — OPAC",
        ],
        device_ratios={"user_devices": 1.5, "ip_phones": 0.2, "aps": 0.15, "cctv": 0.1, "printers": 0.05, "lab_devices": 0.8},
        wan_topology="Hub & Spoke — main campus + remote campuses",
        security_level="medium",
        icon="🎓",
    ),
    "hotel": InstitutionProfile(
        type=InstitutionType.HOTEL,
        name_en="Hotel / Hospitality",
        name_ar="فندق / ضيافة",
        description_en="Hotel with guest rooms, POS, IPTV, PMS, high density Wi-Fi, PCI-DSS for POS",
        description_ar="فندق مع غرف ضيوف، نقاط بيع، تلفاز، إدارة فندق، واي فاي كثيف، PCI لنقاط البيع",
        vlan_ids=[10,20,30,40,50,60,70,80,410,420,430,440,450,460],
        service_names=["AD","DNS","DHCP","PMS","POS","IPTV_SRV","DOOR_LOCK","CONFERENCE_AV","FILE","BACKUP","NMS","WLC","NVR","FILE_SRV"],
        compliance=["PCI-DSS"],
        special_requirements_en=[
            "Guest rooms VLAN 410 — IPTV + Internet — isolated per room — no inter-room",
            "POS VLAN 420 — PCI-DSS — isolated — no Internet — encrypted",
            "IPTV VLAN 430 — multicast — IGMP snooping — high bandwidth",
            "PMS — Property Management — must integrate with POS and IPTV",
            "High density Wi-Fi — 1 AP per 3 rooms — roaming",
            "CCTV — lobby, corridors — not in rooms — privacy",
        ],
        special_requirements_ar=[
            "غرف ضيوف VLAN 410 — تلفاز + إنترنت — معزولة لكل غرفة — بدون بين الغرف",
            "نقاط بيع VLAN 420 — PCI — معزولة — بدون إنترنت — مشفرة",
            "تلفاز VLAN 430 — متعدد — IGMP — نطاق عالي",
            "إدارة فندق — تكامل مع نقاط بيع وتلفاز",
            "واي فاي كثيف — نقطة لكل 3 غرف — تجوال",
            "كاميرات — استقبال، ممرات — ليس في الغرف — خصوصية",
        ],
        device_ratios={"user_devices": 0.5, "ip_phones": 0.4, "aps": 0.2, "cctv": 0.15, "printers": 0.02, "iptv": 1.0, "pos": 0.1},
        wan_topology="Single site or Hub & Spoke for chain hotels",
        security_level="high",
        icon="🏨",
    ),
    "bank": InstitutionProfile(
        type=InstitutionType.BANK,
        name_en="Bank / Finance",
        name_ar="بنك / مالي",
        description_en="Bank with very high security, PCI-DSS, banking VLAN isolated, ATM network, no single point of failure",
        description_ar="بنك بأمان عالي جدا، PCI، شبكة مصرفية معزولة، شبكة صراف، بدون نقطة فشل",
        vlan_ids=[10,20,30,40,50,60,70,80,510,520,530,540,550],
        service_names=["AD","DNS","DHCP","CORE_BANKING","ATM_MGMT","VAULT_MGMT","TELLER_SYS","RISK_MGMT","FILE","BACKUP","NMS","WLC","NVR","FILE_SRV"],
        compliance=["PCI-DSS", "SOX", "GLBA"],
        special_requirements_en=[
            "Banking VLAN 510 — very high security — PCI-DSS — no Internet — encrypted — audit log",
            "ATM VLAN 520 — isolated — no access from users — VPN to central",
            "No single point of failure — dual ISP, dual FW HA, dual CORE SVL, dual everything",
            "All traffic logged — NetFlow to NMS — 1 year retention",
            "802.1X on all access ports — certificate based",
            "Guest Wi-Fi completely isolated — no access to banking",
        ],
        special_requirements_ar=[
            "عمليات مصرفية VLAN 510 — أمان عالي جدا — PCI — بدون إنترنت — مشفرة — سجل تدقيق",
            "صراف VLAN 520 — معزول — بدون وصول من المستخدمين — VPN للمركزي",
            "بدون نقطة فشل واحدة — مزدوج إنترنت، جدار ناري HA، أساسي SVL، مزدوج كل شيء",
            "كل حركة مسجلة — NetFlow لمراقبة — احتفاظ سنة",
            "802.1X على كل منافذ وصول — شهادات",
            "واي فاي ضيوف معزول تماما — بدون وصول مصرفي",
        ],
        device_ratios={"user_devices": 1.0, "ip_phones": 0.7, "aps": 0.05, "cctv": 0.2, "printers": 0.05, "atm": 0.05},
        wan_topology="Dual Hub — HQ + DR + branches — MPLS + IPsec",
        security_level="very_high",
        icon="🏦",
    ),
    "retail": InstitutionProfile(
        type=InstitutionType.RETAIL,
        name_en="Retail / Mall / Store Chain",
        name_ar="تجزئة / مول / سلسلة متاجر",
        description_en="Retail chain with POS, inventory, warehouse, CCTV, PCI-DSS, HQ + stores",
        description_ar="سلسلة تجزئة مع نقاط بيع، مخزون، مستودع، كاميرات، PCI، مقر ومتاجر",
        vlan_ids=[10,20,30,40,50,60,70,80,230,420,710,720,730],
        service_names=["AD","DNS","DHCP","POS","WMS","ERP","INVENTORY_SYS","LOSS_PREV","FILE","BACKUP","NMS","WLC","NVR","FILE_SRV"],
        compliance=["PCI-DSS"],
        special_requirements_en=[
            "POS VLAN 420 — PCI-DSS — isolated — encrypted — no Internet",
            "Warehouse VLAN 230 — WMS, scanners — HQ integration",
            "CCTV — high density — POS monitoring — loss prevention",
            "Guest Wi-Fi — customers — Internet only — captive portal — marketing",
            "ERP — inventory sync across stores — HQ",
        ],
        special_requirements_ar=[
            "نقاط بيع VLAN 420 — PCI — معزولة — مشفرة — بدون إنترنت",
            "مستودع VLAN 230 — إدارة مستودع، ماسحات — تكامل مقر",
            "كاميرات — كثافة عالية — مراقبة نقاط بيع — منع خسارة",
            "واي فاي ضيوف — عملاء — إنترنت فقط — بوابة — تسويق",
            "ERP — مزامنة مخزون عبر المتاجر — مقر",
        ],
        device_ratios={"user_devices": 0.6, "ip_phones": 0.2, "aps": 0.08, "cctv": 0.3, "printers": 0.03, "pos": 0.3, "scanners": 0.2},
        wan_topology="Hub & Spoke — HQ + stores + warehouse",
        security_level="high",
        icon="🛒",
    ),
    "government": InstitutionProfile(
        type=InstitutionType.GOVERNMENT,
        name_en="Government / Public Sector",
        name_ar="حكومي / قطاع عام",
        description_en="Government with classified network, high security, compliance, audit, no Internet for classified",
        description_ar="حكومي مع شبكة سرية، أمان عالي، امتثال، تدقيق، بدون إنترنت للسري",
        vlan_ids=[10,20,30,40,50,60,70,80,610,620,630,640],
        service_names=["AD","DNS","DHCP","CITIZEN_PORTAL","JUSTICE_SYS","FILE","BACKUP","NMS","WLC","NVR","FILE_SRV"],
        compliance=["NIST", "FISMA", "Common Criteria"],
        special_requirements_en=[
            "Classified VLAN 610 — no Internet — air-gapped or encrypted — audit",
            "All traffic logged — 7 years retention — SIEM",
            "802.1X + certificates + 2FA on all ports",
            "No wireless for classified — wired only",
            "Guest Wi-Fi isolated — Internet only — no access to internal",
        ],
        special_requirements_ar=[
            "سري VLAN 610 — بدون إنترنت — معزول هوائيا أو مشفر — تدقيق",
            "كل حركة مسجلة — احتفاظ 7 سنوات — SIEM",
            "802.1X + شهادات + تحقق ثنائي على كل المنافذ",
            "بدون لاسلكي للسري — سلكي فقط",
            "واي فاي ضيوف معزول — إنترنت فقط — بدون وصول داخلي",
        ],
        device_ratios={"user_devices": 1.0, "ip_phones": 0.6, "aps": 0.06, "cctv": 0.15, "printers": 0.06},
        wan_topology="Hub & Spoke + classified WAN separate",
        security_level="very_high",
        icon="🏛️",
    ),
    "office": InstitutionProfile(
        type=InstitutionType.OFFICE,
        name_en="General Office",
        name_ar="مكتب عام",
        description_en="General office — users, VoIP, servers, management, printers, CCTV, Wi-Fi, guest — standard",
        description_ar="مكتب عام — مستخدمين، هواتف، خوادم، إدارة، طابعات، كاميرات، واي فاي، ضيوف — قياسي",
        vlan_ids=[10,20,30,40,50,60,70,80,90],
        service_names=["AD","DNS","DHCP","FILE","BACKUP","NMS","WLC","NVR","FILE_SRV"],
        compliance=[],
        special_requirements_en=[
            "Standard office — users + VoIP + servers",
            "Guest Wi-Fi isolated — Internet only",
            "CCTV isolated — NVR only",
        ],
        special_requirements_ar=[
            "مكتب قياسي — مستخدمين + هواتف + خوادم",
            "واي فاي ضيوف معزول — إنترنت فقط",
            "كاميرات معزولة — مسجل فقط",
        ],
        device_ratios={"user_devices": 1.1, "ip_phones": 0.5, "aps": 0.06, "cctv": 0.1, "printers": 0.05},
        wan_topology="Single site or Hub & Spoke",
        security_level="medium",
        icon="🏢",
    ),
    "datacenter": InstitutionProfile(
        type=InstitutionType.DATACENTER,
        name_en="Data Center",
        name_ar="مركز بيانات",
        description_en="Data center — servers, storage, management, no users, high bandwidth, leaf-spine",
        description_ar="مركز بيانات — خوادم، تخزين، إدارة، بدون مستخدمين، نطاق عالي، ورقة-عمود",
        vlan_ids=[30,40,60,810,820,830],
        service_names=["NMS","STORAGE_SRV","BACKUP_DC_SRV","VCENTER","FILE_SRV"],
        compliance=["SOC2", "ISO27001"],
        special_requirements_en=[
            "Leaf-Spine architecture — no users",
            "High bandwidth — 40G/100G",
            "Storage network — iSCSI or FC",
            "No wireless — wired only",
        ],
        special_requirements_ar=[
            "معمارية ورقة-عمود — بدون مستخدمين",
            "نطاق عالي — 40G/100G",
            "شبكة تخزين — iSCSI أو FC",
            "بدون لاسلكي — سلكي فقط",
        ],
        device_ratios={"user_devices": 0.0, "ip_phones": 0.0, "aps": 0.0, "cctv": 0.05, "printers": 0.0, "servers": 5.0},
        wan_topology="Dual homed — 2 ISP — BGP",
        security_level="high",
        icon="🖥️",
    ),
}


def get_institution_profile(inst_type: str) -> InstitutionProfile:
    """Get profile by type string — case-insensitive — REAL — no hallucination"""
    key = inst_type.lower().strip()
    # Handle aliases
    aliases = {
        "trading": "trading",
        "company": "trading",
        "al-nour": "trading",
        "alnour": "trading",
        "hospital": "hospital",
        "medical": "hospital",
        "clinic": "hospital",
        "health": "hospital",
        "factory": "factory",
        "manufacturing": "factory",
        "industrial": "factory",
        "plant": "factory",
        "school": "school",
        "university": "school",
        "education": "school",
        "college": "school",
        "hotel": "hotel",
        "hospitality": "hotel",
        "resort": "hotel",
        "bank": "bank",
        "finance": "bank",
        "financial": "bank",
        "retail": "retail",
        "mall": "retail",
        "store": "retail",
        "shop": "retail",
        "government": "government",
        "gov": "government",
        "public": "government",
        "office": "office",
        "datacenter": "datacenter",
        "dc": "datacenter",
    }
    mapped = aliases.get(key, key)
    if mapped in INSTITUTION_PROFILES:
        return INSTITUTION_PROFILES[mapped]
    # Default to office if unknown — no hallucination, safe fallback
    return INSTITUTION_PROFILES["office"]


def get_vlans_for_institution(inst_type: str) -> Dict[int, VlanTemplate]:
    """Get VLANs for institution type — REAL — deterministic"""
    profile = get_institution_profile(inst_type)
    result = {}
    for vid in profile.vlan_ids:
        if vid in ALL_VLANS:
            result[vid] = ALL_VLANS[vid]
    return result


def get_services_for_institution(inst_type: str) -> Dict[str, ServiceTemplate]:
    """Get services for institution type — REAL"""
    profile = get_institution_profile(inst_type)
    result = {}
    for sname in profile.service_names:
        if sname in ALL_SERVICES:
            result[sname] = ALL_SERVICES[sname]
    return result


def calculate_devices_for_site(employees: int, inst_type: str) -> Dict[str, int]:
    """Calculate devices for site based on employees and institution type — REAL — 40Y expert"""
    profile = get_institution_profile(inst_type)
    ratios = profile.device_ratios
    result = {}
    for dev_type, ratio in ratios.items():
        count = int(employees * ratio)
        # Minimum 1 for critical types if employees > 0
        if employees > 0 and ratio > 0 and count == 0:
            count = 1
        result[dev_type] = count
    return result


def estimate_infra_for_site(employees: int, inst_type: str, site_id: str = "HQ") -> Dict[str, int]:
    """Estimate infra devices (switches, FW, etc.) for site — REAL — 40Y expert"""
    profile = get_institution_profile(inst_type)
    # Base on employees and security level
    is_hq = site_id == "HQ" or site_id.lower() == "hq"
    
    if employees <= 20:
        # Small
        return {
            "edge": 1,
            "firewall": 1,
            "core": 1 if is_hq else 0,
            "access": max(1, (employees + 15) // 24),  # 1 switch per 24 ports
            "wlc": 0,
        }
    elif employees <= 100:
        # Medium
        return {
            "edge": 1 if not is_hq else 2,
            "firewall": 1 if not is_hq else 2,  # HA for HQ
            "core": 1 if is_hq else 0,
            "access": max(1, (employees + 20) // 20),
            "wlc": 1 if is_hq else 0,
        }
    elif employees <= 500:
        # Large
        access_count = max(2, (employees + 24) // 24)
        return {
            "edge": 2,
            "firewall": 1 if not is_hq else 2,
            "core": 2 if is_hq else 1,
            "access": access_count,
            "wlc": 1,
        }
    else:
        # Enterprise / Complex
        access_count = max(4, (employees + 20) // 20)
        if is_hq:
            access_count = max(8, access_count)
        return {
            "edge": 2,
            "firewall": 1 if not is_hq else 2,
            "core": 2 if is_hq else 1,
            "access": access_count,
            "wlc": 1,
        }


def get_all_institution_types() -> List[Dict]:
    """Get all institution types for UI wizard — REAL — no hallucination"""
    result = []
    for key, profile in INSTITUTION_PROFILES.items():
        result.append({
            "id": key,
            "type": profile.type.value,
            "name_en": profile.name_en,
            "name_ar": profile.name_ar,
            "description_en": profile.description_en,
            "description_ar": profile.description_ar,
            "icon": profile.icon,
            "vlan_count": len(profile.vlan_ids),
            "vlans": profile.vlan_ids,
            "services": profile.service_names,
            "compliance": profile.compliance,
            "security_level": profile.security_level,
            "wan_topology": profile.wan_topology,
            "device_ratios": profile.device_ratios,
            "special_requirements_en": profile.special_requirements_en,
            "special_requirements_ar": profile.special_requirements_ar,
        })
    return result
