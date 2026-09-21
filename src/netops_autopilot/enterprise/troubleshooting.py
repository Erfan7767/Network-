"""
Enterprise Troubleshooting — Real Scenarios — RCA like 40Y Expert — WORLD-CLASS PROFESSIONAL

Scenarios from Al-Nour doc:
- BR02 can't reach ERP but Internet works
- Wi-Fi slow BR03
- Wrong VLAN BR01 10.11.10.x gets 10.11.80.x
- BR03 full DOWN
- Guest isolation
- Normal user acceptance
- ISP failure, WAN failure, CORE failure, FW failure

No random config changes — evidence before change — microscopic precision.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum

class ScenarioType(str, Enum):
    ERP_UNREACHABLE = "erp_unreachable"
    WIFI_SLOW = "wifi_slow"
    WRONG_VLAN = "wrong_vlan"
    BRANCH_DOWN = "branch_down"
    GUEST_ISOLATION_FAIL = "guest_isolation_fail"
    INTERNET_DOWN = "internet_down"
    WAN_DOWN = "wan_down"
    CORE_DOWN = "core_down"
    FW_DOWN = "fw_down"
    DHCP_FAIL = "dhcp_fail"
    DNS_FAIL = "dns_fail"
    VOIP_FAIL = "voip_fail"
    CCTV_FAIL = "cctv_fail"

@dataclass
class RCAStep:
    order: int
    check: str
    check_ar: str
    command: str
    expected: str
    evidence: str
    if_fail: str

@dataclass
class TroubleshootingScenario:
    scenario_type: ScenarioType
    title_en: str
    title_ar: str
    symptom_en: str
    symptom_ar: str
    rca_steps: List[RCAStep]
    possible_causes: List[str]
    fix_en: str
    fix_ar: str
    verification: List[str]
    is_security: bool = False

SCENARIOS: Dict[ScenarioType, TroubleshootingScenario] = {
    ScenarioType.ERP_UNREACHABLE: TroubleshootingScenario(
        scenario_type=ScenarioType.ERP_UNREACHABLE,
        title_en="Branch 2 — Users can't reach ERP, but Internet works",
        title_ar="الفرع 2 — الموظفون لا يصلون ERP لكن الإنترنت يعمل",
        symptom_en="Employees in Branch 2 report: Internet OK, ERP at HQ 10.10.30.20:443 FAIL",
        symptom_ar="موظفو الفرع 2: الإنترنت يعمل، ERP في المقر 10.10.30.20:443 لا يعمل",
        rca_steps=[
            RCAStep(1, "PC IP?", "IP الحاسوب؟", "ipconfig /all or ip addr", "10.12.10.x/24 gw 10.12.10.1", "If not in 10.12.10.0/24 → VLAN/DHCP issue", "Check VLAN/access port"),
            RCAStep(2, "Gateway reachable?", "البوابة قابلة للوصول؟", "ping 10.12.10.1", "Reply", "If fail → L2 issue, trunk, SVI", "Check trunk, SVI, L2"),
            RCAStep(3, "DNS?", "DNS؟", "nslookup erp.alnour.local 10.10.30.10", "10.10.30.20", "If fail → DNS, FW policy DNS 53", "Check DNS server, FW"),
            RCAStep(4, "Route to HQ?", "المسار إلى المقر؟", "show ip route 10.10.30.0 or traceroute 10.10.30.20", "via IPsec 10.255.2.0/30", "If no route → OSPF, IPsec", "Check OSPF, IPsec tunnel"),
            RCAStep(5, "WAN up?", "الشبكة الواسعة تعمل؟", "show crypto ipsec sa or ping HQ FW", "IPsec SA up", "If down → ISP, FW, tunnel", "Check ISP, FW, IPsec phase1/2"),
            RCAStep(6, "VPN/Overlay up?", "VPN يعمل؟", "show vpn ipsec phase1/phase2", "Up", "If down → PSK, proposal, GW", "Check PSK AlNourIPsec2024!, proposal aes256-sha256"),
            RCAStep(7, "Firewall policy?", "سياسة الجدار؟", "show firewall policy or FW logs", "BR01 USERS→HQ SERVERS ALLOW 443", "If DENY → FW policy", "Add/allow policy 100 BR Vlan10→IPsec-HQ dst 10.10.30.0/24 ALLOW"),
            RCAStep(8, "ERP port open?", "منفذ ERP مفتوح؟", "telnet 10.10.30.20 443 or nc -zv 10.10.30.20 443", "Open", "If closed → ERP service, FW HQ", "Check ERP01 service, HQ FW policy"),
            RCAStep(9, "Server up?", "الخادم يعمل؟", "ping 10.10.30.20, check server", "Up", "If down → server, VLAN 30", "Check ERP01 10.10.30.20, VLAN 30 SVI"),
            RCAStep(10, "Application?", "التطبيق؟", "curl https://10.10.30.20 or browser", "ERP login page", "If fail → ERP app, AD auth", "Check ERP service, AD01/02, DB"),
        ],
        possible_causes=[
            "FW policy DENY BR→HQ ERP — most common — check FW-BR02-01 policy 100",
            "IPsec tunnel DOWN — ISP, FW, PSK mismatch, proposal mismatch",
            "OSPF route missing — no route to 10.10.30.0/24 via IPsec",
            "DNS failure — erp.alnour.local not resolving to 10.10.30.20",
            "HQ FW DENY — BR subnet not allowed to SERVERS VLAN 30",
            "ERP service DOWN — ERP01 10.10.30.20 service stopped",
            "AD auth FAIL — AD01/02 down, user not authenticated",
        ],
        fix_en="Fix FW policy: config firewall policy edit 100 set srcintf Vlan10 set dstintf IPsec-HQ set dstaddr 10.10.30.0/24 set service HTTPS set action accept. Verify: BR02 PC → ERP PASS. Log in ledger.",
        fix_ar="إصلاح سياسة الجدار الناري: السماح من VLAN 10 في الفرع إلى شبكة الخوادم 10.10.30.0/24 عبر IPsec للخدمة HTTPS. تحقق: حاسوب الفرع 2 → ERP نجاح.",
        verification=["BR02 User 10.12.10.100 → HQ ERP 10.10.30.20:443 PASS", "BR02 User → HQ File 10.10.30.21 SMB PASS", "BR02 Guest → HQ ERP BLOCK (security)", "NMS shows BR02→HQ latency OK", "Ledger logged"],
    ),
    ScenarioType.WIFI_SLOW: TroubleshootingScenario(
        scenario_type=ScenarioType.WIFI_SLOW,
        title_en="Branch 3 — Wi-Fi connected but speed is poor",
        title_ar="الفرع 3 — الواي فاي متصل لكن السرعة سيئة",
        symptom_en="Users in Branch 3: Wi-Fi connected Company-Corp VLAN 70 but speed poor, not Internet assumed slow",
        symptom_ar="مستخدمو الفرع 3: واي فاي متصل لكن السرعة سيئة، لا أستنتج مباشرة أن الإنترنت بطيء",
        rca_steps=[
            RCAStep(1, "Client?", "العميل؟", "Check client Wi-Fi adapter, driver", "802.11ac/ax, driver up to date", "Old driver, 802.11b", "Update driver, check adapter"),
            RCAStep(2, "RSSI?", "قوة الإشارة؟", "Check RSSI on client: -30 to -67 dBm good, -70+ poor", "-50 dBm good", "RSSI -80 → far from AP, obstruction", "Move closer, add AP, check AP placement"),
            RCAStep(3, "SNR?", "نسبة الإشارة للضوضاء؟", "SNR = RSSI - Noise floor, >25 dB good, <20 poor", ">25 dB", "SNR 15 → interference, noise", "Check interference, channel"),
            RCAStep(4, "Channel Utilization?", "استخدام القناة؟", "WLC: show ap channel or NMS AP dashboard", "<70% good, >80% congested", "Util 90% → co-channel interference, many clients", "Change channel, add AP, load balance"),
            RCAStep(5, "AP Uplink?", "وصلة نقطة الواي فاي؟", "Check AP switch port Gi1/0/37-40 trunk 40/70/80 status", "1G full, no errors", "100M, half, CRC → L1/L2", "Check cable Cat6A, port config, PoE"),
            RCAStep(6, "Switch?", "السويتش؟", "Check SW-BR03-01 CPU, memory, errors", "CPU <50%, no errors", "CPU 90% → broadcast storm, loop", "Check STP, loops, broadcast"),
            RCAStep(7, "WAN?", "الشبكة الواسعة؟", "Check WAN latency HQ↔BR03 ping, IPsec", "<50ms good, >100ms poor", "Latency 200ms → ISP, congestion", "Check ISP, QoS, bandwidth"),
            RCAStep(8, "Internet?", "الإنترنت؟", "Speedtest from BR03 FW, not client", "ISP speed per contract", "Speed low → ISP, FW policy, NAT", "Check ISP, FW sessions, NAT, bandwidth"),
        ],
        possible_causes=[
            "Channel congestion — many APs same channel, co-channel interference — change channel via WLC",
            "RSSI low — client far from AP, obstruction, AP placement poor — move/add AP",
            "AP uplink 100M/half/CRC — cable Cat5, bad crimp, port misconfig — replace Cat6A, check trunk",
            "Switch CPU high — broadcast storm, STP loop — check STP, find loop",
            "WAN latency high — ISP congestion, IPsec overhead — check ISP, QoS for voice vs data",
            "Client old — 802.11b/g, old driver — update, use 5GHz",
            "Too many clients per AP — BR03 has 2 APs for 30 users+15 phones=45 devices — may need 3rd AP",
        ],
        fix_en="WLC: change channel for APs in BR03 to non-overlapping (1,6,11 2.4GHz, 36,40,44 5GHz), check RSSI >-67 dBm, SNR >25 dB, channel util <70%, AP uplink 1G full no CRC, switch CPU OK, WAN latency <100ms. Add AP if needed. Verify speedtest from client.",
        fix_ar="متحكم الواي فاي: تغيير القناة لنقاط الفرع 3 لقنوات غير متداخلة، فحص RSSI >-67، SNR >25، استخدام قناة <70%، وصلة نقطة 1G بدون أخطاء، معالج سويتش سليم، زمن شبكة واسعة <100ms. إضافة نقطة إذا لزم.",
        verification=["Client RSSI -50 dBm PASS", "SNR 30 dB PASS", "Channel util 50% PASS", "AP uplink 1G full 0 CRC PASS", "Speedtest client >50Mbps PASS", "NMS AP dashboard green"],
    ),
    ScenarioType.WRONG_VLAN: TroubleshootingScenario(
        scenario_type=ScenarioType.WRONG_VLAN,
        title_en="Branch 1 — Employee should be 10.11.10.x but gets 10.11.80.x",
        title_ar="الفرع 1 — موظف يجب أن يكون 10.11.10.x لكنه يحصل 10.11.80.x",
        symptom_en="Employee in BR01: expected VLAN 10 USERS 10.11.10.x but gets VLAN 80 GUEST 10.11.80.x — possible Access VLAN, Trunk, DHCP, DHCP Relay, Policy issue — check evidence before change",
        symptom_ar="موظف في الفرع 1: يجب أن يكون 10.11.10.x لكنه يحصل 10.11.80.x — مشكلة محتملة في VLAN وصول، ترانك، DHCP، مرحل DHCP، سياسة — تحقق بالأدلة قبل التغيير",
        rca_steps=[
            RCAStep(1, "Access VLAN?", "VLAN وصول؟", "show vlan brief, show interfaces Gi1/0/10 switchport", "access vlan 10", "If vlan 80 → port misconfigured", "Fix switchport access vlan 10"),
            RCAStep(2, "Trunk allowed?", "الترانك مسموح؟", "show interfaces trunk, show interfaces Gi1/1/1 trunk", "allowed 10,20,40,50,60,70,80", "If VLAN 10 not allowed → trunk prune", "Add vlan 10 to trunk allowed"),
            RCAStep(3, "DHCP scope?", "مجال DHCP؟", "Check DHCP server 10.10.30.10 scope 10.11.10.0/24 and 10.11.80.0/24", "Both scopes exist", "If 10.11.10.0 scope missing → clients get wrong pool", "Create scope 10.11.10.0/24 gw 10.11.10.1 DNS 10.10.30.10"),
            RCAStep(4, "DHCP Relay?", "مرحل DHCP؟", "show ip helper-address on SVI Vlan10", "helper 10.10.30.10 and .11", "If no helper → broadcast not relayed to HQ DHCP", "Add ip helper-address 10.10.30.10 on Vlan10 SVI"),
            RCAStep(5, "Policy / 802.1X?", "سياسة / 802.1X؟", "Check 802.1X, RADIUS, policy maps", "Pass — authenticated", "If 802.1X FAIL → guest VLAN assignment", "Check RADIUS AD01/02, certificate, user auth"),
            RCAStep(6, "Client?", "العميل؟", "Check client previous VLAN cache, release/renew", "ipconfig /release /renew", "If cached → old lease", "Release/renew, clear cache"),
        ],
        possible_causes=[
            "Access port VLAN misconfigured — Gi1/0/10 set to VLAN 80 instead of 10 — fix access vlan 10",
            "Trunk not allowing VLAN 10 — uplink trunk pruned VLAN 10 — add to allowed",
            "DHCP scope 10.11.10.0/24 missing on DHCP server 10.10.30.10 — create scope",
            "DHCP Relay missing — SVI Vlan10 no ip helper-address → broadcast not reaching HQ — add helper",
            "802.1X failure — RADIUS timeout → assigned to guest VLAN 80 — check RADIUS, AD, cert",
            "Client cached old lease — release/renew",
        ],
        fix_en="Check Gi1/0/10 switchport access vlan 10, trunk allowed vlan includes 10, DHCP scope 10.11.10.0/24 exists on 10.10.30.10, ip helper-address on Vlan10 SVI, 802.1X/RADIUS OK. Fix: switchport access vlan 10, add vlan to trunk, create DHCP scope, add helper. Verify: client gets 10.11.10.x PASS.",
        fix_ar="فحص منفذ Gi1/0/10 VLAN 10، ترانك يسمح 10، مجال DHCP 10.11.10.0/24 موجود، مرحل DHCP على واجهة VLAN 10، 802.1X سليم. إصلاح: منفذ وصول VLAN 10، إضافة VLAN للترانك، إنشاء مجال DHCP، إضافة مرحل. تحقق: عميل يحصل 10.11.10.x نجاح.",
        verification=["Gi1/0/10 access vlan 10 PASS", "Trunk allowed includes 10 PASS", "DHCP scope 10.11.10.0/24 exists PASS", "ip helper-address on Vlan10 PASS", "Client 10.11.10.100 gw 10.11.10.1 DNS 10.10.30.10 PASS", "ERP reachable PASS"],
    ),
    ScenarioType.BRANCH_DOWN: TroubleshootingScenario(
        scenario_type=ScenarioType.BRANCH_DOWN,
        title_en="Branch 3 — Entire branch DOWN — NMS shows DOWN",
        title_ar="الفرع 3 — الفرع كامل ساقط — NMS يظهر ساقط",
        symptom_en="NMS NMS01 10.10.30.30 shows BR03 DOWN — check centrally ISP, WAN, FW, Tunnel, Router, Switch then site visit if needed — not assume ISP only",
        symptom_ar="NMS يظهر فرع 3 ساقط — أفحص مركزيا مزود، شبكة واسعة، جدار، نفق، راوتر، سويتش ثم زيارة موقع عند الحاجة — لا أفترض مزود فقط",
        rca_steps=[
            RCAStep(1, "ISP?", "المزود؟", "Ping BR03 FW public IP from HQ, check EDGE logs", "Reply, no loss", "If fail → ISP down, EDGE, FW wan1", "Check ISP ONT, EDGE, FW wan1 interface, cable"),
            RCAStep(2, "WAN?", "الشبكة الواسعة؟", "Check IPsec tunnel HQ↔BR03 10.255.3.0/30 status", "IPsec SA up", "If down → ISP, FW, PSK, proposal", "Check IPsec phase1/2, PSK, proposal, FW logs"),
            RCAStep(3, "Firewall?", "الجدار الناري؟", "Check FW-BR03-01 status via NMS, CPU, memory, uptime", "Up, CPU <50%", "If down → power, UPS, hardware", "Check power, UPS, console, hardware"),
            RCAStep(4, "Tunnel?", "النفق؟", "show crypto ipsec sa, show vpn ipsec phase1/2", "Up", "If down → FW config, ISP", "Check FW IPsec config, ISP"),
            RCAStep(5, "Router?", "الراوتر؟", "Check CORE-01/02 routing to 10.13.0.0/16 via IPsec", "Route via IPsec 10.255.3.0/30", "If no route → OSPF, IPsec", "Check OSPF, IPsec, CORE routing"),
            RCAStep(6, "Switch?", "السويتش؟", "Check SW-BR03-01/02 via FW if FW up, else site visit", "Up", "If down → power, stacking, L1", "Site visit: check Rack, Power, UPS, Grounding, Cabling, Patch Panel"),
            RCAStep(7, "Site visit?", "زيارة موقع؟", "If central checks fail → site visit BR03", "Rack, Power, UPS, ISP, Cabling OK", "If power down → UPS, PDU, mains", "Check power, UPS, PDU, mains, grounding"),
        ],
        possible_causes=[
            "ISP down — BR03 ISP ONT down, fiber cut, EDGE down — check ISP, EDGE, ONT, fiber",
            "FW-BR03-01 down — power, UPS, hardware failure — check power, UPS, console",
            "IPsec tunnel down — PSK mismatch, proposal mismatch, FW policy, ISP — check IPsec",
            "CORE routing missing — OSPF not advertising 10.13.0.0/16 — check OSPF, CORE",
            "Power outage — UPS failed, PDU, mains — check power, UPS, PDU",
            "Switches down — SW-BR03-01/02 power, stacking — check switches",
            "Cable cut — fiber, Cat6A — check cable schedule, OTDR",
        ],
        fix_en="Central: ping BR03 FW public IP, check IPsec SA 10.255.3.0/30, check FW-BR03-01 via NMS, check CORE routing to 10.13.0.0/16. If FW down → site visit: check Rack, Power, UPS, Grounding, ISP, Cabling, Patch Panel, FW/Switches/APs/UPS. Fix root cause (ISP, power, FW, IPsec). Verify: BR03 up, NMS green, BR03→HQ ERP PASS, Internet PASS.",
        fix_ar="مركزيا: ping جدار فرع 3 العام، فحص IPsec 10.255.3.0/30، فحص جدار فرع 3 عبر NMS، فحص توجيه أساسي إلى 10.13.0.0/16. إذا الجدار ساقط → زيارة موقع: فحص راك، طاقة، UPS، تأريض، مزود، كابلات، لوحة، جدار/سويتشات/نقاط/UPS. إصلاح سبب جذري. تحقق: فرع 3 يعمل، NMS أخضر، فرع 3→مقر ERP نجاح.",
        verification=["BR03 FW ping PASS", "IPsec SA up PASS", "FW-BR03-01 up PASS", "SW-BR03-01/02 up PASS", "BR03→HQ ERP PASS", "BR03→Internet PASS", "NMS BR03 green", "Ledger logged"],
    ),
}

def get_scenario(scenario_type: ScenarioType) -> Optional[TroubleshootingScenario]:
    return SCENARIOS.get(scenario_type)

def get_all_scenarios() -> List[TroubleshootingScenario]:
    return list(SCENARIOS.values())

def rca_for_symptom(symptom: str) -> Optional[TroubleshootingScenario]:
    s = symptom.lower()
    if "erp" in s and ("branch 2" in s or "br02" in s or "br2" in s) and "internet" in s:
        return SCENARIOS[ScenarioType.ERP_UNREACHABLE]
    if "wifi" in s or "wi-fi" in s or "واي فاي" in s and ("slow" in s or "بطي" in s or "speed" in s):
        return SCENARIOS[ScenarioType.WIFI_SLOW]
    if "vlan" in s and ("wrong" in s or "80" in s or "10.11.80" in s or "خاطئ" in s):
        return SCENARIOS[ScenarioType.WRONG_VLAN]
    if ("branch 3" in s or "br03" in s or "br3" in s) and ("down" in s or "ساقط" in s or "كامل" in s):
        return SCENARIOS[ScenarioType.BRANCH_DOWN]
    if "guest" in s and ("erp" in s or "isolation" in s or "ضيف" in s):
        # Guest isolation test — not failure but verification
        return None
    return None
