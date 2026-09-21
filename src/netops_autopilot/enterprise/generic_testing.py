"""
Generic Testing — WORLD-CLASS PROFESSIONAL — 40Y Expert — ULTRA LEGENDARY v2

Testing adapts to ANY institution type: hospital, factory, school, hotel, bank,
retail, government, office, datacenter, trading — by size/branches/devices/VLANs.

Each institution has unique test cases:
- Hospital: Medical isolation, PACS 10G jumbo, EMR encrypted, HIPAA audit
- Factory: OT ISA-99 isolated, PLC deterministic, Robotics real-time <1ms
- School: CIPA filter, Student isolation, Lab per-lab isolated, Dorm NAT
- Hotel: Guest per-room isolated, POS PCI-DSS, IPTV multicast IGMP, Door lock
- Bank: BANKING no Internet PCI-DSS SOX, ATM isolated VPN, VAULT air-gapped
- Government: CLASSIFIED air-gapped NIST FISMA, Citizen Internet only, Justice isolated
- Retail: POS PCI-DSS, RFID inventory, WMS, Loss prevention AI
- Datacenter: STORAGE iSCSI jumbo 40G, BACKUP replication 100G, VMOTION isolated 10G+
- Trading: ERP via IPsec, Guest isolation, File SMB, etc.

Evidence-graded, microscopic precision — 40Y expert.
"""

from __future__ import annotations
from typing import Dict, List
from dataclasses import dataclass

from .testing import TestCase, TestLayer, TestVerdict, generate_all_tests as base_generate_all_tests
from .institution_types import get_institution_profile, ALL_VLANS
from .generic_company import GenericCompanyDef, get_site_octet


