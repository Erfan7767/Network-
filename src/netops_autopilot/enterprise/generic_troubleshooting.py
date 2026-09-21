"""
Generic Troubleshooting — WORLD-CLASS PROFESSIONAL — 40Y Expert — ULTRA LEGENDARY v3

Troubleshooting adapts to ANY institution type: hospital, factory, school, hotel,
bank, retail, government, office, datacenter, trading — ANY size/branches/devices.

Each institution has unique failure modes with microscopic precision:
- Hospital: Medical device DOWN VLAN 110 HIPAA life-critical, PACS slow 10G jumbo, EMR unreachable, HIPAA audit fail, pharmacy, lab
- Factory: OT DOWN VLAN 210 ISA-99 production stop, PLC→SCADA timeout, Robotics real-time <1ms fail, Production line stop, warehouse WMS
- School: STUDENTS VLAN 310 CIPA filtered per-user 2M, LABS VLAN 320 per-dept isolation, Dorm, Faculty, CIPA/FERPA
- Hotel: PMS→Door lock fail VLAN 440 Opera RFID, POS PCI fail VLAN 420, IPTV multicast fail, Guest per-room isolation VLAN 410 privacy
- Bank: BANKING VLAN 510 very_high PCI-DSS SOX no Internet but teller cannot reach core banking 802.1X, ATM VLAN 520 isolated PCI-DSS VPN only, VAULT VLAN 530 air-gapped dual auth
- Government: CLASSIFIED VLAN 610 air-gapped NIST FISMA TEMPEST, Citizen kiosk VLAN 620 Internet only no internal, Justice isolated
- Retail: POS VLAN 410 PCI-DSS encrypted 10 stores, RFID inventory VLAN 430 real-time WMS, warehouse
- Datacenter: STORAGE VLAN 810 iSCSI jumbo 9000 40G/100G, VMOTION isolated 10G+, BACKUP-DC replication 100G, Leaf-Spine ECMP
- Trading: ERP unreachable but Internet OK, File SMB fail, VOIP QoS EF, etc.
- Office: Users, VOICE, WIFI, GUEST, etc.

No random config changes — evidence before change — microscopic precision — 40Y expert RCA — ULTRA LEGENDARY v3 — world-class first-grade.
"""

from __future__ import annotations
from typing import Dict, List

from .troubleshooting import ScenarioType, RCAStep, TroubleshootingScenario, SCENARIOS
from .institution_types import get_institution_profile

# Institution-specific scenarios — WORLD-CLASS — 40Y expert — ULTRA LEGENDARY v3 — microscopic precision