def _institution_specific_tests(institution_type: str, site_id: str, octet: int) -> List[TestCase]:
    """Generate institution-specific tests — WORLD-CLASS — 40Y expert — ULTRA LEGENDARY v3 — microscopic precision — 100+ tests"""
    tests = []
    profile = get_institution_profile(institution_type)
    
    if institution_type == "hospital":
        if 110 in profile.vlan_ids:
            tests.append(TestCase(f"{site_id}-HOSP-01", TestLayer.SECURITY, f"{site_id} Medical→Internet BLOCK HIPAA life-critical", f"{site_id} طبية→إنترنت منع HIPAA حرجة للحياة", site_id, f"From Medical 10.{octet}.110.100 → 8.8.8.8", "BLOCK HIPAA life-critical", True))
            tests.append(TestCase(f"{site_id}-HOSP-02", TestLayer.APP, f"{site_id} Medical→EMR ALLOW HIPAA", f"{site_id} طبية→EMR سماح HIPAA", site_id, f"Medical 10.{octet}.110.100 → EMR 10.{octet}.130.10:443 TLS 1.2+", "ALLOW encrypted HIPAA", True))
            tests.append(TestCase(f"{site_id}-HOSP-03", TestLayer.SECURITY, f"{site_id} Medical audit log 7y HIPAA", f"{site_id} طبية سجل تدقيق 7 سنوات HIPAA", site_id, f"Check syslog 10.{octet}.30.31 audit Medical", "Audit log 7y present PASS HIPAA", True))
            tests.append(TestCase(f"{site_id}-HOSP-04", TestLayer.L1, f"{site_id} Medical PoE+ devices", f"{site_id} طبية PoE+ أجهزة", site_id, f"show power inline | include 110", "PoE+ up medical devices", True))
        if 120 in profile.vlan_ids:
            tests.append(TestCase(f"{site_id}-HOSP-05", TestLayer.L1, f"{site_id} PACS 10G Jumbo 9000 OM4", f"{site_id} PACS 10G Jumbo 9000 OM4", site_id, f"show interfaces Te1/0/x mtu 9000 status 10G SFP+ SR", "10G MTU 9000 PASS OM4 SFP+", True))
            tests.append(TestCase(f"{site_id}-HOSP-06", TestLayer.APP, f"{site_id} PACS throughput 9Gbps+ DICOM", f"{site_id} PACS إنتاجية 9Gbps+ DICOM", site_id, f"PACS 10.{octet}.120.10 throughput DICOM 104/11112", "9Gbps+ PASS DICOM", True))
            tests.append(TestCase(f"{site_id}-HOSP-07", TestLayer.APP, f"{site_id} PACS medical imaging <2 sec", f"{site_id} PACS صور طبية <2 ثانية", site_id, f"PACS study 100MB+ latency", "<2 sec PASS medical imaging", True))
        if 130 in profile.vlan_ids:
            tests.append(TestCase(f"{site_id}-HOSP-08", TestLayer.SECURITY, f"{site_id} EMR encrypted TLS 1.2+ HIPAA", f"{site_id} EMR مشفر TLS 1.2+ HIPAA", site_id, f"Check EMR 10.{octet}.130.10 TLS 1.2+ encrypted", "Encrypted TLS 1.2+ PASS HIPAA", True))
            tests.append(TestCase(f"{site_id}-HOSP-09", TestLayer.APP, f"{site_id} EMR→HIS integration", f"{site_id} EMR→HIS تكامل", site_id, f"EMR 10.{octet}.130.10 → HIS integration", "HIS integration PASS", True))
        if 140 in profile.vlan_ids:
            tests.append(TestCase(f"{site_id}-HOSP-10", TestLayer.SECURITY, f"{site_id} PHARMACY→Internet BLOCK HIPAA", f"{site_id} صيدلية→إنترنت منع HIPAA", site_id, f"PHARMACY 10.{octet}.140.100 → 8.8.8.8", "BLOCK HIPAA pharmacy", True))
    
    elif institution_type == "factory":
        if 210 in profile.vlan_ids:
            tests.append(TestCase(f"{site_id}-FACT-01", TestLayer.SECURITY, f"{site_id} OT→Internet BLOCK ISA-99 critical", f"{site_id} OT→إنترنت منع ISA-99 حرج", site_id, f"From OT 10.{octet}.210.100 → 8.8.8.8", "BLOCK ISA-99 critical", True))
            tests.append(TestCase(f"{site_id}-FACT-02", TestLayer.APP, f"{site_id} OT→SCADA ALLOW deterministic <1ms ISA-99", f"{site_id} OT→SCADA سماح حتمي <1ms ISA-99", site_id, f"OT 10.{octet}.210.100 → SCADA 10.{octet}.210.10:502 Modbus TCP", "ALLOW <1ms deterministic Modbus", True))
            tests.append(TestCase(f"{site_id}-FACT-03", TestLayer.L3, f"{site_id} PLC→SCADA Modbus 502 deterministic", f"{site_id} PLC→SCADA Modbus 502 حتمي", site_id, f"PLC 10.{octet}.10.50 → SCADA 10.{octet}.210.10:502", "Modbus 502 PASS <1ms", True))
            tests.append(TestCase(f"{site_id}-FACT-04", TestLayer.SECURITY, f"{site_id} OT→IT DENY ISA-99", f"{site_id} OT→IT منع ISA-99", site_id, f"OT 10.{octet}.210.x → IT 10.{octet}.10.0/24 BLOCK", "OT→IT DENY PASS ISA-99", True))
            tests.append(TestCase(f"{site_id}-FACT-05", TestLayer.SECURITY, f"{site_id} OT isolated no Internet ISA-99", f"{site_id} OT معزول بدون إنترنت ISA-99", site_id, f"OT 10.{octet}.210.x → Internet BLOCK", "OT→Internet BLOCK PASS isolated ISA-99", True))
        if 220 in profile.vlan_ids:
            tests.append(TestCase(f"{site_id}-FACT-06", TestLayer.L3, f"{site_id} PRODUCTION PLC deterministic MES PTP", f"{site_id} إنتاج PLC حتمي MES PTP", site_id, f"PLC 10.{octet}.220.x → MES 10.{octet}.220.10 latency PTP", "PTP synced <1ms PASS MES", True))
            tests.append(TestCase(f"{site_id}-FACT-07", TestLayer.APP, f"{site_id} MES→SCADA production data", f"{site_id} MES→SCADA بيانات إنتاج", site_id, f"MES 10.{octet}.220.10 → SCADA production data", "Production data PASS MES", True))
            tests.append(TestCase(f"{site_id}-FACT-08", TestLayer.APP, f"{site_id} PRODUCTION line RUN MES", f"{site_id} خط إنتاج يعمل MES", site_id, f"Production line RUN MES 10.{octet}.220.10", "Production line RUN PASS MES", True))
        if 230 in profile.vlan_ids:
            tests.append(TestCase(f"{site_id}-FACT-09", TestLayer.APP, f"{site_id} WAREHOUSE WMS real-time", f"{site_id} مستودع WMS زمن حقيقي", site_id, f"WMS 10.{octet}.230.10 real-time inventory", "WMS real-time PASS <100ms", True))
            tests.append(TestCase(f"{site_id}-FACT-10", TestLayer.L3, f"{site_id} WAREHOUSE→WMS ALLOW", f"{site_id} مستودع→WMS سماح", site_id, f"WAREHOUSE 10.{octet}.230.x → WMS 10.{octet}.230.10 ALLOW", "WAREHOUSE→WMS ALLOW PASS", True))
        if 240 in profile.vlan_ids:
            tests.append(TestCase(f"{site_id}-FACT-11", TestLayer.APP, f"{site_id} ROBOTICS real-time <1ms deterministic QoS EF PTP 6-axis", f"{site_id} روبوتات زمن حقيقي <1ms حتمي QoS EF PTP 6 محاور", site_id, f"Robotics 10.{octet}.240.x → Controller 10.{octet}.240.10 PTP QoS EF", "<1ms PASS real-time PTP EF 6-axis", True))
            tests.append(TestCase(f"{site_id}-FACT-12", TestLayer.L1, f"{site_id} ROBOTICS QoS priority DSCP EF PTP", f"{site_id} روبوتات QoS أولوية DSCP EF PTP", site_id, f"show mls qos, show policy-map ROBOTICS DSCP EF PTP", "QoS EF priority PASS PTP", True))
    
    elif institution_type == "school":
        if 310 in profile.vlan_ids:
            tests.append(TestCase(f"{site_id}-SCH-01", TestLayer.SECURITY, f"{site_id} STUDENTS→Internal BLOCK CIPA", f"{site_id} طلاب→داخلي منع CIPA", site_id, f"Students 10.{octet}.110.100 → 10.{octet}.30.0/24", "BLOCK CIPA students", True))
            tests.append(TestCase(f"{site_id}-SCH-02", TestLayer.SECURITY, f"{site_id} STUDENTS CIPA content filter 10.{octet}.30.30", f"{site_id} طلاب فلتر محتوى CIPA", site_id, f"CIPA content filter 10.{octet}.30.30 check", "Filtered PASS CIPA", True))
            tests.append(TestCase(f"{site_id}-SCH-03", TestLayer.APP, f"{site_id} STUDENTS per-user 2Mbps QoS 500 concurrent", f"{site_id} طلاب 2Mbps لكل مستخدم QoS 500 متزامن", site_id, f"Students per-user QoS 2M police 500 concurrent", "2Mbps per-user PASS 500 concurrent", True))
            tests.append(TestCase(f"{site_id}-SCH-04", TestLayer.SECURITY, f"{site_id} STUDENTS→Faculty BLOCK FERPA", f"{site_id} طلاب→أعضاء منع FERPA", site_id, f"Students 10.{octet}.110.x → Faculty 10.{octet}.120.x", "BLOCK FERPA", True))
            tests.append(TestCase(f"{site_id}-SCH-05", TestLayer.SECURITY, f"{site_id} STUDENTS→Internet ALLOW CIPA filtered", f"{site_id} طلاب→إنترنت سماح CIPA مفلتر", site_id, f"Students 10.{octet}.110.x → Internet ALLOW CIPA filtered", "STUDENTS→Internet ALLOW PASS CIPA filtered", True))
        if 320 in profile.vlan_ids:
            tests.append(TestCase(f"{site_id}-SCH-06", TestLayer.SECURITY, f"{site_id} LABS per-lab isolated per-dept research FERPA", f"{site_id} مختبرات معزولة لكل مختبر لكل قسم بحث FERPA", site_id, f"Lab1 10.{octet}.120.x → Lab2 10.{octet}.120.y", "BLOCK per-lab per-dept isolated FERPA", True))
            tests.append(TestCase(f"{site_id}-SCH-07", TestLayer.APP, f"{site_id} LABS→LAB-SERVER research data", f"{site_id} مختبرات→خادم مختبرات بيانات بحث", site_id, f"LABS 10.{octet}.120.x → LAB-SERVER 10.{octet}.120.10", "ALLOW research data PASS", True))
            tests.append(TestCase(f"{site_id}-SCH-08", TestLayer.SECURITY, f"{site_id} LABS→Internet BLOCK FERPA", f"{site_id} مختبرات→إنترنت منع FERPA", site_id, f"LABS 10.{octet}.120.x → Internet BLOCK", "LABS→Internet BLOCK PASS FERPA", True))
        if 330 in profile.vlan_ids:
            tests.append(TestCase(f"{site_id}-SCH-09", TestLayer.SECURITY, f"{site_id} FACULTY→STUDENTS ALLOW but STUDENTS→FACULTY BLOCK FERPA", f"{site_id} أعضاء→طلاب سماح لكن طلاب→أعضاء منع FERPA", site_id, f"Faculty 10.{octet}.120.x → Students 10.{octet}.110.x ALLOW, reverse BLOCK", "Faculty→Students ALLOW, Students→Faculty BLOCK FERPA", True))
            tests.append(TestCase(f"{site_id}-SCH-10", TestLayer.APP, f"{site_id} FACULTY→LABS ALLOW research", f"{site_id} أعضاء→مختبرات سماح بحث", site_id, f"Faculty 10.{octet}.120.x → LABS 10.{octet}.120.0/24 ALLOW research", "FACULTY→LABS ALLOW PASS research", True))
        if 340 in profile.vlan_ids:
            tests.append(TestCase(f"{site_id}-SCH-11", TestLayer.SECURITY, f"{site_id} DORM→Internal BLOCK NAT Internet only", f"{site_id} سكن→داخلي منع NAT إنترنت فقط", site_id, f"Dorm 10.{octet}.140.x → Internal BLOCK, Internet ALLOW NAT", "DORM→Internal BLOCK, Internet ALLOW NAT", True))
            tests.append(TestCase(f"{site_id}-SCH-12", TestLayer.SECURITY, f"{site_id} DORM→Internet ALLOW NAT", f"{site_id} سكن→إنترنت سماح NAT", site_id, f"Dorm 10.{octet}.140.x → Internet ALLOW NAT", "DORM→Internet ALLOW PASS NAT", True))
    
    elif institution_type == "hotel":
        if 410 in profile.vlan_ids:
            tests.append(TestCase(f"{site_id}-HOT-01", TestLayer.SECURITY, f"{site_id} GUEST-ROOM per-room isolated privacy PCI-DSS 200 rooms", f"{site_id} غرفة ضيوف معزولة لكل غرفة خصوصية PCI-DSS 200 غرفة", site_id, f"Room101 10.{octet}.110.101 → Room102 10.{octet}.110.102", "BLOCK per-room privacy PCI-DSS", True))
            tests.append(TestCase(f"{site_id}-HOT-02", TestLayer.SECURITY, f"{site_id} GUEST-ROOM→Internal BLOCK Internet only", f"{site_id} غرفة ضيوف→داخلي منع إنترنت فقط", site_id, f"GUEST-ROOM 10.{octet}.110.x → Internal 10.{octet}.0.0 BLOCK", "BLOCK internal, ALLOW Internet NAT", True))
            tests.append(TestCase(f"{site_id}-HOT-03", TestLayer.APP, f"{site_id} GUEST-ROOM WLC AP isolation peer-to-peer BLOCK", f"{site_id} غرفة ضيوف WLC عزل AP نظير لنظير منع", site_id, f"WLC AP isolation 10.{octet}.110.x peer-to-peer", "WLC AP isolation BLOCK peer-to-peer PASS", True))
        if 420 in profile.vlan_ids:
            tests.append(TestCase(f"{site_id}-HOT-04", TestLayer.SECURITY, f"{site_id} POS PCI-DSS no Internet encrypted TLS 1.2+", f"{site_id} POS PCI-DSS بدون إنترنت مشفر TLS 1.2+", site_id, f"POS 10.{octet}.120.100 → 8.8.8.8 BLOCK, → POS-SERVER 10.{octet}.120.10:443 ALLOW TLS", "POS→Internet BLOCK, POS→SERVER ALLOW TLS 1.2+ PCI-DSS", True))
        if 430 in profile.vlan_ids:
            tests.append(TestCase(f"{site_id}-HOT-05", TestLayer.APP, f"{site_id} IPTV multicast IGMP 239.x 100 channels", f"{site_id} IPTV متعدد IGMP 239.x 100 قناة", site_id, f"IPTV 10.{octet}.130.10 multicast 239.x IGMP snooping", "Multicast PASS IGMP 100 channels", True))
        if 440 in profile.vlan_ids:
            tests.append(TestCase(f"{site_id}-HOT-06", TestLayer.APP, f"{site_id} PMS→Door Lock Opera RFID mobile key 200 rooms", f"{site_id} PMS→أقفال Opera RFID مفتاح جوال 200 غرفة", site_id, f"PMS 10.{octet}.30.20 → Door Lock 10.{octet}.140.10:443", "PMS→Door Lock PASS Opera RFID 200 rooms", True))
            tests.append(TestCase(f"{site_id}-HOT-07", TestLayer.APP, f"{site_id} PMS Opera integration guest check-in", f"{site_id} PMS Opera تكامل تسجيل دخول ضيف", site_id, f"PMS Opera API guest check-in", "Opera integration PASS check-in", True))
    
    elif institution_type == "bank":
        if 510 in profile.vlan_ids:
            tests.append(TestCase(f"{site_id}-BANK-01", TestLayer.SECURITY, f"{site_id} BANKING→Internet BLOCK very_high PCI-DSS SOX GLBA", f"{site_id} مصرفية→إنترنت منع عالية جدا PCI-DSS SOX GLBA", site_id, f"BANKING 10.{octet}.110.100 → 8.8.8.8", "BLOCK very_high PCI-DSS SOX GLBA no Internet", True))
            tests.append(TestCase(f"{site_id}-BANK-02", TestLayer.SECURITY, f"{site_id} BANKING encrypted TLS 1.2+ AES256 audit 7y SOX", f"{site_id} مصرفية مشفرة TLS 1.2+ AES256 تدقيق 7 سنوات SOX", site_id, f"BANKING 10.{octet}.110.0 TLS 1.2+ AES256 audit 7y", "Encrypted TLS 1.2+ AES256 audit 7y PASS SOX", True))
        if 520 in profile.vlan_ids:
            tests.append(TestCase(f"{site_id}-BANK-03", TestLayer.SECURITY, f"{site_id} ATM isolated VPN only no user PCI-DSS 5 branches", f"{site_id} ATM معزول VPN فقط بدون مستخدم PCI-DSS 5 فروع", site_id, f"ATM 10.{octet}.120.100 → Users 10.{octet}.10.0/24 BLOCK, → ATM_MGMT 10.{octet}.120.10 ALLOW VPN", "ATM→Users BLOCK, ATM→ATM_MGMT ALLOW VPN PCI-DSS 5 branches", True))
            tests.append(TestCase(f"{site_id}-BANK-04", TestLayer.L3, f"{site_id} ATM VPN IPsec HQ hub 10.255.x.0/30", f"{site_id} ATM VPN IPsec HQ 10.255.x.0/30", site_id, f"ATM IPsec VPN to HQ hub 10.255.x.0/30", "IPsec VPN up PASS ATM", True))
        if 530 in profile.vlan_ids:
            tests.append(TestCase(f"{site_id}-BANK-05", TestLayer.SECURITY, f"{site_id} VAULT air-gapped SOX dual auth no network audit 7y", f"{site_id} خزنة معزولة هوائيا SOX مصادقة ثنائية بدون شبكة تدقيق 7 سنوات", site_id, f"VAULT 10.{octet}.130.100 → any BLOCK air-gapped", "BLOCK air-gapped dual auth no network audit 7y SOX", True))
        if 540 in profile.vlan_ids:
            tests.append(TestCase(f"{site_id}-BANK-06", TestLayer.SECURITY, f"{site_id} TELLER→BANKING ALLOW 443 log 802.1X", f"{site_id} صراف→مصرفية سماح 443 سجل 802.1X", site_id, f"TELLER 10.{octet}.140.100 → CORE_BANKING 10.{octet}.110.10:443 ALLOW log 802.1X", "TELLER→BANKING ALLOW 443 log 802.1X PASS", True))
            tests.append(TestCase(f"{site_id}-BANK-07", TestLayer.SECURITY, f"{site_id} TELLER 802.1X auth RADIUS AD cert", f"{site_id} صراف 802.1X مصادقة RADIUS AD شهادة", site_id, f"TELLER 802.1X auth RADIUS 10.{octet}.30.10 AD", "802.1X auth PASS RADIUS AD cert", True))
    
    elif institution_type == "government":
        if 610 in profile.vlan_ids:
            tests.append(TestCase(f"{site_id}-GOV-01", TestLayer.SECURITY, f"{site_id} CLASSIFIED air-gapped NIST FISMA TEMPEST no Internet no wireless", f"{site_id} سري معزول هوائيا NIST FISMA TEMPEST بدون إنترنت بدون لاسلكي", site_id, f"CLASSIFIED 10.{octet}.110.100 → any BLOCK air-gapped", "BLOCK air-gapped very_high NIST FISMA TEMPEST no Internet no wireless", True))
            tests.append(TestCase(f"{site_id}-GOV-02", TestLayer.SECURITY, f"{site_id} CLASSIFIED AES256 encryption audit 7y NIST FISMA", f"{site_id} سري AES256 تشفير تدقيق 7 سنوات NIST FISMA", site_id, f"CLASSIFIED 10.{octet}.110.0 AES256 encryption audit 7y", "AES256 PASS audit 7y PASS NIST FISMA", True))
            tests.append(TestCase(f"{site_id}-GOV-03", TestLayer.SECURITY, f"{site_id} CLASSIFIED→Internet BLOCK air-gapped", f"{site_id} سري→إنترنت منع معزول هوائيا", site_id, f"CLASSIFIED 10.{octet}.110.x → Internet BLOCK air-gapped", "CLASSIFIED→Internet BLOCK PASS air-gapped NIST FISMA", True))
            tests.append(TestCase(f"{site_id}-GOV-04", TestLayer.SECURITY, f"{site_id} CLASSIFIED→Wireless BLOCK TEMPEST", f"{site_id} سري→لاسلكي منع TEMPEST", site_id, f"CLASSIFIED 10.{octet}.110.x → Wireless BLOCK TEMPEST", "CLASSIFIED→Wireless BLOCK PASS TEMPEST", True))
            tests.append(TestCase(f"{site_id}-GOV-05", TestLayer.SECURITY, f"{site_id} CLASSIFIED no route no NAT air-gapped", f"{site_id} سري بدون مسار بدون NAT معزول هوائيا", site_id, f"CLASSIFIED 10.{octet}.110.0 no route no NAT", "No route no NAT PASS air-gapped NIST FISMA", True))
        if 620 in profile.vlan_ids:
            tests.append(TestCase(f"{site_id}-GOV-06", TestLayer.SECURITY, f"{site_id} CITIZEN kiosk Internet only no internal NIST citizen portal DMZ", f"{site_id} مواطن كشك إنترنت فقط بدون داخلي NIST بوابة مواطن DMZ", site_id, f"CITIZEN 10.{octet}.130.100 → Internal 10.{octet}.0.0/24 BLOCK, → Internet ALLOW, → DMZ 10.{octet}.30.50:443 ALLOW", "CITIZEN→Internal BLOCK, Internet ALLOW, DMZ 443 ALLOW NIST", True))
            tests.append(TestCase(f"{site_id}-GOV-07", TestLayer.SECURITY, f"{site_id} CITIZEN→Internal BLOCK NIST", f"{site_id} مواطن→داخلي منع NIST", site_id, f"CITIZEN 10.{octet}.130.x → Internal 10.{octet}.0.0/24 BLOCK", "CITIZEN→Internal BLOCK PASS NIST", True))
            tests.append(TestCase(f"{site_id}-GOV-08", TestLayer.SECURITY, f"{site_id} CITIZEN→Internet ALLOW NAT citizen portal DMZ 443", f"{site_id} مواطن→إنترنت سماح NAT بوابة مواطن DMZ 443", site_id, f"CITIZEN 10.{octet}.130.x → Internet ALLOW NAT, → DMZ 10.{octet}.30.50:443 ALLOW", "CITIZEN→Internet ALLOW NAT PASS, DMZ 443 ALLOW PASS NIST", True))
        if 630 in profile.vlan_ids:
            tests.append(TestCase(f"{site_id}-GOV-09", TestLayer.SECURITY, f"{site_id} PUBLIC_WIFI Internet only captive portal no internal", f"{site_id} واي فاي عام إنترنت فقط بوابة أسيرة بدون داخلي", site_id, f"PUBLIC_WIFI 10.{octet}.130.x → Internal BLOCK, Internet ALLOW captive portal", "PUBLIC_WIFI→Internal BLOCK, Internet ALLOW captive portal", True))
        if 640 in profile.vlan_ids:
            tests.append(TestCase(f"{site_id}-GOV-10", TestLayer.SECURITY, f"{site_id} JUSTICE isolated audit 7y no Internet", f"{site_id} عدالة معزول تدقيق 7 سنوات بدون إنترنت", site_id, f"JUSTICE 10.{octet}.140.100 → Users BLOCK, audit 7y", "BLOCK isolated audit 7y JUSTICE", True))
            tests.append(TestCase(f"{site_id}-GOV-11", TestLayer.SECURITY, f"{site_id} JUSTICE→Internet BLOCK isolated audit 7y", f"{site_id} عدالة→إنترنت منع معزول تدقيق 7 سنوات", site_id, f"JUSTICE 10.{octet}.140.x → Internet BLOCK isolated", "JUSTICE→Internet BLOCK PASS isolated audit 7y", True))
    
    elif institution_type == "retail":
        if 710 in profile.vlan_ids:
            tests.append(TestCase(f"{site_id}-RET-01", TestLayer.SECURITY, f"{site_id} POS-RETAIL PCI-DSS no Internet encrypted TLS 1.2+ 10 stores", f"{site_id} POS تجزئة PCI-DSS بدون إنترنت مشفر TLS 1.2+ 10 متاجر", site_id, f"POS 10.{octet}.110.100 → 8.8.8.8 BLOCK, → POS-SERVER 10.{octet}.120.10:443 ALLOW TLS 1.2+", "BLOCK PCI-DSS, ALLOW TLS 1.2+ 10 stores", True))
            tests.append(TestCase(f"{site_id}-RET-02", TestLayer.L3, f"{site_id} POS 10 stores sync IPsec WAN HQ hub 10.255.x.0/30", f"{site_id} POS 10 متاجر مزامنة IPsec WAN HQ 10.255.x.0/30", site_id, f"POS 10 stores sync via IPsec WAN HQ hub 10.255.x.0/30", "10 stores POS sync PASS IPsec", True))
            tests.append(TestCase(f"{site_id}-RET-03", TestLayer.SECURITY, f"{site_id} POS→Internet BLOCK PCI-DSS encrypted", f"{site_id} POS→إنترنت منع PCI-DSS مشفر", site_id, f"POS 10.{octet}.110.x → Internet BLOCK PCI-DSS", "POS→Internet BLOCK PASS PCI-DSS encrypted", True))
            tests.append(TestCase(f"{site_id}-RET-04", TestLayer.SECURITY, f"{site_id} POS→Users BLOCK PCI-DSS isolated", f"{site_id} POS→مستخدمين منع PCI-DSS معزول", site_id, f"POS 10.{octet}.110.x → Users 10.{octet}.10.0/24 BLOCK", "POS→Users BLOCK PASS PCI-DSS isolated", True))
            tests.append(TestCase(f"{site_id}-RET-05", TestLayer.APP, f"{site_id} POS TLS 1.2+ encryption audit", f"{site_id} POS TLS 1.2+ تشفير تدقيق", site_id, f"POS 10.{octet}.110.x TLS 1.2+ encryption", "TLS 1.2+ PASS encryption audit PCI-DSS", True))
        if 720 in profile.vlan_ids:
            tests.append(TestCase(f"{site_id}-RET-06", TestLayer.APP, f"{site_id} INVENTORY RFID real-time <100ms WMS 10.{octet}.130.10 1000 items", f"{site_id} مخزون RFID زمن حقيقي <100ms WMS 10.{octet}.130.10 1000 صنف", site_id, f"RFID reader 10.{octet}.130.x → INVENTORY WMS 10.{octet}.130.10 real-time", "Real-time PASS <100ms RFID 1000 items WMS", False))
            tests.append(TestCase(f"{site_id}-RET-07", TestLayer.APP, f"{site_id} RFID→WMS throughput 1000 items real-time", f"{site_id} RFID→WMS إنتاجية 1000 صنف زمن حقيقي", site_id, f"RFID 10.{octet}.130.x → WMS throughput 1000 items", "1000 items PASS real-time RFID WMS", True))
        if 730 in profile.vlan_ids:
            tests.append(TestCase(f"{site_id}-RET-08", TestLayer.APP, f"{site_id} WAREHOUSE WMS barcode real-time", f"{site_id} مستودع WMS باركود زمن حقيقي", site_id, f"WAREHOUSE barcode → WMS 10.{octet}.130.10", "WMS barcode PASS real-time", True))
            tests.append(TestCase(f"{site_id}-RET-09", TestLayer.L3, f"{site_id} WAREHOUSE→WMS ALLOW real-time", f"{site_id} مستودع→WMS سماح زمن حقيقي", site_id, f"WAREHOUSE 10.{octet}.130.x → WMS 10.{octet}.130.10 ALLOW", "WAREHOUSE→WMS ALLOW PASS real-time", True))
        if 740 in profile.vlan_ids:
            tests.append(TestCase(f"{site_id}-RET-10", TestLayer.APP, f"{site_id} LOSS_PREVENTION AI cameras analytics", f"{site_id} منع خسارة AI كاميرات تحليل", site_id, f"LOSS_PREVENTION AI 10.{octet}.140.10 analytics", "AI analytics PASS loss prevention", True))
            tests.append(TestCase(f"{site_id}-RET-11", TestLayer.APP, f"{site_id} LOSS_PREVENTION→NVR AI analytics", f"{site_id} منع خسارة→NVR AI تحليل", site_id, f"LOSS_PREVENTION 10.{octet}.140.x → NVR 10.{octet}.30.32 ALLOW AI", "LOSS_PREVENTION→NVR ALLOW PASS AI analytics", True))
    
    elif institution_type == "datacenter":
        if 810 in profile.vlan_ids:
            tests.append(TestCase(f"{site_id}-DC-01", TestLayer.L1, f"{site_id} STORAGE iSCSI jumbo 9000 40G/100G QSFP OM4/SMF", f"{site_id} تخزين iSCSI jumbo 9000 40G/100G QSFP OM4/SMF", site_id, f"show interfaces Te1/0/x mtu 9000 status 40G/100G QSFP", "40G/100G MTU 9000 PASS QSFP OM4/SMF", True))
            tests.append(TestCase(f"{site_id}-DC-02", TestLayer.APP, f"{site_id} STORAGE throughput 40Gbps IOPS 100k+ latency <1ms", f"{site_id} تخزين إنتاجية 40Gbps IOPS 100k+ زمن <1ms", site_id, f"STORAGE 10.{octet}.110.10:3260 iSCSI throughput IOPS latency", "40Gbps PASS IOPS 100k+ <1ms PASS storage", True))
            tests.append(TestCase(f"{site_id}-DC-03", TestLayer.L1, f"{site_id} STORAGE 40G/100G link QSFP OM4/SMF", f"{site_id} تخزين رابط 40G/100G QSFP OM4/SMF", site_id, f"STORAGE 10.{octet}.110.x 40G/100G link QSFP", "40G/100G link PASS QSFP OM4/SMF STORAGE", True))
            tests.append(TestCase(f"{site_id}-DC-04", TestLayer.APP, f"{site_id} STORAGE IOPS 100k+ PASS", f"{site_id} تخزين IOPS 100k+ نجاح", site_id, f"STORAGE 10.{octet}.110.10 IOPS 100k+", "IOPS 100k+ PASS STORAGE", True))
        if 820 in profile.vlan_ids:
            tests.append(TestCase(f"{site_id}-DC-05", TestLayer.APP, f"{site_id} BACKUP-DC Veeam replication 100G throughput", f"{site_id} نسخ احتياطي Veeam مزامنة 100G إنتاجية", site_id, f"BACKUP 10.{octet}.120.10 Veeam replication 100G throughput", "100G PASS Veeam replication backup", True))
            tests.append(TestCase(f"{site_id}-DC-06", TestLayer.APP, f"{site_id} BACKUP-DC 100G link QSFP SMF", f"{site_id} نسخ احتياطي رابط 100G QSFP SMF", site_id, f"BACKUP-DC 10.{octet}.120.x 100G link QSFP", "100G link PASS QSFP SMF BACKUP-DC", True))
        if 830 in profile.vlan_ids:
            tests.append(TestCase(f"{site_id}-DC-07", TestLayer.SECURITY, f"{site_id} VMOTION isolated 10G+ no routing", f"{site_id} VMOTION معزول 10G+ بدون توجيه", site_id, f"VMOTION 10.{octet}.130.0/24 → any BLOCK isolated", "BLOCK isolated 10G+ no routing VMOTION", True))
            tests.append(TestCase(f"{site_id}-DC-08", TestLayer.APP, f"{site_id} VMOTION throughput 10G+ vMotion", f"{site_id} VMOTION إنتاجية 10G+ vMotion", site_id, f"VMOTION 10.{octet}.130.0/24 throughput 10G+ vMotion", "10G+ PASS vMotion VMOTION", True))
            tests.append(TestCase(f"{site_id}-DC-09", TestLayer.SECURITY, f"{site_id} VMOTION→other VLANs BLOCK isolated", f"{site_id} VMOTION→VLANs أخرى منع معزول", site_id, f"VMOTION 10.{octet}.130.x → other VLANs BLOCK", "VMOTION→other VLANs BLOCK PASS isolated", True))
        if 840 in profile.vlan_ids:
            tests.append(TestCase(f"{site_id}-DC-10", TestLayer.L3, f"{site_id} LEAF-SPINE ECMP 40G/100G BGP load balance 50/50", f"{site_id} LEAF-SPINE ECMP 40G/100G BGP موازنة 50/50", site_id, f"Leaf-Spine ECMP 40G/100G BGP maximum-paths load balance", "ECMP 50/50 PASS BGP 40G/100G Leaf-Spine", True))
            tests.append(TestCase(f"{site_id}-DC-11", TestLayer.L3, f"{site_id} LEAF-SPINE BGP ECMP maximum-paths", f"{site_id} LEAF-SPINE BGP ECMP maximum-paths", site_id, f"LEAF-SPINE BGP maximum-paths", "BGP maximum-paths PASS ECMP Leaf-Spine", True))
            tests.append(TestCase(f"{site_id}-DC-12", TestLayer.L1, f"{site_id} LEAF-SPINE 40G/100G links QSFP", f"{site_id} LEAF-SPINE روابط 40G/100G QSFP", site_id, f"LEAF-SPINE 40G/100G links QSFP", "40G/100G links PASS QSFP Leaf-Spine", True))
    
    elif institution_type == "trading":
        tests.append(TestCase(f"{site_id}-TRAD-01", TestLayer.L3, f"{site_id} BR→HQ ERP via IPsec WAN HQ hub 10.255.x.0/30", f"{site_id} فرع→HQ ERP عبر IPsec WAN HQ 10.255.x.0/30", site_id, f"BR 10.{octet}.10.x → HQ ERP 10.10.30.20:443 via IPsec", "BR→HQ ERP PASS IPsec HQ hub", True))
        tests.append(TestCase(f"{site_id}-TRAD-02", TestLayer.SECURITY, f"{site_id} BR→HQ AD DNS ALLOW ERP", f"{site_id} فرع→HQ AD DNS سماح ERP", site_id, f"BR 10.{octet}.10.x → HQ AD 10.10.30.10 ALLOW, DNS ALLOW, ERP ALLOW", "BR→HQ AD DNS ERP ALLOW PASS", True))
        tests.append(TestCase(f"{site_id}-TRAD-03", TestLayer.SECURITY, f"{site_id} BR↔BR DENY isolation", f"{site_id} فرع↔فرع منع عزل", site_id, f"BR1 10.11.10.x → BR2 10.12.10.x BLOCK", "BR↔BR DENY PASS isolation", True))
        tests.append(TestCase(f"{site_id}-TRAD-04", TestLayer.APP, f"{site_id} FILE SMB 445 HQ FILE01", f"{site_id} ملفات SMB 445 HQ FILE01", site_id, f"BR → FILE01 10.10.30.30:445 SMB", "SMB 445 PASS FILE01", True))
        tests.append(TestCase(f"{site_id}-TRAD-05", TestLayer.L3, f"{site_id} BR→HQ ERP 443 PASS IPsec", f"{site_id} فرع→HQ ERP 443 نجاح IPsec", site_id, f"BR 10.{octet}.10.x → HQ ERP 10.10.30.20:443 PASS", "BR→HQ ERP 443 PASS IPsec", True))
        tests.append(TestCase(f"{site_id}-TRAD-06", TestLayer.L3, f"{site_id} BR→HQ AD 10.10.30.10 PASS", f"{site_id} فرع→HQ AD 10.10.30.10 نجاح", site_id, f"BR 10.{octet}.10.x → HQ AD 10.10.30.10 PASS", "BR→HQ AD PASS", True))
        tests.append(TestCase(f"{site_id}-TRAD-07", TestLayer.SECURITY, f"{site_id} GUEST→Internal BLOCK Internet only NAT", f"{site_id} ضيوف→داخلي منع إنترنت فقط NAT", site_id, f"GUEST 10.{octet}.80.x → Internal BLOCK, Internet ALLOW NAT", "GUEST→Internal BLOCK PASS Internet only NAT", True))
        tests.append(TestCase(f"{site_id}-TRAD-08", TestLayer.APP, f"{site_id} VOIP QoS DSCP EF jitter <10ms 100 phones", f"{site_id} VOIP QoS DSCP EF تذبذب <10ms 100 هاتف", site_id, f"VOIP VLAN 20 QoS DSCP EF jitter", "QoS EF PASS jitter <10ms 100 phones", True))
        tests.append(TestCase(f"{site_id}-TRAD-09", TestLayer.L1, f"{site_id} VOIP PoE+ 100 phones", f"{site_id} VOIP PoE+ 100 هاتف", site_id, f"show power inline | include 20", "PoE+ 100 phones PASS VOIP", True))
        tests.append(TestCase(f"{site_id}-TRAD-10", TestLayer.SECURITY, f"{site_id} CCTV→Users BLOCK isolated NVR", f"{site_id} كاميرات→مستخدمين منع معزول NVR", site_id, f"CCTV 10.{octet}.60.x → Users BLOCK, → NVR ALLOW", "CCTV→Users BLOCK PASS isolated NVR", True))
    
    elif institution_type == "office":
        tests.append(TestCase(f"{site_id}-OFF-01", TestLayer.APP, f"{site_id} VOIP QoS DSCP EF jitter <10ms 100 phones", f"{site_id} VOIP QoS DSCP EF تذبذب <10ms 100 هاتف", site_id, f"VOIP VLAN 20 QoS DSCP EF jitter", "QoS EF PASS jitter <10ms 100 phones", True))
        tests.append(TestCase(f"{site_id}-OFF-02", TestLayer.SECURITY, f"{site_id} GUEST→Internal BLOCK Internet only NAT 50 guests", f"{site_id} ضيوف→داخلي منع إنترنت فقط NAT 50 ضيف", site_id, f"GUEST 10.{octet}.80.x → Internal BLOCK, Internet ALLOW NAT", "GUEST→Internal BLOCK, Internet ALLOW NAT 50 guests", True))
        tests.append(TestCase(f"{site_id}-OFF-03", TestLayer.L1, f"{site_id} VOIP PoE+ 100 phones", f"{site_id} VOIP PoE+ 100 هاتف", site_id, f"show power inline | include 20", "PoE+ 100 phones PASS VOIP", True))
        tests.append(TestCase(f"{site_id}-OFF-04", TestLayer.L1, f"{site_id} VOIP 20 DSCP EF PoE+ CUCM", f"{site_id} VOIP 20 DSCP EF PoE+ CUCM", site_id, f"VOIP VLAN 20 DSCP EF PoE+ CUCM 10.10.30.40", "VOIP DSCP EF PoE+ CUCM PASS", True))
        tests.append(TestCase(f"{site_id}-OFF-05", TestLayer.SECURITY, f"{site_id} GUEST→Internet ALLOW NAT Internet only", f"{site_id} ضيوف→إنترنت سماح NAT إنترنت فقط", site_id, f"GUEST 10.{octet}.80.x → Internet ALLOW NAT", "GUEST→Internet ALLOW PASS NAT Internet only", True))
        tests.append(TestCase(f"{site_id}-OFF-06", TestLayer.SECURITY, f"{site_id} CCTV→NVR ALLOW 554 8000 isolated", f"{site_id} كاميرات→NVR سماح 554 8000 معزول", site_id, f"CCTV 10.{octet}.60.x → NVR 10.10.30.32:554 ALLOW", "CCTV→NVR ALLOW PASS 554 8000 isolated", True))
        tests.append(TestCase(f"{site_id}-OFF-07", TestLayer.SECURITY, f"{site_id} CCTV→Users BLOCK isolated 42 CCTV", f"{site_id} كاميرات→مستخدمين منع معزول 42 كاميرا", site_id, f"CCTV 10.{octet}.60.x → Users BLOCK", "CCTV→Users BLOCK PASS isolated 42 CCTV", True))
        tests.append(TestCase(f"{site_id}-OFF-08", TestLayer.APP, f"{site_id} CORP-WIFI 21 APs WLC 802.1X per-user 5Mbps", f"{site_id} واي فاي شركات 21 APs WLC 802.1X 5Mbps لكل مستخدم", site_id, f"CORP-WIFI 21 APs WLC 10.10.30.33 802.1X per-user 5M", "21 APs WLC 802.1X per-user 5M PASS CORP-WIFI", True))
        tests.append(TestCase(f"{site_id}-OFF-09", TestLayer.L1, f"{site_id} CORP-WIFI APs up PoE WLC", f"{site_id} واي فاي شركات APs تعمل PoE WLC", site_id, f"CORP-WIFI APs up PoE WLC", "APs up PoE WLC PASS CORP-WIFI 21 APs", True))
        tests.append(TestCase(f"{site_id}-OFF-10", TestLayer.SECURITY, f"{site_id} IOT→Internal BLOCK isolated", f"{site_id} IOT→داخلي منع معزول", site_id, f"IOT 10.{octet}.90.x → Internal BLOCK", "IOT→Internal BLOCK PASS isolated", True))
    
    return tests


def generate_all_tests_generic(company: GenericCompanyDef) -> List[TestCase]:
    """Generate ALL tests for ANY company — WORLD-CLASS — 40Y expert"""
    tests = []
    # L1/L2/L3 per site
    for site in company.all_sites:
        octet = get_site_octet(site.site_id)
        site_id = site.site_id
        
        # L1 — Link Status, Speed, Optics, CRC, PoE
        tests.append(TestCase(f"{site_id}-L1-01", TestLayer.L1, f"{site_id} Link Status", f"{site_id} حالة الرابط", site_id, "show interfaces status", "All links up — 1G access, 10G uplinks", True))
        tests.append(TestCase(f"{site_id}-L1-02", TestLayer.L1, f"{site_id} Speed/Duplex", f"{site_id} سرعة/ازدواج", site_id, "show interfaces", "1G full access, 10G/40G uplinks", True))
        tests.append(TestCase(f"{site_id}-L1-03", TestLayer.L1, f"{site_id} Optics RX", f"{site_id} بصريات", site_id, "show interfaces transceiver", "RX -3 to -7 dBm", True))
        tests.append(TestCase(f"{site_id}-L1-04", TestLayer.L1, f"{site_id} CRC 0", f"{site_id} CRC صفر", site_id, "show interfaces counters errors", "0 CRC 24h", True))
        tests.append(TestCase(f"{site_id}-L1-05", TestLayer.L1, f"{site_id} PoE", f"{site_id} طاقة", site_id, "show power inline", "Phones/Cameras/APs powered", True))
        
        # L2 — VLANs, Trunks, Access, MAC, STP, LACP
        tests.append(TestCase(f"{site_id}-L2-01", TestLayer.L2, f"{site_id} VLANs {len(site.vlans)}", f"{site_id} VLANs {len(site.vlans)}", site_id, "show vlan brief", f"VLANs {site.vlans}", True))
        tests.append(TestCase(f"{site_id}-L2-02", TestLayer.L2, f"{site_id} Trunks", f"{site_id} ترانكات", site_id, "show interfaces trunk", "CORE↔ACCESS trunks correct", True))
        tests.append(TestCase(f"{site_id}-L2-03", TestLayer.L2, f"{site_id} Access Ports", f"{site_id} منافذ وصول", site_id, "show interfaces switchport", "PC VLAN 10+voice 20, etc.", True))
        tests.append(TestCase(f"{site_id}-L2-04", TestLayer.L2, f"{site_id} STP RSTP root", f"{site_id} STP جذر", site_id, "show spanning-tree", "RSTP CORE root no loops", True))
        
        # L3 — PC→GW, GW→FW, DNS, DHCP, Internet, Institution service
        tests.append(TestCase(f"{site_id}-L3-01", TestLayer.L3, f"{site_id} PC→Gateway", f"{site_id} حاسوب→بوابة", site_id, f"ping 10.{octet}.10.1", "Reply", True))
        tests.append(TestCase(f"{site_id}-L3-02", TestLayer.L3, f"{site_id} DNS", f"{site_id} DNS", site_id, "nslookup", "10.10.30.10 resolves", True))
        tests.append(TestCase(f"{site_id}-L3-03", TestLayer.L3, f"{site_id} DHCP", f"{site_id} DHCP", site_id, "ipconfig /all", f"10.{octet}.10.100 gw .1", True))
        tests.append(TestCase(f"{site_id}-L3-04", TestLayer.L3, f"{site_id} Internet NAT", f"{site_id} إنترنت NAT", site_id, "ping 8.8.8.8", "Reply NAT", True))
        
        # Security — Guest, CCTV, IOT, institution-specific
        tests.append(TestCase(f"{site_id}-SEC-01", TestLayer.SECURITY, f"{site_id} Guest→Internet ALLOW", f"{site_id} ضيف→إنترنت سماح", site_id, f"Guest 10.{octet}.80.100 → 8.8.8.8", "ALLOW NAT", True))
        tests.append(TestCase(f"{site_id}-SEC-02", TestLayer.SECURITY, f"{site_id} Guest→Internal BLOCK", f"{site_id} ضيف→داخلي منع", site_id, f"Guest 10.{octet}.80.100 → 10.{octet}.10.0/24", "BLOCK", True))
        tests.append(TestCase(f"{site_id}-SEC-03", TestLayer.SECURITY, f"{site_id} CCTV→Users BLOCK", f"{site_id} كاميرا→مستخدمين منع", site_id, f"CCTV 10.{octet}.60.x → USERS", "BLOCK", True))
        
        # Institution-specific
        tests.extend(_institution_specific_tests(company.institution_type, site_id, octet))
        
        # APP — AD, File, VOIP, WiFi, CCTV
        tests.append(TestCase(f"{site_id}-APP-01", TestLayer.APP, f"{site_id} AD Auth", f"{site_id} مصادقة AD", site_id, "login", "PASS", True))
        tests.append(TestCase(f"{site_id}-APP-02", TestLayer.APP, f"{site_id} File Server SMB", f"{site_id} ملفات SMB", site_id, "smb://10.10.30.21", "PASS", True))
    
    # Failover — ISP, CORE, FW, WAN
    tests.append(TestCase("FAIL-01", TestLayer.FAILOVER, "ISP-1 Failure <5 sec", "فشل مزود 1 <5 ث", "HQ", "Shutdown EDGE-01 ISP1", "Failover ISP2 <5 sec PASS", True))
    tests.append(TestCase("FAIL-02", TestLayer.FAILOVER, "CORE-01 Failure <3 sec", "فشل أساسي 01 <3 ث", "HQ", "Power off CORE-01", "CORE-02 SVL <3 sec PASS", True))
    tests.append(TestCase("FAIL-03", TestLayer.FAILOVER, "FW-01 HA Failure <5 sec", "فشل جدار 01 <5 ث", "HQ", "Power off FW-01 Active", "FW-02 Active <5 sec PASS", True))
    
    return tests


def tests_to_dict_generic(company: GenericCompanyDef) -> List[Dict]:
    """Convert tests to dict for API — generic"""
    return [
        {
            "test_id": t.test_id,
            "layer": t.layer.value,
            "title": t.title_en,
            "title_ar": t.title_ar,
            "site": t.site,
            "command": t.command,
            "expected": t.expected,
            "critical": t.critical,
        } for t in generate_all_tests_generic(company)
    ]