INSTITUTION_SCENARIOS: Dict[str, Dict[str, TroubleshootingScenario]] = {
    "hospital": {
        "medical_down": TroubleshootingScenario(
            scenario_type=ScenarioType.BRANCH_DOWN,
            title_en="Hospital — Medical devices DOWN — VLAN 110 — life-critical — HIPAA — no Internet",
            title_ar="مستشفى — أجهزة طبية ساقطة — VLAN 110 — حرجة للحياة — HIPAA — بدون إنترنت",
            symptom_en="Medical devices in VLAN 110 MEDICAL cannot reach EMR 10.10.130.10 — HIPAA — life-critical — no Internet by design — PACS/EMR/HIS",
            symptom_ar="أجهزة طبية في VLAN 110 لا تصل EMR 10.10.130.10 — حرجة للحياة — HIPAA",
            rca_steps=[
                RCAStep(1, "Medical VLAN SVI up?", "SVI طبية تعمل؟", "show ip interface brief Vlan110", "up up", "If down → SVI, VLAN", "no shutdown Vlan110"),
                RCAStep(2, "ACL blocking?", "ACL يمنع؟", "show access-lists ACL_VLAN110_IN", "permit to EMR 10.x.130.10 only", "If deny → ACL", "Fix ACL_VLAN110_IN permit to 10.x.130.10 only"),
                RCAStep(3, "EMR server up?", "خادم EMR يعمل؟", "ping 10.10.130.10, check EMR01", "Up", "If down → server, VLAN 130", "Check EMR01 10.10.130.10 VLAN 130"),
                RCAStep(4, "HIPAA audit log?", "سجل تدقيق HIPAA؟", "show logging | include 110", "Logs present 7y", "If no log → syslog", "Check syslog 10.10.30.31 audit 7y"),
                RCAStep(5, "Medical device power?", "طاقة أجهزة طبية؟", "show power inline | include 110", "PoE up", "If down → PoE", "Check PoE budget, power inline"),
            ],
            possible_causes=[
                "ACL_VLAN110_IN DENY — medical isolated by design — must permit to EMR 10.10.130.10 only per HIPAA",
                "EMR01 10.10.130.10 DOWN — check server, VLAN 130 SVI, power, HIS",
                "VLAN 110 SVI DOWN — no shutdown, check CORE C9500 SVL",
                "HIPAA compliance — audit log missing 7y — syslog 10.10.30.31",
                "PoE budget exceeded — medical devices need PoE+ — check power budget",
            ],
            fix_en="Fix ACL_VLAN110_IN: permit 10.x.110.0 to 10.x.130.10 EMR only, deny Internet per HIPAA life-critical. Verify medical→EMR PASS, medical→Internet BLOCK PASS, audit log 7y present, medical devices PoE up, NMS green, PACS/EMR/HIS integration PASS.",
            fix_ar="إصلاح ACL: السماح طبي→EMR فقط، منع إنترنت HIPAA حرجة للحياة. تحقق طبي→EMR نجاح، طبي→إنترنت منع، سجل 7 سنوات، أجهزة طبية PoE، PACS/EMR/HIS نجاح.",
            verification=["Medical 10.x.110.x → EMR 10.x.130.10 PASS", "Medical → Internet BLOCK PASS", "HIPAA audit log 7y present PASS", "NMS medical devices green PASS", "PoE medical devices up PASS", "PACS 10.x.120.10 reachable PASS", "HIS integration PASS"],
            is_security=True,
        ),
        "pacs_slow": TroubleshootingScenario(
            scenario_type=ScenarioType.WIFI_SLOW,
            title_en="Hospital — PACS slow — 10G jumbo 9000 — medical imaging 100MB+ per study",
            title_ar="مستشفى — PACS بطيء — 10G jumbo 9000 — أشعة — صور طبية كبيرة",
            symptom_en="PACS Server 10.10.120.10 slow — medical imaging 100MB+ per study — DICOM — needs 10G jumbo 9000 OM4 SFP+ — throughput <1Gbps FAIL",
            symptom_ar="خادم PACS بطيء — صور طبية كبيرة 100MB+ — DICOM — يحتاج 10G jumbo 9000 — إنتاجية <1Gbps فشل",
            rca_steps=[
                RCAStep(1, "Jumbo enabled?", "Jumbo مفعل؟", "show system mtu, show interfaces Te1/0/1 mtu", "9000", "If 1500 → no jumbo", "system mtu 9000, interface mtu 9000"),
                RCAStep(2, "Link 10G?", "رابط 10G؟", "show interfaces status", "10G", "If 1G → bottleneck", "Check fiber OM4, SFP+ 10G-SR, QSFP"),
                RCAStep(3, "PACS server CPU?", "معالج PACS؟", "Check PACS01 CPU/memory/storage I/O", "<80%", "If 95% → server", "Check PACS01 10.10.120.10 CPU, storage, DICOM"),
                RCAStep(4, "DICOM port?", "منفذ DICOM؟", "show access-lists | include 120", "permit DICOM 104/11112", "If deny → ACL", "Allow DICOM ports 104, 11112 to PACS"),
            ],
            possible_causes=[
                "Jumbo not enabled — MTU 1500 → fragmentation → slow — enable 9000 system+interface",
                "Link 1G not 10G — fiber OM4, SFP+ 10G-SR — upgrade to 10G/40G",
                "PACS01 CPU 95% — storage I/O bottleneck — check server, storage array",
                "ACL blocking DICOM ports 104/11112 — must permit medical→PACS DICOM",
            ],
            fix_en="Enable jumbo 9000 system+interface, verify 10G link OM4 SFP+ SR, PACS01 CPU <80%, DICOM ports 104/11112 ALLOW. Verify PACS throughput 9Gbps+ PASS, medical imaging <2 sec PASS, DICOM PASS, radiology workflow PASS.",
            fix_ar="تفعيل jumbo 9000، تحقق رابط 10G OM4 SFP+، معالج PACS <80%، منافذ DICOM 104/11112 سماح. تحقق إنتاجية PACS 9Gbps+ نجاح، صور <2 ثانية نجاح، DICOM نجاح.",
            verification=["MTU 9000 PASS", "10G link PASS", "PACS throughput 9Gbps+ PASS", "Medical imaging <2 sec PASS", "DICOM 104/11112 PASS", "Radiology workflow PASS"],
        ),
        "emr_encrypted": TroubleshootingScenario(
            scenario_type=ScenarioType.ERP_UNREACHABLE,
            title_en="Hospital — EMR unreachable — VLAN 130 — encrypted TLS 1.2+ — HIPAA — 7y audit",
            title_ar="مستشفى — EMR لا يصل — VLAN 130 — مشفر TLS 1.2+ — HIPAA — تدقيق 7 سنوات",
            symptom_en="EMR 10.10.130.10 unreachable from medical VLAN 110 — encrypted TLS 1.2+ — HIPAA — audit log 7y required — HIS integration",
            symptom_ar="EMR 10.10.130.10 لا يصل من VLAN طبية 110 — مشفر TLS 1.2+ — HIPAA — تدقيق 7 سنوات",
            rca_steps=[
                RCAStep(1, "EMR SVI up?", "SVI EMR؟", "show ip interface brief Vlan130", "up up", "If down → SVI", "no shutdown Vlan130"),
                RCAStep(2, "TLS 1.2+?", "TLS 1.2+؟", "show crypto | include 130", "TLS 1.2+", "If TLS 1.0 → HIPAA fail", "Enable TLS 1.2+ for EMR"),
                RCAStep(3, "EMR server up?", "خادم EMR يعمل؟", "ping 10.10.130.10:443", "Up", "If down → server", "Check EMR01 10.10.130.10"),
                RCAStep(4, "Audit log?", "سجل تدقيق؟", "show log | include 130", "7y logs", "If no log → syslog", "Check syslog 10.10.30.31 7y"),
            ],
            possible_causes=[
                "EMR SVI DOWN — check CORE",
                "TLS 1.0 not 1.2+ — HIPAA requires TLS 1.2+ — enable TLS 1.2+",
                "EMR01 DOWN — check server",
                "Audit log missing — HIPAA 7y — syslog",
            ],
            fix_en="Fix EMR SVI up, TLS 1.2+ encryption, EMR01 up, audit log 7y. Verify EMR→Medical PASS encrypted, EMR→Internet BLOCK, HIPAA PASS, HIS integration PASS.",
            fix_ar="إصلاح SVI EMR، تشفير TLS 1.2+، خادم EMR، سجل 7 سنوات. تحقق EMR→طبي نجاح مشفر، EMR→إنترنت منع، HIPAA نجاح.",
            verification=["EMR 10.x.130.10:443 TLS 1.2+ PASS", "Medical → EMR encrypted PASS", "EMR → Internet BLOCK PASS", "HIPAA audit 7y PASS", "HIS integration PASS"],
            is_security=True,
        ),
    },
    "factory": {
        "ot_down": TroubleshootingScenario(
            scenario_type=ScenarioType.BRANCH_DOWN,
            title_en="Factory — OT DOWN — VLAN 210 — ISA-99 — production line STOP — critical — no Internet",
            title_ar="مصنع — OT ساقط — VLAN 210 — ISA-99 — توقف خط إنتاج — حرج — بدون إنترنت",
            symptom_en="OT devices VLAN 210 cannot reach SCADA 10.10.210.10 — ISA-99 isolated no Internet — production line STOP — PLC/SCADA — critical — MES",
            symptom_ar="أجهزة OT VLAN 210 لا تصل SCADA 10.10.210.10 — ISA-99 معزول بدون إنترنت — توقف خط إنتاج — حرج — PLC/SCADA",
            rca_steps=[
                RCAStep(1, "OT SVI up?", "SVI OT تعمل؟", "show ip interface brief Vlan210", "up up", "If down → SVI", "no shutdown Vlan210"),
                RCAStep(2, "SCADA up?", "SCADA يعمل؟", "ping 10.10.210.10, check SCADA server", "Up", "If down → server", "Check SCADA 10.10.210.10, PLC"),
                RCAStep(3, "ISA-99 ACL?", "ACL ISA-99؟", "show access-lists ACL_VLAN210_IN", "permit to SCADA only", "If wrong → ACL", "Fix ACL permit OT to SCADA 10.10.210.10 only per ISA-99"),
                RCAStep(4, "Production line?", "خط إنتاج؟", "Check PLC status, MES 10.10.220.10, robotics 10.10.240.10", "Up RUN", "If down → PLC, MES, robotics", "Check PLC, MES, robotics controllers"),
                RCAStep(5, "OT power industrial?", "طاقة OT صناعية؟", "show power inline, check industrial power", "Up", "If down → power", "Check industrial power, UPS, OT cabinets"),
            ],
            possible_causes=[
                "OT SVI DOWN — production STOP — no shutdown Vlan210 — CORE C9500 SVL",
                "SCADA 10.10.210.10 DOWN — check server, power, VLAN 210, PLC hardware",
                "ACL blocking OT→SCADA — must permit OT 10.10.10.0 to SCADA 10.10.210.10 only per ISA-99/IEC 62443",
                "PLC down — check PLC hardware, power, OT network, industrial cabinets",
                "MES 10.10.220.10 DOWN — manufacturing execution — check MES server",
                "Industrial power fail — OT cabinets — check UPS, power",
            ],
            fix_en="Fix OT SVI up, SCADA up, PLC up, MES up, ACL permit OT to SCADA only per ISA-99, industrial power up. Verify OT→SCADA PASS, OT→Internet BLOCK PASS, production line RUN PASS, PLC→SCADA deterministic <1ms PASS, ISA-99 compliance PASS, IEC 62443 PASS.",
            fix_ar="إصلاح SVI OT، SCADA، PLC، MES، ACL سماح OT→SCADA فقط ISA-99، طاقة صناعية. تحقق OT→SCADA نجاح، OT→إنترنت منع، خط إنتاج يعمل، PLC→SCADA <1ms نجاح، ISA-99 نجاح.",
            verification=["OT 10.x.210.x → SCADA 10.x.210.10 PASS", "OT → Internet BLOCK PASS", "Production line RUN PASS", "PLC→SCADA deterministic <1ms PASS", "ISA-99 compliance PASS", "IEC 62443 PASS", "Industrial power PASS"],
            is_security=True,
        ),
        "robotics_realtime": TroubleshootingScenario(
            scenario_type=ScenarioType.WIFI_SLOW,
            title_en="Factory — Robotics real-time fail — VLAN 240 — deterministic <1ms — QoS priority — production quality FAIL",
            title_ar="مصنع — روبوتات فشل زمن حقيقي — VLAN 240 — حتمي <1ms — QoS أولوية — جودة إنتاج فشل",
            symptom_en="Robotics VLAN 240 latency >1ms — needs deterministic real-time <1ms — QoS priority — production quality FAIL — 6-axis robots",
            symptom_ar="VLAN روبوتات 240 زمن وصول >1ms — يحتاج حتمي <1ms — QoS أولوية — جودة إنتاج فشل — روبوتات 6 محاور",
            rca_steps=[
                RCAStep(1, "QoS deterministic priority?", "QoS حتمي أولوية؟", "show mls qos, show policy-map ROBOTICS, show queue", "Priority queue for VLAN 240", "If no QoS → latency >1ms", "mls qos, priority queue for VLAN 240, DSCP EF"),
                RCAStep(2, "Link congestion discards?", "ازدحام رابط فقد؟", "show interfaces counters errors, show interfaces status", "0 discards, 10G", "If discards → congestion", "Check bandwidth, add 10G, QoS shaping"),
                RCAStep(3, "Robot controller up <1ms?", "متحكم روبوت يعمل <1ms؟", "ping 10.10.240.10, check robot controller 6-axis", "Up <1ms", "If down → controller", "Check robot controller 10.10.240.10, real-time OS"),
                RCAStep(4, "Deterministic network?", "شبكة حتمية؟", "show clock, show ntp status, show ptp", "PTP synced", "If no PTP → jitter", "Enable PTP for robotics deterministic"),
            ],
            possible_causes=[
                "No QoS deterministic priority — robotics needs priority queue DSCP EF — mls qos + priority",
                "Link congestion discards — 1G congested — upgrade to 10G, QoS shaping",
                "Robot controller 10.10.240.10 DOWN — real-time OS — check controller hardware",
                "No PTP — jitter — enable PTP IEEE 1588 for deterministic <1ms",
            ],
            fix_en="Enable QoS deterministic priority DSCP EF for VLAN 240, check link 0 discards 10G, robot controller up <1ms, PTP synced. Verify latency 10.x.240.x → 10.x.240.10 <1ms PASS deterministic, robotics RUN PASS, production quality PASS, 6-axis precision PASS.",
            fix_ar="تفعيل QoS حتمي أولوية DSCP EF VLAN 240، فحص رابط 0 فقد 10G، متحكم روبوت <1ms، PTP متزامن. تحقق زمن <1ms نجاح حتمي، روبوتات تعمل نجاح، جودة إنتاج نجاح، دقة 6 محاور نجاح.",
            verification=["Latency 10.x.240.x → 10.x.240.10 <1ms deterministic PASS", "QoS priority DSCP EF PASS", "Robotics RUN PASS", "Production quality PASS", "6-axis precision PASS", "PTP synced PASS"],
        ),
        "plc_scada_timeout": TroubleshootingScenario(
            scenario_type=ScenarioType.ERP_UNREACHABLE,
            title_en="Factory — PLC→SCADA timeout — VLAN 210→220 — MES — production data FAIL",
            title_ar="مصنع — PLC→SCADA انتهاء مهلة — VLAN 210→220 — MES — بيانات إنتاج فشل",
            symptom_en="PLC 10.10.10.50 cannot reach SCADA 10.10.210.10:502 Modbus TCP — MES 10.10.220.10 cannot get production data — timeout",
            symptom_ar="PLC 10.10.10.50 لا يصل SCADA 10.10.210.10:502 Modbus TCP — MES لا يحصل بيانات إنتاج — انتهاء مهلة",
            rca_steps=[
                RCAStep(1, "Modbus port 502 ALLOW?", "منفذ Modbus 502 سماح؟", "show access-lists | include 502", "permit 502", "If deny → ACL", "Allow Modbus TCP 502 OT→SCADA"),
                RCAStep(2, "SCADA Modbus service up?", "خدمة SCADA Modbus تعمل؟", "check SCADA Modbus service 10.10.210.10:502", "Up", "If down → service", "Check SCADA Modbus service"),
                RCAStep(3, "PLC up?", "PLC يعمل؟", "ping 10.10.10.50, check PLC", "Up", "If down → PLC", "Check PLC 10.10.10.50 power, OT network"),
            ],
            possible_causes=[
                "ACL blocking Modbus TCP 502 — must permit OT→SCADA 502 per ISA-99",
                "SCADA Modbus service DOWN — check SCADA server Modbus service",
                "PLC 10.10.10.50 DOWN — check PLC hardware",
            ],
            fix_en="Fix ACL ALLOW Modbus TCP 502 OT→SCADA per ISA-99, SCADA Modbus service up, PLC up. Verify PLC→SCADA 502 PASS, MES→SCADA PASS, production data PASS.",
            fix_ar="إصلاح ACL سماح Modbus TCP 502 OT→SCADA ISA-99، خدمة SCADA Modbus، PLC. تحقق PLC→SCADA 502 نجاح، MES→SCADA نجاح، بيانات إنتاج نجاح.",
            verification=["PLC 10.10.10.50 → SCADA 10.10.210.10:502 Modbus PASS", "MES 10.10.220.10 → SCADA PASS", "Production data PASS", "ISA-99 PASS"],
        ),
    },
    "school": {
        "students_filter": TroubleshootingScenario(
            scenario_type=ScenarioType.BRANCH_DOWN,
            title_en="School — STUDENTS VLAN 310 filtered — CIPA — per-user 2Mbps — 500 students — Internet slow",
            title_ar="مدرسة — VLAN طلاب 310 مفلتر — CIPA — 2Mbps لكل مستخدم — 500 طالب — إنترنت بطيء",
            symptom_en="Students VLAN 310 cannot reach Internet or slow — CIPA content filter 10.10.30.30 — per-user bandwidth 2Mbps — 500 students concurrent — NAT",
            symptom_ar="VLAN طلاب 310 لا يصل إنترنت أو بطيء — فلتر CIPA 10.10.30.30 — 2Mbps لكل مستخدم — 500 طالب متزامن",
            rca_steps=[
                RCAStep(1, "STUDENTS SVI up?", "SVI طلاب؟", "show ip interface brief Vlan310", "up up", "If down → SVI", "no shutdown Vlan310"),
                RCAStep(2, "CIPA filter up?", "فلتر CIPA يعمل؟", "show content-filter status, ping 10.10.30.30", "Up", "If down → filter", "Check content-filter CIPA 10.10.30.30"),
                RCAStep(3, "Per-user QoS 2M?", "QoS 2M لكل مستخدم؟", "show policy-map STUDENTS, show qos interface", "2Mbps per user police", "If no limit → saturation", "police 2M per user VLAN 310, QoS shaping"),
                RCAStep(4, "NAT Internet?", "NAT إنترنت؟", "show ip nat translations | include 310, ping 8.8.8.8 source Vlan310", "NAT up", "If no NAT → Internet fail", "Check NAT overload, FW STUDENT→Internet ALLOW with CIPA"),
            ],
            possible_causes=[
                "STUDENTS SVI DOWN — check CORE C9500 SVL",
                "CIPA filter 10.10.30.30 DOWN — content-filter — check server, license",
                "No per-user QoS — 500 students saturate 1G — police 2M per user, QoS shaping",
                "FW DENY STUDENT→Internet — must ALLOW with CIPA filter per CIPA compliance",
                "NAT overload fail — check NAT pool, overload",
            ],
            fix_en="Fix STUDENTS SVI up, CIPA filter up 10.10.30.30, QoS per-user 2M police shaping, NAT overload, FW ALLOW STUDENT→Internet with CIPA filter. Verify STUDENT→Internet PASS with CIPA filter, STUDENT→Faculty BLOCK PASS, per-user 2M PASS, 500 students concurrent PASS, CIPA compliance PASS.",
            fix_ar="إصلاح SVI طلاب، فلتر CIPA 10.10.30.30، QoS 2M لكل مستخدم، NAT، جدار سماح طلاب→إنترنت مع CIPA. تحقق طلاب→إنترنت نجاح مع فلتر، طلاب→أعضاء منع، 2M نجاح، 500 طالب متزامن نجاح، CIPA نجاح.",
            verification=["STUDENT 10.x.10.x → Internet PASS with CIPA filter", "STUDENT → Faculty 10.x.20.x BLOCK PASS", "Per-user 2Mbps police PASS", "CIPA content filter PASS", "500 students concurrent PASS", "NAT overload PASS"],
        ),
        "lab_isolation": TroubleshootingScenario(
            scenario_type=ScenarioType.ERP_UNREACHABLE,
            title_en="School — LABS VLAN 320 isolation fail — per-dept — research data — FERPA",
            title_ar="مدرسة — عزل معامل VLAN 320 فشل — لكل قسم — بيانات بحث — FERPA",
            symptom_en="LABS VLAN 320 cannot reach LAB-SERVER 10.10.120.10 — per-dept isolation — research data — FERPA compliance — 10 labs",
            symptom_ar="VLAN معامل 320 لا تصل خادم معامل 10.10.120.10 — عزل لكل قسم — بيانات بحث — FERPA — 10 معامل",
            rca_steps=[
                RCAStep(1, "LABS SVI up?", "SVI معامل؟", "show ip interface brief Vlan320", "up up", "If down → SVI", "no shutdown Vlan320"),
                RCAStep(2, "LAB-SERVER up?", "خادم معامل يعمل؟", "ping 10.10.120.10, check LAB-SERVER", "Up", "If down → server", "Check 10.10.120.10, storage"),
                RCAStep(3, "Per-dept ACL?", "ACL لكل قسم؟", "show access-lists ACL_VLAN320_IN", "permit to LAB-SERVER per dept", "If wrong → ACL", "Fix ACL permit LABS to LAB-SERVER per-dept per FERPA"),
            ],
            possible_causes=[
                "LABS SVI DOWN — check CORE",
                "LAB-SERVER 10.10.120.10 DOWN — check server, storage",
                "ACL blocking LABS→LAB-SERVER — must permit per-dept per FERPA",
            ],
            fix_en="Fix LABS SVI up, LAB-SERVER up, ACL permit LABS→LAB-SERVER per-dept per FERPA. Verify LABS→LAB-SERVER PASS, LABS→Internet BLOCK, per-dept isolation PASS, FERPA PASS, 10 labs PASS.",
            fix_ar="إصلاح SVI معامل، خادم معامل، ACL سماح معامل→خادم لكل قسم FERPA. تحقق معامل→خادم نجاح، معامل→إنترنت منع، عزل لكل قسم نجاح، FERPA نجاح، 10 معامل نجاح.",
            verification=["LABS 10.x.20.x → LAB-SERVER 10.x.20.10 PASS", "LABS → Internet BLOCK PASS", "Per-dept isolation PASS", "FERPA PASS", "10 labs PASS"],
        ),
    },
    "bank": {
        "banking_block": TroubleshootingScenario(
            scenario_type=ScenarioType.ERP_UNREACHABLE,
            title_en="Bank — TELLER VLAN 540 cannot reach CORE_BANKING 10.10.110.10:443 — BANKING VLAN 510 very_high PCI-DSS SOX no Internet — 802.1X — audit 7y",
            title_ar="بنك — VLAN صراف 540 لا يصل نظام مصرفي أساسي 10.10.110.10:443 — VLAN مصرفية 510 عالية جدا PCI-DSS SOX بدون إنترنت — 802.1X — تدقيق 7 سنوات",
            symptom_en="Teller in VLAN 540 cannot reach CORE_BANKING 10.10.110.10:443 — BANKING VLAN 510 very_high PCI-DSS SOX GLBA no Internet by design — 802.1X auth — audit log 7y required — SOX compliance",
            symptom_ar="صراف VLAN 540 لا يصل نظام مصرفي أساسي 10.10.110.10:443 — VLAN مصرفية 510 عالية جدا PCI-DSS SOX GLBA بدون إنترنت — 802.1X مصادقة — تدقيق 7 سنوات — SOX",
            rca_steps=[
                RCAStep(1, "TELLER VLAN 540 SVI?", "SVI صراف 540؟", "show ip interface brief Vlan540", "up up", "If down → SVI", "no shutdown Vlan540"),
                RCAStep(2, "CORE_BANKING up?", "نظام أساسي يعمل؟", "ping 10.10.110.10:443, check core banking server", "Up", "If down → server", "Check 10.10.110.10 VLAN 510 very_high"),
                RCAStep(3, "802.1X teller auth?", "802.1X صراف مصادق؟", "show dot1x all, show authentication sessions, show radius", "Auth", "If fail → RADIUS, AD, cert", "Check RADIUS 10.10.30.10, AD, cert, 802.1X"),
                RCAStep(4, "FW TELLER→BANKING policy?", "سياسة جدار صراف→مصرفية؟", "show firewall policy | include 540 510", "ALLOW TELLER→BANKING 443 log", "If DENY → FW", "Allow TELLER 10.10.140.0/24 → BANKING 10.10.110.10:443 log per PCI-DSS SOX"),
                RCAStep(5, "Audit log 7y?", "سجل تدقيق 7 سنوات؟", "show log | include 510 540, show syslog", "Logs present 7y retention", "If no log → syslog", "Check syslog 10.10.30.31 audit 7y SOX"),
            ],
            possible_causes=[
                "TELLER VLAN 540 SVI DOWN — check CORE C9500 SVL SVI",
                "CORE_BANKING 10.10.110.10 DOWN — very_high security — check server, power, VLAN 510",
                "802.1X FAIL — teller not authenticated — RADIUS 10.10.30.10 timeout — check RADIUS, AD, certificate",
                "FW policy DENY TELLER→BANKING — PCI-DSS SOX — must ALLOW 443 to 10.10.110.10 with log per compliance",
                "Audit log missing 7y — SOX requires 7y retention — syslog 10.10.30.31",
            ],
            fix_en="Fix TELLER SVI up, CORE_BANKING up, 802.1X auth via RADIUS AD cert, FW ALLOW TELLER→BANKING 443 log per PCI-DSS SOX, audit log 7y to syslog. Verify TELLER→BANKING PASS, BANKING→Internet BLOCK PASS, 802.1X auth PASS, audit log 7y PASS, SOX compliance PASS, GLBA PASS.",
            fix_ar="إصلاح SVI صراف 540، نظام مصرفي أساسي 10.10.110.10، 802.1X عبر RADIUS AD شهادة، جدار سماح صراف→مصرفية 443 مع سجل PCI-DSS SOX، تدقيق 7 سنوات syslog. تحقق صراف→مصرفية نجاح، مصرفية→إنترنت منع، 802.1X نجاح، تدقيق 7 سنوات نجاح، SOX نجاح، GLBA نجاح.",
            verification=["TELLER 10.x.140.100 → CORE_BANKING 10.x.110.10:443 PASS", "BANKING 10.x.110.0 → Internet BLOCK PASS", "802.1X auth PASS", "Audit log 7y PASS", "SOX compliance PASS", "GLBA PASS", "PCI-DSS PASS"],
            is_security=True,
        ),
        "atm_isolated": TroubleshootingScenario(
            scenario_type=ScenarioType.BRANCH_DOWN,
            title_en="Bank — ATM VLAN 520 DOWN — isolated PCI-DSS VPN only — no user — 5 branches",
            title_ar="بنك — ATM VLAN 520 ساقط — معزول PCI-DSS VPN فقط — بدون مستخدم — 5 فروع",
            symptom_en="ATM in VLAN 520 cannot reach ATM_MGMT 10.10.120.10 — isolated PCI-DSS — VPN to central only — no user access by design — 5 branches ATMs",
            symptom_ar="ATM VLAN 520 لا يصل إدارة ATM 10.10.120.10 — معزول PCI-DSS — VPN للمركز فقط — بدون وصول مستخدم — 5 فروع ATMs",
            rca_steps=[
                RCAStep(1, "ATM SVI up?", "SVI ATM تعمل؟", "show ip interface brief Vlan520", "up up", "If down → SVI", "no shutdown Vlan520"),
                RCAStep(2, "ATM_MGMT up?", "إدارة ATM تعمل؟", "ping 10.10.120.10, check ATM_MGMT server", "Up", "If down → server", "Check 10.10.120.10"),
                RCAStep(3, "VPN to central up?", "VPN للمركز يعمل؟", "show crypto ipsec sa | include 520, show crypto isakmp sa", "Up", "If down → IPsec", "Check IPsec HQ 10.255.x.0/30, PSK, proposal AES256/SHA256"),
                RCAStep(4, "ACL ATM isolated?", "ACL ATM معزول؟", "show access-lists ACL_VLAN520_IN", "permit to ATM_MGMT only", "If wrong → ACL", "Fix ACL permit 10.x.120.0 to 10.x.120.10 only per PCI-DSS"),
            ],
            possible_causes=[
                "ATM SVI DOWN — check CORE",
                "ATM_MGMT 10.10.120.10 DOWN — check server",
                "VPN DOWN — ATM needs VPN to central — IPsec HQ 10.255.x.0/30, PSK, proposal AES256/SHA256",
                "ACL blocking ATM→ATM_MGMT — must permit to 10.10.120.10 only per PCI-DSS isolated",
            ],
            fix_en="Fix ATM SVI up, ATM_MGMT up, VPN up IPsec HQ 10.255.x.0/30 PSK AES256/SHA256, ACL permit ATM to ATM_MGMT only per PCI-DSS. Verify ATM→ATM_MGMT PASS, ATM→Internet BLOCK PASS, ATM→Users BLOCK PASS, VPN up PASS, PCI-DSS PASS, 5 branches ATMs PASS.",
            fix_ar="إصلاح SVI ATM، إدارة ATM، VPN IPsec HQ 10.255.x.0/30 PSK AES256/SHA256، ACL سماح ATM→إدارة فقط PCI-DSS. تحقق ATM→إدارة نجاح، ATM→إنترنت منع، ATM→مستخدمين منع، VPN نجاح، PCI-DSS نجاح، 5 فروع ATMs نجاح.",
            verification=["ATM 10.x.120.x → ATM_MGMT 10.x.120.10 PASS", "ATM → Internet BLOCK PASS", "ATM → Users BLOCK PASS", "VPN IPsec up PASS", "PCI-DSS PASS", "5 branches ATMs PASS"],
            is_security=True,
        ),
        "vault_airgap": TroubleshootingScenario(
            scenario_type=ScenarioType.BRANCH_DOWN,
            title_en="Bank — VAULT VLAN 530 air-gapped fail — dual auth — SOX — audit 7y — no network",
            title_ar="بنك — VLAN خزنة 530 فشل عزل هوائي — مصادقة ثنائية — SOX — تدقيق 7 سنوات — بدون شبكة",
            symptom_en="VAULT VLAN 530 not air-gapped — SOX requires air-gapped, dual auth, no network, audit 7y — compliance FAIL",
            symptom_ar="VLAN خزنة 530 غير معزول هوائيا — SOX يتطلب عزل هوائي، مصادقة ثنائية، بدون شبكة، تدقيق 7 سنوات — امتثال فشل",
            rca_steps=[
                RCAStep(1, "VAULT air-gapped?", "خزنة معزولة هوائيا؟", "show ip route Vlan530, show firewall policy", "No route, no wireless", "If route → air-gap fail", "Remove route, disable wireless for VAULT 530"),
                RCAStep(2, "Dual auth?", "مصادقة ثنائية؟", "show aaa, show dual-auth status", "Dual auth enabled", "If no dual auth → SOX fail", "Enable dual auth for VAULT"),
                RCAStep(3, "Audit log 7y?", "سجل تدقيق 7 سنوات؟", "show log | include 530", "7y logs", "If no log → syslog", "Check syslog 10.10.30.31 7y SOX"),
            ],
            possible_causes=[
                "VAULT not air-gapped — route to network exists — must remove per SOX",
                "No dual auth — SOX requires dual authorization for VAULT",
                "Audit log missing 7y — SOX requires",
            ],
            fix_en="Fix VAULT air-gapped — no route, no wireless, dual auth enabled, audit log 7y. Verify VAULT air-gapped PASS, dual auth PASS, audit 7y PASS, SOX PASS.",
            fix_ar="إصلاح خزنة معزولة هوائيا — بدون مسار، بدون لاسلكي، مصادقة ثنائية، سجل 7 سنوات. تحقق خزنة معزولة نجاح، مصادقة ثنائية نجاح، تدقيق 7 سنوات نجاح، SOX نجاح.",
            verification=["VAULT air-gapped PASS — no Internet, no wireless", "Dual auth PASS", "Audit log 7y PASS", "SOX PASS", "No network access PASS"],
            is_security=True,
        ),
    },
    "hotel": {
        "pms_door": TroubleshootingScenario(
            scenario_type=ScenarioType.ERP_UNREACHABLE,
            title_en="Hotel — PMS cannot reach Door Lock — VLAN 440 — Opera integration — RFID mobile key — guest check-in FAIL",
            title_ar="فندق — PMS لا يصل أقفال أبواب — VLAN 440 — تكامل Opera — RFID مفتاح جوال — تسجيل دخول فشل",
            symptom_en="PMS 10.10.30.20 cannot reach Door Lock System 10.10.140.10 — RFID mobile key — PMS integrated Opera — guest check-in FAIL — 200 rooms",
            symptom_ar="PMS 10.10.30.20 لا يصل نظام أقفال 10.10.140.10 — RFID مفتاح جوال — PMS متكامل Opera — تسجيل دخول فشل — 200 غرفة",
            rca_steps=[
                RCAStep(1, "PMS up?", "PMS يعمل؟", "ping 10.10.30.20, check PMS Opera", "Up", "If down → server", "Check PMS 10.10.30.20 Opera"),
                RCAStep(2, "Door Lock up?", "أقفال تعمل؟", "ping 10.10.140.10, check door lock controller RFID", "Up", "If down → controller", "Check 10.10.140.10 RFID controller"),
                RCAStep(3, "VLAN 440 SVI?", "SVI 440؟", "show ip interface brief Vlan440", "up up", "If down → SVI", "no shutdown Vlan440"),
                RCAStep(4, "FW PMS→DOOR policy?", "سياسة جدار PMS→أقفال؟", "show firewall policy | include 440 140", "ALLOW PMS→DOOR 443", "If DENY → FW", "Allow PMS 10.10.30.20 → Door Lock 10.10.140.10:443"),
                RCAStep(5, "Opera integration?", "تكامل Opera؟", "check Opera PMS integration API", "Up", "If down → Opera API", "Check Opera API, PMS integration"),
            ],
            possible_causes=[
                "PMS 10.10.30.20 DOWN — Opera — check server, Opera service",
                "Door Lock 10.10.140.10 DOWN — RFID controller — check controller, RFID",
                "VLAN 440 SVI DOWN — check CORE C9500 SVL",
                "FW DENY PMS→DOOR — must ALLOW 443 for Opera→Door Lock",
                "Opera integration API DOWN — check Opera PMS API",
            ],
            fix_en="Fix PMS up, Door Lock up, VLAN 440 SVI up, FW ALLOW PMS→DOOR 443, Opera API up. Verify PMS→DOOR PASS, guest check-in RFID PASS, Opera integration PASS, door lock mobile key PASS, 200 rooms PASS.",
            fix_ar="إصلاح PMS، أقفال أبواب، SVI 440، جدار سماح PMS→أقفال 443، واجهة Opera. تحقق PMS→أقفال نجاح، تسجيل دخول RFID نجاح، تكامل Opera نجاح، مفتاح جوال نجاح، 200 غرفة نجاح.",
            verification=["PMS 10.10.30.20 → Door Lock 10.10.140.10:443 PASS", "Guest check-in RFID PASS", "Opera integration PASS", "Door lock mobile key PASS", "200 rooms PASS"],
        ),
        "guest_room_isolation": TroubleshootingScenario(
            scenario_type=ScenarioType.ERP_UNREACHABLE,
            title_en="Hotel — GUEST-ROOM VLAN 410 per-room isolation fail — guest can see other guests — privacy FAIL — PCI-DSS",
            title_ar="فندق — عزل غرف ضيوف VLAN 410 فشل — ضيف يرى ضيوف آخرين — خصوصية فشل — PCI-DSS",
            symptom_en="Guest in room 101 VLAN 410 10.10.10.101 can ping guest in room 102 10.10.10.102 — per-room isolation FAIL — PCI-DSS privacy — 200 rooms",
            symptom_ar="ضيف غرفة 101 VLAN 410 10.10.10.101 يستطيع ping ضيف غرفة 102 10.10.10.102 — عزل لكل غرفة فشل — PCI-DSS خصوصية — 200 غرفة",
            rca_steps=[
                RCAStep(1, "Per-room isolation enabled?", "عزل لكل غرفة مفعل؟", "show dot1x, show port-security, show private-vlan", "Isolation per port/private VLAN", "If no isolation → privacy fail", "Enable per-room isolation — private VLAN or ACL DENY inter-guest"),
                RCAStep(2, "ACL GUEST-ROOM?", "ACL غرف ضيوف؟", "show access-lists ACL_VLAN410_IN", "DENY inter-guest 10.x.10.0 to 10.x.10.0, ALLOW Internet only", "If ALLOW inter-guest → privacy fail", "Fix ACL DENY 10.x.10.0 to 10.x.10.0, ALLOW Internet only per PCI-DSS privacy"),
                RCAStep(3, "WLC per-room isolation?", "WLC لكل غرفة عزل؟", "show wlan summary, show ap config, show wlan 410", "Per-room AP isolation", "If no isolation → WLC", "Enable WLC per-room isolation — AP isolation, peer-to-peer blocking"),
            ],
            possible_causes=[
                "No per-room isolation — private VLAN or ACL — privacy FAIL — PCI-DSS",
                "ACL ALLOW inter-guest — must DENY 10.x.10.0 to 10.x.10.0 per PCI-DSS privacy — 200 rooms",
                "WLC no per-room isolation — enable AP isolation, peer-to-peer blocking",
            ],
            fix_en="Enable per-room isolation private VLAN or ACL DENY inter-guest 10.x.10.0 to 10.x.10.0, WLC AP isolation peer-to-peer blocking. Verify GUEST-ROOM 101 10.x.10.101 → GUEST-ROOM 102 10.x.10.102 BLOCK PASS, GUEST-ROOM → Internet PASS, privacy per-room PASS, PCI-DSS PASS, WLC AP isolation PASS, 200 rooms PASS.",
            fix_ar="تفعيل عزل لكل غرفة VLAN خاصة أو ACL منع بين ضيوف 10.x.10.0→10.x.10.0، WLC عزل AP منع نظير لنظير. تحقق غرفة 101 10.10.10.101→غرفة 102 10.10.10.102 منع نجاح، غرف→إنترنت نجاح، خصوصية لكل غرفة نجاح، PCI-DSS نجاح، WLC عزل AP نجاح، 200 غرفة نجاح.",
            verification=["GUEST-ROOM 101 10.x.10.101 → GUEST-ROOM 102 10.x.10.102 BLOCK PASS", "GUEST-ROOM → Internet PASS", "Privacy per-room PASS", "PCI-DSS PASS", "WLC AP isolation peer-to-peer BLOCK PASS", "200 rooms PASS"],
            is_security=True,
        ),
        "pos_pci": TroubleshootingScenario(
            scenario_type=ScenarioType.ERP_UNREACHABLE,
            title_en="Hotel — POS VLAN 420 PCI-DSS — cannot reach POS-SERVER — encrypted — restaurant",
            title_ar="فندق — POS VLAN 420 PCI-DSS — لا يصل خادم POS — مشفر — مطعم",
            symptom_en="POS terminals VLAN 420 cannot reach POS-SERVER 10.10.120.10:443 — PCI-DSS isolated no Internet — encrypted — restaurant/bar POS",
            symptom_ar="أجهزة POS VLAN 420 لا تصل خادم POS 10.10.120.10 — PCI-DSS معزول بدون إنترنت — مشفر — مطعم",
            rca_steps=[
                RCAStep(1, "POS SVI up?", "SVI POS؟", "show ip interface brief Vlan420", "up up", "If down → SVI", "no shutdown Vlan420"),
                RCAStep(2, "POS-SERVER up?", "خادم POS يعمل؟", "ping 10.10.120.10:443", "Up", "If down → server", "Check POS-SERVER 10.10.120.10"),
                RCAStep(3, "PCI-DSS ACL?", "ACL PCI-DSS؟", "show access-lists ACL_VLAN420_IN", "permit to POS-SERVER 443 only", "If wrong → ACL", "Fix ACL permit POS to POS-SERVER 443 only per PCI-DSS"),
            ],
            possible_causes=[
                "POS SVI DOWN",
                "POS-SERVER 10.10.120.10 DOWN",
                "ACL blocking POS→POS-SERVER — PCI-DSS must permit 443 only",
            ],
            fix_en="Fix POS SVI up, POS-SERVER up, ACL permit POS→POS-SERVER 443 only per PCI-DSS. Verify POS→POS-SERVER 443 PASS, POS→Internet BLOCK, PCI-DSS PASS.",
            fix_ar="إصلاح SVI POS، خادم POS، ACL سماح POS→خادم 443 فقط PCI-DSS. تحقق POS→خادم 443 نجاح، POS→إنترنت منع، PCI-DSS نجاح.",
            verification=["POS 10.x.20.x → POS-SERVER 10.x.20.10:443 PASS", "POS → Internet BLOCK PASS", "PCI-DSS PASS"],
            is_security=True,
        ),
    },
    "retail": {
        "pos_pci": TroubleshootingScenario(
            scenario_type=ScenarioType.ERP_UNREACHABLE,
            title_en="Retail — POS VLAN 410 PCI-DSS — cannot reach POS-SERVER 10.10.120.10 — encrypted — 10 stores",
            title_ar="متجر — POS VLAN 410 PCI-DSS — لا يصل خادم POS 10.10.120.10 — مشفر — 10 متاجر",
            symptom_en="POS terminals VLAN 410 cannot reach POS-SERVER 10.10.120.10:443 — PCI-DSS isolated no Internet — encrypted — 10 stores POS sync — 1000 transactions/day",
            symptom_ar="أجهزة POS VLAN 410 لا تصل خادم POS 10.10.120.10 — PCI-DSS معزول بدون إنترنت — مشفر — 10 متاجر مزامنة POS — 1000 معاملة/يوم",
            rca_steps=[
                RCAStep(1, "POS SVI up?", "SVI POS؟", "show ip interface brief Vlan410", "up up", "If down → SVI", "no shutdown Vlan410"),
                RCAStep(2, "POS-SERVER up?", "خادم POS يعمل؟", "ping 10.10.120.10:443, check POS-SERVER", "Up", "If down → server", "Check 10.10.120.10"),
                RCAStep(3, "PCI-DSS ACL?", "ACL PCI-DSS؟", "show access-lists ACL_VLAN410_IN", "permit to POS-SERVER 443 only", "If wrong → ACL", "Fix ACL permit POS to POS-SERVER 443 only per PCI-DSS"),
                RCAStep(4, "Encryption TLS 1.2+?", "تشفير TLS 1.2+؟", "show crypto | include 410", "TLS 1.2+", "If TLS 1.0 → PCI-DSS fail", "Enable TLS 1.2+ for POS"),
                RCAStep(5, "10 stores sync?", "مزامنة 10 متاجر؟", "check POS sync HQ 10 stores", "Sync up", "If sync fail → WAN, IPsec", "Check IPsec WAN HQ hub 10.255.x.0/30, POS sync"),
            ],
            possible_causes=[
                "POS SVI DOWN — check CORE",
                "POS-SERVER 10.10.120.10 DOWN — check server",
                "ACL blocking POS→POS-SERVER — PCI-DSS must permit 443 only",
                "No TLS 1.2+ encryption — PCI-DSS requires encrypted",
                "WAN IPsec DOWN — 10 stores cannot sync POS — check IPsec HQ hub",
            ],
            fix_en="Fix POS SVI up, POS-SERVER up, ACL permit POS→POS-SERVER 443 only per PCI-DSS, TLS 1.2+ encryption, IPsec WAN HQ hub 10.255.x.0/30 up. Verify POS→POS-SERVER 443 PASS, POS→Internet BLOCK PASS, POS→Users BLOCK PASS, PCI-DSS audit PASS, TLS 1.2+ PASS, 10 stores POS sync PASS, 1000 transactions/day PASS.",
            fix_ar="إصلاح SVI POS، خادم POS، ACL سماح POS→خادم 443 فقط PCI-DSS، تشفير TLS 1.2+، WAN IPsec HQ 10.255.x.0/30. تحقق POS→خادم 443 نجاح، POS→إنترنت منع، POS→مستخدمين منع، PCI-DSS نجاح، TLS 1.2+ نجاح، 10 متاجر مزامنة POS نجاح، 1000 معاملة/يوم نجاح.",
            verification=["POS 10.x.10.x → POS-SERVER 10.x.20.10:443 PASS", "POS → Internet BLOCK PASS", "POS → Users BLOCK PASS", "PCI-DSS audit PASS", "TLS 1.2+ PASS", "10 stores POS sync PASS", "1000 transactions/day PASS"],
            is_security=True,
        ),
        "rfid_inventory": TroubleshootingScenario(
            scenario_type=ScenarioType.WIFI_SLOW,
            title_en="Retail — RFID inventory slow — VLAN 430 — real-time — WMS 10.10.130.10 — 1000 items",
            title_ar="متجر — جرد RFID بطيء — VLAN 430 — زمن حقيقي — WMS 10.10.130.10 — 1000 صنف",
            symptom_en="RFID readers VLAN 430 slow — inventory real-time — WMS 10.10.130.10 — 1000 items — real-time <100ms FAIL — warehouse",
            symptom_ar="قارئات RFID VLAN 430 بطيئة — جرد زمن حقيقي — WMS 10.10.130.10 — 1000 صنف — زمن حقيقي <100ms فشل — مستودع",
            rca_steps=[
                RCAStep(1, "RFID SVI up?", "SVI RFID؟", "show ip interface brief Vlan430", "up up", "If down → SVI", "no shutdown Vlan430"),
                RCAStep(2, "WMS up?", "WMS يعمل؟", "ping 10.10.130.10, check WMS", "Up", "If down → server", "Check WMS 10.10.130.10"),
                RCAStep(3, "Real-time QoS priority?", "QoS زمن حقيقي أولوية؟", "show mls qos, show policy-map RFID", "Priority for VLAN 430", "If no QoS → latency", "Enable QoS priority for VLAN 430 RFID"),
            ],
            possible_causes=[
                "RFID SVI DOWN — check CORE",
                "WMS 10.10.130.10 DOWN — check server",
                "No QoS real-time — RFID needs priority — enable QoS",
            ],
            fix_en="Fix RFID SVI up, WMS up, QoS priority for VLAN 430. Verify RFID→WMS real-time PASS <100ms, inventory 1000 items PASS, WMS sync PASS.",
            fix_ar="إصلاح SVI RFID، WMS، QoS أولوية VLAN 430. تحقق RFID→WMS زمن حقيقي نجاح <100ms، جرد 1000 صنف نجاح، مزامنة WMS نجاح.",
            verification=["RFID 10.x.30.x → WMS 10.x.30.10 real-time <100ms PASS", "Inventory 1000 items PASS", "WMS sync PASS", "Warehouse PASS"],
        ),
    },
    "government": {
        "classified_airgap": TroubleshootingScenario(
            scenario_type=ScenarioType.BRANCH_DOWN,
            title_en="Government — CLASSIFIED VLAN 610 air-gapped fail — NIST FISMA — TEMPEST — no Internet no wireless",
            title_ar="حكومة — VLAN مصنف 610 فشل عزل هوائي — NIST FISMA — TEMPEST — بدون إنترنت بدون لاسلكي",
            symptom_en="CLASSIFIED VLAN 610 cannot be air-gapped — NIST FISMA requires no Internet, no wireless, TEMPEST, AES256, audit 7y — compliance FAIL — classified room",
            symptom_ar="VLAN مصنف 610 لا يمكن عزله هوائيا — NIST FISMA يتطلب بدون إنترنت، بدون لاسلكي، TEMPEST، AES256، تدقيق 7 سنوات — امتثال فشل — غرفة مصنفة",
            rca_steps=[
                RCAStep(1, "CLASSIFIED SVI up?", "SVI مصنف؟", "show ip interface brief Vlan610", "up up", "If down → SVI", "no shutdown Vlan610"),
                RCAStep(2, "Air-gapped no Internet?", "معزول هوائيا بدون إنترنت؟", "show ip route Vlan610, show firewall policy, show ip nat", "No route to Internet, no NAT", "If route/NAT → air-gap fail", "Remove route to Internet, remove NAT for VLAN 610 per NIST FISMA"),
                RCAStep(3, "Wireless disabled?", "لاسلكي معطل؟", "show wlan summary | include 610, show ap config", "No wireless for 610", "If wireless → TEMPEST fail", "Disable wireless for VLAN 610 — TEMPEST"),
                RCAStep(4, "Encryption AES256?", "تشفير AES256؟", "show crypto | include 610, show encryption", "AES256", "If no AES256 → NIST fail", "Enable AES256 for CLASSIFIED per NIST"),
                RCAStep(5, "Audit log 7y?", "سجل تدقيق 7 سنوات؟", "show log | include 610, show syslog status", "7y logs present retention", "If no log → syslog", "Check syslog 10.10.30.31 7y retention per FISMA"),
            ],
            possible_causes=[
                "CLASSIFIED SVI DOWN — check CORE C9500 SVL",
                "Not air-gapped — route to Internet exists — must remove per NIST FISMA — classified room TEMPEST",
                "Wireless enabled for CLASSIFIED — must disable — TEMPEST — no wireless per NIST",
                "No AES256 encryption — NIST requires AES256 for CLASSIFIED",
                "Audit log missing 7y — FISMA requires 7y retention — syslog 10.10.30.31",
            ],
            fix_en="Fix CLASSIFIED SVI up, air-gap — no Internet route, no NAT, no wireless per TEMPEST, AES256 encryption per NIST, audit log 7y to syslog per FISMA. Verify CLASSIFIED→Internet BLOCK PASS, CLASSIFIED→Wireless BLOCK PASS, encryption AES256 PASS, audit log 7y PASS, NIST FISMA PASS, TEMPEST PASS, air-gapped PASS — classified room secure.",
            fix_ar="إصلاح SVI مصنف 610، عزل هوائي — بدون مسار إنترنت، بدون NAT، بدون لاسلكي TEMPEST، تشفير AES256 NIST، سجل 7 سنوات syslog FISMA. تحقق مصنف→إنترنت منع نجاح، مصنف→لاسلكي منع نجاح، تشفير AES256 نجاح، تدقيق 7 سنوات نجاح، NIST FISMA نجاح، TEMPEST نجاح، معزول هوائيا نجاح — غرفة مصنفة آمنة.",
            verification=["CLASSIFIED 10.x.10.x → Internet BLOCK PASS", "CLASSIFIED → Wireless BLOCK PASS", "AES256 encryption PASS", "Audit log 7y retention PASS", "NIST FISMA compliance PASS", "TEMPEST PASS", "Air-gapped no route PASS", "Classified room secure PASS"],
            is_security=True,
        ),
        "citizen_kiosk": TroubleshootingScenario(
            scenario_type=ScenarioType.ERP_UNREACHABLE,
            title_en="Government — Citizen kiosk VLAN 620 Internet only — cannot reach internal — by design NIST — citizen portal DMZ",
            title_ar="حكومة — كشك مواطن VLAN 620 إنترنت فقط — لا يصل داخلي — تصميم NIST — بوابة مواطن DMZ",
            symptom_en="Citizen kiosk VLAN 620 cannot reach Internet — should be Internet only no internal per NIST — citizen portal DMZ 10.10.30.50 — public portal",
            symptom_ar="كشك مواطن VLAN 620 لا يصل إنترنت — يجب إنترنت فقط بدون داخلي NIST — بوابة مواطن DMZ 10.10.30.50 — بوابة عامة",
            rca_steps=[
                RCAStep(1, "Kiosk SVI up?", "SVI كشك؟", "show ip interface brief Vlan620", "up up", "If down → SVI", "no shutdown Vlan620"),
                RCAStep(2, "Internet up via NAT?", "إنترنت عبر NAT؟", "show ip nat translations | include 620, ping 8.8.8.8 source Vlan620", "NAT up, Internet PASS", "If no NAT → Internet fail", "Check NAT overload, FW KIOSK→Internet ALLOW"),
                RCAStep(3, "Internal BLOCK?", "داخلي ممنوع؟", "ping 10.10.0.1 source Vlan620, ping 10.10.30.10 source Vlan620", "BLOCK", "If ALLOW → security FAIL", "Fix ACL DENY KIOSK 10.x.20.0 to Internal 10.x.0.0, ALLOW Internet only per NIST"),
                RCAStep(4, "Citizen portal DMZ?", "بوابة مواطن DMZ؟", "ping 10.10.30.50 source Vlan620", "ALLOW to DMZ only", "If BLOCK → portal fail", "Allow KIOSK to citizen portal DMZ 10.10.30.50:443 only"),
            ],
            possible_causes=[
                "Kiosk SVI DOWN — check CORE",
                "Internet DOWN — NAT overload fail, FW DENY — check NAT, FW KIOSK→Internet ALLOW",
                "Internal not BLOCKED — security FAIL — must DENY KIOSK→Internal per NIST — kiosk Internet only",
                "Citizen portal DMZ 10.10.30.50 BLOCKED — must ALLOW KIOSK→DMZ 443 only",
            ],
            fix_en="Fix Kiosk SVI up, Internet via NAT overload ALLOW, internal DENY per NIST, citizen portal DMZ 10.10.30.50 ALLOW 443 only. Verify KIOSK→Internet PASS, KIOSK→Internal 10.x.0.0 BLOCK PASS, KIOSK→AD BLOCK, citizen portal DMZ 10.10.30.50:443 PASS, NIST PASS, public portal secure.",
            fix_ar="إصلاح SVI كشك 620، إنترنت عبر NAT سماح، داخلي منع NIST، بوابة مواطن DMZ 10.10.30.50 سماح 443 فقط. تحقق كشك→إنترنت نجاح، كشك→داخلي 10.x.0.0 منع نجاح، كشك→AD منع، بوابة مواطن DMZ 443 نجاح، NIST نجاح، بوابة عامة آمنة.",
            verification=["KIOSK 10.x.20.x → Internet PASS", "KIOSK → Internal 10.x.0.0 BLOCK PASS", "KIOSK → AD 10.x.30.10 BLOCK PASS", "Citizen portal DMZ 10.10.30.50:443 PASS", "NIST PASS", "Public portal secure PASS"],
            is_security=True,
        ),
    },

    "datacenter": {
        "storage_jumbo": TroubleshootingScenario(
            scenario_type=ScenarioType.WIFI_SLOW,
            title_en="Datacenter — STORAGE VLAN 810 iSCSI slow — jumbo 9000 — 40G/100G — VM storage latency high >5ms — ULTRA LEGENDARY v4",
            title_ar="مركز بيانات — تخزين VLAN 810 iSCSI بطيء — jumbo 9000 — 40G/100G — زمن وصول تخزين VM عالي >5ms — فائق الأسطورية v4",
            symptom_en="Storage VLAN 810 iSCSI slow — needs jumbo 9000 40G/100G — VM storage latency high >5ms — VM FAIL — vMotion — storage array — 50 racks — datacenter",
            symptom_ar="تخزين VLAN 810 iSCSI بطيء — يحتاج jumbo 9000 40G/100G — زمن وصول تخزين VM عالي >5ms — VM فشل — vMotion — مصفوفة تخزين — 50 رف — مركز بيانات",
            rca_steps=[
                RCAStep(1, "Jumbo 9000 enabled?", "Jumbo 9000 مفعل؟", "show system mtu, show interfaces Te1/0/1 mtu, show interfaces Fo1/0/1 mtu", "9000", "If 1500 → fragmentation → slow", "system mtu 9000, interface mtu 9000, jumbo"),
                RCAStep(2, "40G/100G link?", "رابط 40G/100G؟", "show interfaces status, show interfaces transceiver", "40G/100G", "If 10G → bottleneck", "Check QSFP 40G-SR4 / 100G-SR4, fiber OM4/SMF, 40G/100G"),
                RCAStep(3, "Storage server up iSCSI 3260?", "خادم تخزين يعمل iSCSI 3260؟", "ping 10.10.110.10, check iSCSI target 10.10.110.10:3260, show iscsi", "Up", "If down → server", "Check storage 10.10.110.10 iSCSI target 3260, storage array"),
                RCAStep(4, "vCenter up?", "vCenter يعمل؟", "ping 10.10.30.10, check vCenter, vMotion", "Up", "If down → vCenter", "Check vCenter 10.10.30.10, vMotion VLAN 830 isolated 10G+"),
                RCAStep(5, "Storage throughput?", "إنتاجية تخزين؟", "check storage throughput, IOPS, latency", "40Gbps, <1ms", "If slow → storage", "Check storage array, IOPS, latency, throughput"),
            ],
            possible_causes=[
                "Jumbo not 9000 — iSCSI needs 9000 — enable system mtu 9000 + interface mtu 9000 — fragmentation → slow",
                "Link 10G not 40G/100G — storage needs 40G/100G — QSFP 40G-SR4 / 100G-SR4 OM4/SMF",
                "Storage server 10.10.110.10 DOWN — iSCSI target 3260 — check server, storage array",
                "vCenter 10.10.30.10 DOWN — VM management — check vCenter, vMotion VLAN 830 isolated 10G+",
                "Storage array IOPS bottleneck — check array, latency, throughput",
            ],
            fix_en="Enable jumbo 9000 system+interface, verify 40G/100G link QSFP 40G-SR4/100G-SR4 OM4/SMF, storage 10.10.110.10 up iSCSI 3260, vCenter 10.10.30.10 up, storage array IOPS OK. Verify storage throughput 40Gbps PASS, VM storage latency <1ms PASS, IOPS 100k+ PASS, vMotion 10G+ isolated PASS, Leaf-Spine ECMP PASS — datacenter 50 racks — ULTRA LEGENDARY v4 — 40Y expert.",
            fix_ar="تفعيل jumbo 9000 نظام+واجهة، تحقق رابط 40G/100G QSFP 40G-SR4/100G-SR4 OM4/SMF، تخزين 10.10.110.10 iSCSI 3260 يعمل، vCenter 10.10.30.10 يعمل، مصفوفة تخزين IOPS جيد. تحقق إنتاجية تخزين 40Gbps نجاح، زمن تخزين VM <1ms نجاح، IOPS 100k+ نجاح، vMotion 10G+ معزول نجاح، Leaf-Spine ECMP نجاح — مركز بيانات 50 رف — فائق الأسطورية v4 — 40 عام خبير.",
            verification=["MTU 9000 jumbo PASS", "40G/100G link PASS QSFP", "Storage 10.10.110.10:3260 iSCSI PASS", "VM storage latency <1ms PASS", "IOPS 100k+ PASS", "vMotion 10G+ isolated PASS", "Leaf-Spine ECMP PASS", "vCenter 10.10.30.10 PASS"],
        ),
        "leaf_spine_ecmp": TroubleshootingScenario(
            scenario_type=ScenarioType.BRANCH_DOWN,
            title_en="Datacenter — Leaf-Spine ECMP fail — 40G/100G — BGP — load balancing FAIL — throughput <50% — ULTRA LEGENDARY v4",
            title_ar="مركز بيانات — Leaf-Spine ECMP فشل — 40G/100G — BGP — موازنة حمل فشل — إنتاجية <50% — فائق الأسطورية v4",
            symptom_en="Leaf-Spine ECMP not load balancing — 40G/100G links — BGP — one link saturated, others idle — ECMP FAIL — throughput <50% — 50 racks — datacenter",
            symptom_ar="Leaf-Spine ECMP لا يوازن حمل — روابط 40G/100G — BGP — رابط مشبع، أخرى خاملة — ECMP فشل — إنتاجية <50% — 50 رف — مركز بيانات",
            rca_steps=[
                RCAStep(1, "BGP ECMP enabled?", "BGP ECMP مفعل؟", "show ip bgp summary, show bgp", "ECMP enabled", "If no ECMP → no load balance", "Enable BGP ECMP, maximum-paths"),
                RCAStep(2, "40G/100G links up?", "روابط 40G/100G تعمل؟", "show interfaces status | include 40G 100G", "Up 40G/100G", "If down → link", "Check QSFP, fiber, link"),
                RCAStep(3, "Load balancing?", "موازنة حمل؟", "show ip cef, show load-balance", "Load balance per flow", "If no LB → ECMP fail", "Check CEF, load-balance hashing"),
            ],
            possible_causes=[
                "BGP ECMP not enabled — maximum-paths missing — enable BGP ECMP",
                "40G/100G link DOWN — check QSFP, fiber",
                "CEF load balancing not per flow — check CEF, hashing",
            ],
            fix_en="Enable BGP ECMP maximum-paths, verify 40G/100G links up QSFP, CEF load balance per flow. Verify Leaf-Spine ECMP PASS, 40G/100G throughput PASS, load balancing 50/50 PASS — datacenter 50 racks — ULTRA LEGENDARY v4.",
            fix_ar="تفعيل BGP ECMP maximum-paths، تحقق روابط 40G/100G QSFP، CEF موازنة حمل لكل تدفق. تحقق Leaf-Spine ECMP نجاح، إنتاجية 40G/100G نجاح، موازنة 50/50 نجاح — مركز بيانات 50 رف — فائق الأسطورية v4.",
            verification=["BGP ECMP maximum-paths PASS", "40G/100G links up PASS", "CEF load balance per flow PASS", "Leaf-Spine ECMP 50/50 PASS", "Throughput 80Gbps+ PASS"],
        ),
        "vmotion_isolated": TroubleshootingScenario(
            scenario_type=ScenarioType.BRANCH_DOWN,
            title_en="Datacenter — VMOTION VLAN 830 isolated fail — should be isolated no routing — but routing exists — security FAIL — ULTRA LEGENDARY v4",
            title_ar="مركز بيانات — VMOTION VLAN 830 فشل عزل — يجب معزول بدون توجيه — لكن توجيه موجود — أمان فشل — فائق الأسطورية v4",
            symptom_en="VMOTION VLAN 830 should be isolated no routing — but routing to other VLANs exists — security FAIL — vMotion 10G+ — 50 racks — datacenter",
            symptom_ar="VLAN VMOTION 830 يجب معزول بدون توجيه — لكن توجيه ل VLANs أخرى موجود — أمان فشل — vMotion 10G+ — 50 رف — مركز بيانات",
            rca_steps=[
                RCAStep(1, "VMOTION SVI up isolated?", "SVI VMOTION معزول؟", "show ip interface brief Vlan830, show ip route Vlan830", "up up, no route to other VLANs", "If route exists → isolation fail", "Remove route, ACL DENY VMOTION→other VLANs, isolated"),
                RCAStep(2, "VMOTION throughput 10G+?", "إنتاجية VMOTION 10G+؟", "show interfaces status | include 830, check throughput", "10G+", "If 1G → bottleneck", "Check 10G links, QSFP, fiber"),
            ],
            possible_causes=[
                "VMOTION not isolated — route to other VLANs exists — must remove per security — VMOTION isolated 10G+ no routing",
                "VMOTION throughput 1G not 10G+ — needs 10G+ — check 10G links",
            ],
            fix_en="Fix VMOTION isolated — no route to other VLANs, ACL DENY, throughput 10G+. Verify VMOTION isolated PASS no routing, throughput 10G+ PASS, vMotion PASS — datacenter — ULTRA LEGENDARY v4.",
            fix_ar="إصلاح VMOTION معزول — بدون مسار ل VLANs أخرى، ACL منع، إنتاجية 10G+. تحقق VMOTION معزول نجاح بدون توجيه، إنتاجية 10G+ نجاح، vMotion نجاح — مركز بيانات — فائق الأسطورية v4.",
            verification=["VMOTION isolated no routing PASS", "Throughput 10G+ PASS", "vMotion PASS", "Security isolated PASS"],
        ),
        "backup_replication": TroubleshootingScenario(
            scenario_type=ScenarioType.WIFI_SLOW,
            title_en="Datacenter — BACKUP-DC VLAN 820 Veeam replication slow — 100G — throughput <50G — backup FAIL — ULTRA LEGENDARY v4",
            title_ar="مركز بيانات — نسخ احتياطي VLAN 820 Veeam مزامنة بطيئة — 100G — إنتاجية <50G — نسخ احتياطي فشل — فائق الأسطورية v4",
            symptom_en="BACKUP-DC VLAN 820 Veeam replication slow — 100G link — throughput <50G — backup FAIL — 50 racks — Veeam — datacenter",
            symptom_ar="نسخ احتياطي VLAN 820 Veeam مزامنة بطيئة — رابط 100G — إنتاجية <50G — نسخ احتياطي فشل — 50 رف — Veeam — مركز بيانات",
            rca_steps=[
                RCAStep(1, "100G link up?", "رابط 100G يعمل؟", "show interfaces status | include 100G", "Up 100G", "If down → link", "Check QSFP 100G-SR4, fiber SMF"),
                RCAStep(2, "Veeam up?", "Veeam يعمل؟", "ping 10.10.120.10, check Veeam", "Up", "If down → Veeam", "Check Veeam 10.10.120.10, backup storage"),
                RCAStep(3, "Throughput 100G?", "إنتاجية 100G؟", "check Veeam throughput", "100G", "If <50G → bottleneck", "Check storage I/O, network, Veeam config"),
            ],
            possible_causes=[
                "100G link DOWN — check QSFP 100G-SR4, fiber SMF",
                "Veeam 10.10.120.10 DOWN — check Veeam server",
                "Throughput <50G — storage I/O bottleneck — check storage, network",
            ],
            fix_en="Fix 100G link up QSFP 100G-SR4 SMF, Veeam up, throughput 100G. Verify 100G link PASS, Veeam replication 100G PASS, backup PASS — datacenter — ULTRA LEGENDARY v4.",
            fix_ar="إصلاح رابط 100G QSFP 100G-SR4 SMF، Veeam يعمل، إنتاجية 100G. تحقق رابط 100G نجاح، مزامنة Veeam 100G نجاح، نسخ احتياطي نجاح — مركز بيانات — فائق الأسطورية v4.",
            verification=["100G link PASS", "Veeam 10.10.120.10 up PASS", "Throughput 100G PASS Veeam", "Backup PASS"],
        ),
    },
    
    "trading": {
        "erp_unreachable": TroubleshootingScenario(
            scenario_type=ScenarioType.ERP_UNREACHABLE,
            title_en="Trading — ERP unreachable but Internet OK — VLAN 10 — branch cannot reach HQ ERP 10.10.30.20:443 — IPsec WAN HQ hub 10.255.1.0/30 — OSPF Area 0",
            title_ar="تجارة — ERP لا يصل لكن إنترنت يعمل — VLAN 10 — فرع لا يصل ERP HQ 10.10.30.20:443 — IPsec WAN HQ 10.255.1.0/30 — OSPF Area 0",
            symptom_en="Branch employee VLAN 10 10.11.10.x cannot reach HQ ERP 10.10.30.20:443 — but Internet 8.8.8.8 OK — IPsec WAN HQ hub 10.255.1.0/30 — ERP FAIL — OSPF Area 0 — trading HQ 200 2 branches",
            symptom_ar="موظف فرع VLAN 10 10.11.10.x لا يصل ERP HQ 10.10.30.20:443 — لكن إنترنت 8.8.8.8 يعمل — IPsec WAN HQ 10.255.1.0/30 — ERP فشل — OSPF Area 0 — تجارة HQ 200 فرعين",
            rca_steps=[
                RCAStep(1, "IPsec WAN up?", "IPsec WAN يعمل؟", "show crypto ipsec sa, show crypto isakmp sa, ping 10.255.1.1", "Up", "If down → IPsec", "Check IPsec PSK, proposal AES256/SHA256, HQ hub 10.255.1.0/30"),
                RCAStep(2, "ERP server up?", "خادم ERP يعمل؟", "ping 10.10.30.20:443, check ERP01", "Up", "If down → server", "Check ERP01 10.10.30.20:443, VLAN 30"),
                RCAStep(3, "FW BR→HQ policy?", "سياسة جدار فرع→HQ؟", "show firewall policy | include 10.11.10.0 10.10.30.20", "ALLOW BR→HQ ERP 443", "If DENY → FW", "Allow BR 10.11.10.0/24 → HQ ERP 10.10.30.20:443 per policy BR→HQ ALLOW ERP/DNS/AD"),
                RCAStep(4, "OSPF Area 0?", "OSPF Area 0؟", "show ip ospf neighbor, show ip route 10.10.30.20", "OSPF up, route present", "If no route → OSPF", "Check OSPF Area 0, neighbor, route"),
            ],
            possible_causes=[
                "IPsec WAN DOWN — HQ hub 10.255.1.0/30 — PSK, proposal AES256/SHA256 — branch cannot reach HQ",
                "ERP01 10.10.30.20:443 DOWN — check server, VLAN 30, power",
                "FW DENY BR→HQ ERP — must ALLOW 10.11.10.0/24 → 10.10.30.20:443 per policy BR→HQ ALLOW ERP/DNS/AD",
                "OSPF Area 0 DOWN — no route to HQ — check OSPF neighbor, Area 0",
            ],
            fix_en="Fix IPsec WAN up HQ hub 10.255.1.0/30 PSK AES256/SHA256, ERP01 up 10.10.30.20:443, FW ALLOW BR→HQ ERP 443 per policy, OSPF Area 0 up. Verify BR 10.11.10.x → HQ ERP 10.10.30.20:443 PASS, BR→Internet PASS, BR→HQ AD 10.10.30.10 PASS, BR→HQ DNS PASS, BR↔BR DENY PASS, OSPF PASS — trading HQ 200 2 branches — REAL — 40Y expert — ULTRA LEGENDARY v4.",
            fix_ar="إصلاح IPsec WAN HQ 10.255.1.0/30 PSK AES256/SHA256، ERP01 10.10.30.20:443، جدار سماح فرع→HQ ERP 443 حسب سياسة، OSPF Area 0. تحقق فرع 10.11.10.x→HQ ERP 443 نجاح، فرع→إنترنت نجاح، فرع→HQ AD نجاح، فرع→HQ DNS نجاح، فرع↔فرع منع نجاح، OSPF نجاح — تجارة HQ 200 فرعين — حقيقي — 40 عام خبير — فائق الأسطورية v4.",
            verification=["BR 10.11.10.x → HQ ERP 10.10.30.20:443 PASS", "BR → Internet 8.8.8.8 PASS", "BR → HQ AD 10.10.30.10 PASS", "BR → HQ DNS PASS", "BR↔BR DENY PASS", "IPsec up PASS", "OSPF Area 0 PASS"],
        ),
        "file_smb_fail": TroubleshootingScenario(
            scenario_type=ScenarioType.ERP_UNREACHABLE,
            title_en="Trading — FILE SMB fail — VLAN 30 — FILE01 10.10.30.30:445 — branch cannot map drive — AD auth — 28 infra",
            title_ar="تجارة — ملفات SMB فشل — VLAN 30 — FILE01 10.10.30.30:445 — فرع لا يستطيع ربط قرص — مصادقة AD — 28 بنية",
            symptom_en="Branch cannot map FILE01 10.10.30.30 SMB 445 — FILE01 10.10.30.30:445 — AD auth — branch 10.11.10.x → HQ FILE — SMB FAIL — 28 infra Al-Nour",
            symptom_ar="فرع لا يستطيع ربط FILE01 10.10.30.30 SMB 445 — FILE01 10.10.30.30:445 — مصادقة AD — فرع 10.11.10.x→HQ ملفات — SMB فشل — 28 بنية النور",
            rca_steps=[
                RCAStep(1, "FILE01 up?", "FILE01 يعمل؟", "ping 10.10.30.30:445, check FILE01", "Up", "If down → server", "Check FILE01 10.10.30.30 SMB 445"),
                RCAStep(2, "AD auth?", "مصادقة AD؟", "check AD auth 10.10.30.10, show authentication", "Auth", "If fail → AD", "Check AD01 10.10.30.10, AD02 10.10.30.11, user auth"),
                RCAStep(3, "FW BR→HQ FILE?", "جدار فرع→HQ ملفات؟", "show firewall policy | include 445", "ALLOW BR→HQ FILE 445", "If DENY → FW", "Allow BR → HQ FILE 10.10.30.30:445"),
            ],
            possible_causes=[
                "FILE01 10.10.30.30:445 DOWN — check server",
                "AD auth FAIL — AD01 10.10.30.10, AD02 10.10.30.11 — check AD",
                "FW DENY BR→HQ FILE 445 — must ALLOW",
            ],
            fix_en="Fix FILE01 up 10.10.30.30:445, AD auth via AD01/02, FW ALLOW BR→HQ FILE 445. Verify BR→FILE PASS, AD auth PASS, SMB mapping PASS — trading — REAL — 28 infra — ULTRA LEGENDARY v4.",
            fix_ar="إصلاح FILE01 10.10.30.30:445، مصادقة AD عبر AD01/02، جدار سماح فرع→HQ ملفات 445. تحقق فرع→ملفات نجاح، AD نجاح، ربط SMB نجاح — تجارة — حقيقي — 28 بنية — فائق الأسطورية v4.",
            verification=["BR 10.11.10.x → FILE01 10.10.30.30:445 SMB PASS", "AD auth PASS", "SMB mapping PASS", "File access PASS"],
        ),
        "voip_qos": TroubleshootingScenario(
            scenario_type=ScenarioType.WIFI_SLOW,
            title_en="Trading — VOIP QoS fail — VLAN 20 — DSCP EF — PoE — call quality FAIL — jitter >20ms — 100 phones — CUCM 10.10.30.40",
            title_ar="تجارة — VOIP QoS فشل — VLAN 20 — DSCP EF — PoE — جودة مكالمة فشل — تذبذب >20ms — 100 هاتف — CUCM 10.10.30.40",
            symptom_en="VOIP VLAN 20 call quality FAIL — jitter >20ms — DSCP EF — PoE — 100 phones — QoS not priority — voice FAIL — CUCM — Al-Nour Trading HQ 180",
            symptom_ar="جودة مكالمة VOIP VLAN 20 فشل — تذبذب >20ms — DSCP EF — PoE — 100 هاتف — QoS ليس أولوية — صوت فشل — CUCM — النور تجارة HQ 180",
            rca_steps=[
                RCAStep(1, "VOIP SVI up PoE?", "SVI VOIP PoE؟", "show ip interface brief Vlan20, show power inline", "up up, PoE up", "If down → SVI, PoE", "no shutdown Vlan20, power inline"),
                RCAStep(2, "QoS DSCP EF priority?", "QoS DSCP EF أولوية؟", "show mls qos, show policy-map VOIP", "Priority EF for VLAN 20", "If no QoS → jitter", "Enable QoS priority DSCP EF for VOIP VLAN 20"),
                RCAStep(3, "CUCM up?", "CUCM يعمل؟", "ping 10.10.30.40, check CUCM", "Up", "If down → CUCM", "Check CUCM 10.10.30.40, VOIP gateway"),
            ],
            possible_causes=[
                "VOIP SVI DOWN or PoE DOWN — check SVI, PoE budget",
                "No QoS DSCP EF priority — voice needs priority — enable QoS EF",
                "CUCM 10.10.30.40 DOWN — check CUCM server",
            ],
            fix_en="Fix VOIP SVI up PoE, QoS DSCP EF priority for VLAN 20, CUCM up. Verify VOIP QoS EF PASS, jitter <10ms PASS, call quality PASS, 100 phones PASS — trading HQ 180 — REAL — 40Y expert — ULTRA LEGENDARY v4.",
            fix_ar="إصلاح SVI VOIP PoE، QoS DSCP EF أولوية VLAN 20، CUCM يعمل. تحقق VOIP QoS EF نجاح، تذبذب <10ms نجاح، جودة مكالمة نجاح، 100 هاتف نجاح — تجارة HQ 180 — حقيقي — 40 عام خبير — فائق الأسطورية v4.",
            verification=["VOIP VLAN 20 DSCP EF PASS", "Jitter <10ms PASS", "Call quality PASS MOS 4.2+", "PoE 100 phones PASS", "CUCM 10.10.30.40 PASS"],
        ),
        "guest_internet_only": TroubleshootingScenario(
            scenario_type=ScenarioType.ERP_UNREACHABLE,
            title_en="Trading — GUEST VLAN 80 Internet only — cannot reach internal — by design — but cannot reach Internet — NAT — 50 guests — Al-Nour",
            title_ar="تجارة — VLAN ضيوف 80 إنترنت فقط — لا يصل داخلي — تصميم — لكن لا يصل إنترنت — NAT — 50 ضيف — النور",
            symptom_en="GUEST VLAN 80 cannot reach Internet — should be Internet only no internal — but Internet FAIL — NAT, FW — 50 guests — trading HQ 180 Al-Nour",
            symptom_ar="VLAN ضيوف 80 لا يصل إنترنت — يجب إنترنت فقط بدون داخلي — لكن إنترنت فشل — NAT، جدار — 50 ضيف — تجارة HQ 180 النور",
            rca_steps=[
                RCAStep(1, "GUEST SVI up?", "SVI ضيوف؟", "show ip interface brief Vlan80", "up up", "If down → SVI", "no shutdown Vlan80"),
                RCAStep(2, "NAT Internet?", "NAT إنترنت؟", "show ip nat translations | include 80, ping 8.8.8.8 source Vlan80", "NAT up", "If no NAT → Internet fail", "Check NAT overload, FW GUEST→Internet ALLOW"),
                RCAStep(3, "Internal BLOCK?", "داخلي ممنوع؟", "ping 10.10.0.1 source Vlan80", "BLOCK", "If ALLOW → security fail", "Fix ACL DENY GUEST→Internal, ALLOW Internet only"),
            ],
            possible_causes=[
                "GUEST SVI DOWN",
                "NAT fail — no Internet — check NAT overload, FW ALLOW GUEST→Internet",
                "Internal not BLOCKED — security FAIL — must DENY GUEST→Internal",
            ],
            fix_en="Fix GUEST SVI up, NAT overload, FW ALLOW GUEST→Internet, DENY Internal. Verify GUEST→Internet PASS, GUEST→Internal BLOCK, 50 guests PASS — trading HQ 180 Al-Nour — REAL — ULTRA LEGENDARY v4.",
            fix_ar="إصلاح SVI ضيوف، NAT، جدار سماح ضيوف→إنترنت، منع داخلي. تحقق ضيوف→إنترنت نجاح، ضيوف→داخلي منع، 50 ضيف نجاح — تجارة HQ 180 النور — حقيقي — فائق الأسطورية v4.",
            verification=["GUEST 10.x.80.x → Internet PASS", "GUEST → Internal BLOCK PASS", "50 guests PASS", "NAT PASS"],
        ),
    },
    "office": {
        "voip_qos": TroubleshootingScenario(
            scenario_type=ScenarioType.WIFI_SLOW,
            title_en="Office — VOIP QoS fail — VLAN 20 — DSCP EF — PoE — call quality FAIL — jitter >20ms — 100 phones — CUCM 10.10.30.40 — ULTRA LEGENDARY v4",
            title_ar="مكتب — VOIP QoS فشل — VLAN 20 — DSCP EF — PoE — جودة مكالمة فشل — تذبذب >20ms — 100 هاتف — CUCM 10.10.30.40 — فائق الأسطورية v4",
            symptom_en="VOIP VLAN 20 call quality FAIL — jitter >20ms — DSCP EF — PoE — 100 phones — QoS not priority — voice FAIL — CUCM 10.10.30.40 — office HQ 100",
            symptom_ar="جودة مكالمة VOIP VLAN 20 فشل — تذبذب >20ms — DSCP EF — PoE — 100 هاتف — QoS ليس أولوية — صوت فشل — CUCM 10.10.30.40 — مكتب HQ 100",
            rca_steps=[
                RCAStep(1, "VOIP SVI up PoE?", "SVI VOIP PoE؟", "show ip interface brief Vlan20, show power inline", "up up, PoE up", "If down → SVI, PoE", "no shutdown Vlan20, power inline"),
                RCAStep(2, "QoS DSCP EF priority?", "QoS DSCP EF أولوية؟", "show mls qos, show policy-map VOIP", "Priority EF for VLAN 20", "If no QoS → jitter", "Enable QoS priority DSCP EF for VOIP VLAN 20"),
                RCAStep(3, "CUCM up?", "CUCM يعمل؟", "ping 10.10.30.40, check CUCM", "Up", "If down → CUCM", "Check CUCM 10.10.30.40, VOIP gateway"),
            ],
            possible_causes=[
                "VOIP SVI DOWN or PoE DOWN — check SVI, PoE budget",
                "No QoS DSCP EF priority — voice needs priority — enable QoS EF",
                "CUCM 10.10.30.40 DOWN — check CUCM server",
            ],
            fix_en="Fix VOIP SVI up PoE, QoS DSCP EF priority for VLAN 20, CUCM up. Verify VOIP QoS EF PASS, jitter <10ms PASS, call quality PASS, 100 phones PASS — office HQ 100 — REAL — 40Y expert — ULTRA LEGENDARY v4 — world-class professional.",
            fix_ar="إصلاح SVI VOIP PoE، QoS DSCP EF أولوية VLAN 20، CUCM يعمل. تحقق VOIP QoS EF نجاح، تذبذب <10ms نجاح، جودة مكالمة نجاح، 100 هاتف نجاح — مكتب HQ 100 — حقيقي — 40 عام خبير — فائق الأسطورية v4 — احترافي عالمي.",
            verification=["VOIP VLAN 20 DSCP EF PASS", "Jitter <10ms PASS", "Call quality PASS MOS 4.2+", "PoE 100 phones PASS", "CUCM 10.10.30.40 PASS"],
        ),
        "guest_internet_only": TroubleshootingScenario(
            scenario_type=ScenarioType.ERP_UNREACHABLE,
            title_en="Office — GUEST VLAN 80 Internet only — cannot reach internal — by design — but cannot reach Internet — NAT — 50 guests — ULTRA LEGENDARY v4",
            title_ar="مكتب — VLAN ضيوف 80 إنترنت فقط — لا يصل داخلي — تصميم — لكن لا يصل إنترنت — NAT — 50 ضيف — فائق الأسطورية v4",
            symptom_en="GUEST VLAN 80 cannot reach Internet — should be Internet only no internal — but Internet FAIL — NAT, FW — 50 guests — office HQ 100",
            symptom_ar="VLAN ضيوف 80 لا يصل إنترنت — يجب إنترنت فقط بدون داخلي — لكن إنترنت فشل — NAT، جدار — 50 ضيف — مكتب HQ 100",
            rca_steps=[
                RCAStep(1, "GUEST SVI up?", "SVI ضيوف؟", "show ip interface brief Vlan80", "up up", "If down → SVI", "no shutdown Vlan80"),
                RCAStep(2, "NAT Internet?", "NAT إنترنت؟", "show ip nat translations | include 80, ping 8.8.8.8 source Vlan80", "NAT up", "If no NAT → Internet fail", "Check NAT overload, FW GUEST→Internet ALLOW"),
                RCAStep(3, "Internal BLOCK?", "داخلي ممنوع؟", "ping 10.10.0.1 source Vlan80", "BLOCK", "If ALLOW → security fail", "Fix ACL DENY GUEST→Internal, ALLOW Internet only"),
            ],
            possible_causes=[
                "GUEST SVI DOWN",
                "NAT fail — no Internet — check NAT overload, FW ALLOW GUEST→Internet",
                "Internal not BLOCKED — security FAIL — must DENY GUEST→Internal",
            ],
            fix_en="Fix GUEST SVI up, NAT overload, FW ALLOW GUEST→Internet, DENY Internal. Verify GUEST→Internet PASS, GUEST→Internal BLOCK, 50 guests PASS — office HQ 100 — REAL — ULTRA LEGENDARY v4.",
            fix_ar="إصلاح SVI ضيوف، NAT، جدار سماح ضيوف→إنترنت، منع داخلي. تحقق ضيوف→إنترنت نجاح، ضيوف→داخلي منع، 50 ضيف نجاح — مكتب HQ 100 — حقيقي — فائق الأسطورية v4.",
            verification=["GUEST 10.x.80.x → Internet PASS", "GUEST → Internal BLOCK PASS", "50 guests PASS", "NAT PASS"],
        ),
        "cctv_isolated": TroubleshootingScenario(
            scenario_type=ScenarioType.ERP_UNREACHABLE,
            title_en="Office — CCTV VLAN 60 isolated — cannot reach users — by design — but NVR unreachable — 42 CCTV — ULTRA LEGENDARY v4",
            title_ar="مكتب — VLAN كاميرات 60 معزول — لا يصل مستخدمين — تصميم — لكن NVR لا يصل — 42 كاميرا — فائق الأسطورية v4",
            symptom_en="CCTV VLAN 60 isolated — cannot reach users by design — but NVR 10.10.30.32 unreachable — 42 CCTV cameras — office HQ 100 — security — Al-Nour 42 CCTV",
            symptom_ar="VLAN كاميرات 60 معزول — لا يصل مستخدمين تصميم — لكن NVR 10.10.30.32 لا يصل — 42 كاميرا — مكتب HQ 100 — أمان — النور 42 كاميرا",
            rca_steps=[
                RCAStep(1, "CCTV SVI up?", "SVI كاميرات؟", "show ip interface brief Vlan60", "up up", "If down → SVI", "no shutdown Vlan60"),
                RCAStep(2, "NVR up?", "NVR يعمل؟", "ping 10.10.30.32, check NVR", "Up", "If down → NVR", "Check NVR 10.10.30.32, storage"),
                RCAStep(3, "ACL CCTV→NVR?", "ACL كاميرات→NVR؟", "show access-lists ACL_VLAN60_IN", "ALLOW CCTV→NVR 554 8000", "If DENY → ACL", "Allow CCTV 10.x.60.x → NVR 10.10.30.32:554,8000"),
            ],
            possible_causes=[
                "CCTV SVI DOWN",
                "NVR 10.10.30.32 DOWN — check NVR, storage",
                "ACL blocking CCTV→NVR — must ALLOW 554 RTSP, 8000",
            ],
            fix_en="Fix CCTV SVI up, NVR up, ACL ALLOW CCTV→NVR 554 8000. Verify CCTV→NVR PASS, CCTV→Users BLOCK, 42 CCTV PASS — office HQ 100 Al-Nour 42 CCTV — REAL — ULTRA LEGENDARY v4.",
            fix_ar="إصلاح SVI كاميرات، NVR، ACL سماح كاميرات→NVR 554 8000. تحقق كاميرات→NVR نجاح، كاميرات→مستخدمين منع، 42 كاميرا نجاح — مكتب HQ 100 النور 42 كاميرا — حقيقي — فائق الأسطورية v4.",
            verification=["CCTV 10.x.60.x → NVR 10.10.30.32:554 PASS", "CCTV → Users BLOCK PASS", "42 CCTV PASS", "NVR storage PASS"],
        ),
        "wifi_corp": TroubleshootingScenario(
            scenario_type=ScenarioType.WIFI_SLOW,
            title_en="Office — CORP-WIFI VLAN 70 slow — 21 APs — WLC 10.10.30.33 — 802.1X — per-user 5Mbps — 100 users WiFi — ULTRA LEGENDARY v4",
            title_ar="مكتب — واي فاي شركات VLAN 70 بطيء — 21 APs — WLC 10.10.30.33 — 802.1X — 5Mbps لكل مستخدم — 100 مستخدم واي فاي — فائق الأسطورية v4",
            symptom_en="CORP-WIFI VLAN 70 slow — 21 APs — WLC 10.10.30.33 — 802.1X auth — per-user 5Mbps — 100 users WiFi — slow — office HQ 100 Al-Nour 21 APs",
            symptom_ar="واي فاي شركات VLAN 70 بطيء — 21 APs — WLC 10.10.30.33 — 802.1X مصادقة — 5Mbps لكل مستخدم — 100 مستخدم واي فاي — بطيء — مكتب HQ 100 النور 21 APs",
            rca_steps=[
                RCAStep(1, "WLC up?", "WLC يعمل؟", "ping 10.10.30.33, check WLC", "Up", "If down → WLC", "Check WLC 10.10.30.33"),
                RCAStep(2, "APs up?", "APs تعمل؟", "show ap summary, show ap uptime", "21 APs up", "If down → APs", "Check 21 APs, PoE, WLC join"),
                RCAStep(3, "802.1X auth?", "802.1X مصادقة؟", "show dot1x, show authentication sessions", "Auth", "If fail → RADIUS", "Check RADIUS 10.10.30.10, AD, 802.1X"),
                RCAStep(4, "Per-user QoS 5M?", "QoS 5M لكل مستخدم؟", "show qos, show policy-map WIFI", "5Mbps per user", "If no QoS → slow", "Enable QoS per-user 5M for CORP-WIFI"),
            ],
            possible_causes=[
                "WLC 10.10.30.33 DOWN — check WLC",
                "APs DOWN — 21 APs — check PoE, WLC join, AP power",
                "802.1X FAIL — RADIUS 10.10.30.10 — check RADIUS, AD",
                "No per-user QoS — 100 users saturate — enable 5M per user",
            ],
            fix_en="Fix WLC up, 21 APs up PoE, 802.1X auth RADIUS AD, per-user QoS 5M. Verify CORP-WIFI 21 APs up, 802.1X PASS, per-user 5M PASS, 100 users PASS — office HQ 100 Al-Nour 21 APs — REAL — 40Y expert — ULTRA LEGENDARY v4 — world-class professional.",
            fix_ar="إصلاح WLC، 21 APs PoE، 802.1X RADIUS AD، QoS 5M لكل مستخدم. تحقق واي فاي شركات 21 APs، 802.1X نجاح، 5M لكل مستخدم نجاح، 100 مستخدم نجاح — مكتب HQ 100 النور 21 APs — حقيقي — 40 عام خبير — فائق الأسطورية v4 — احترافي عالمي.",
            verification=["WLC 10.10.30.33 up PASS", "21 APs up PASS PoE", "802.1X auth PASS RADIUS AD", "Per-user 5Mbps PASS", "100 WiFi users PASS"],
        ),
    },

}

def get_scenarios_for_institution(institution_type: str) -> List[TroubleshootingScenario]:
    """Get all scenarios for institution type — WORLD-CLASS — 40Y expert — ULTRA LEGENDARY v3"""
    base = list(SCENARIOS.values())
    extra = INSTITUTION_SCENARIOS.get(institution_type, {})
    return base + list(extra.values())

def get_all_generic_scenarios() -> Dict[str, List[TroubleshootingScenario]]:
    """Get scenarios grouped by institution type — ULTRA LEGENDARY v3"""
    result = {}
    for inst_type in ["hospital", "factory", "bank", "hotel", "datacenter", "school", "retail", "government", "trading", "office"]:
        result[inst_type] = get_scenarios_for_institution(inst_type)
    return result
