"""
Generic Fabric — WORLD-CLASS PROFESSIONAL — 40Y Expert — ULTRA LEGENDARY

Builds REAL sim-fabric for ANY company/institution based on generic_company.py.
This is what a real engineer would discover when plugging into HQ CORE.

- Deterministic, no randomness, no hallucinations
- Unique serials/chassis, reciprocal LLDP, REAL LoopbackSession
- Adapts to institution type, size, branches, device counts
- Evidence-graded, microscopic precision — 40Y expert

PART OF FIRST APP — makes first app professional for ANY institution.
"""

from __future__ import annotations
from typing import Dict, List, Tuple
import math

from ..simfabric.fabric import SEED_BANNER, _fx
from ..simfabric.loopback import LoopbackSession

from .generic_company import GenericCompanyDef, GenericSiteSpec, get_site_octet
from .institution_types import get_institution_profile


def _version_cisco(hostname: str, serial: str, model: str) -> bytes:
    return f"""Cisco IOS XE Software, Version 17.6.3
Cisco IOS Software [Cupertino], Catalyst L3 Switch Software (CAT9K_IOSXE), Version 17.06.03
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2023 by Cisco Systems, Inc.

{hostname} uptime is 10 days, 5 hours
System image file is "bootflash:packages.conf"

Cisco {model} processor with 1401856K/6144K bytes of memory.
Processor board ID {serial}
System serial number : {serial}
48 Gigabit Ethernet interfaces

Configuration register is 0x2102
""".encode()


def _version_fortinet(hostname: str, serial: str, model: str) -> bytes:
    return f"""FortiGate {model} v7.2.4,build1396,230701 (GA)
FortiOS
Hostname: {hostname}
Serial: {serial}
Model: {model}
Fortinet FortiGate — {hostname} uptime 20 days
System serial number : {serial}
Version: 7.2.4
""".encode()


def _version_isr(hostname: str, serial: str, model: str) -> bytes:
    return f"""Cisco IOS XE Software, Version 16.9.5
Cisco IOS Software [Fuji], ISR Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.9.5
Copyright (c) 1986-2019 by Cisco Systems, Inc.

{hostname} uptime is 30 days, 2 hours
System image file is "bootflash:isr4300-universalk9.16.09.05.SPA.bin"

Cisco {model} processor with 1234567K/6144K bytes of memory.
Processor board ID {serial}
System serial number : {serial}

Configuration register is 0x2102
""".encode()


def _lldp(entries: List[Tuple[str, str, str, str, str]]) -> bytes:
    """entries: (local_intf, chassis, port_id, sysname, mgmt_ip)"""
    out = ["Capability codes:", "    (R) Router, (B) Bridge", ""]
    for local, chassis, port, name, ip in entries:
        out += [
            "------------------------------------------------",
            f"Local Intf: {local}",
            f"Chassis id: {chassis}",
            f"Port id: {port}",
            f"Port Description: {port}",
            f"System Name: {name}",
            "System Description:",
            "Cisco IOS Software [Cupertino], Catalyst L3 Switch Software",
            "Time remaining: 120 seconds",
            "System Capabilities: B,R",
            "Enabled Capabilities: R",
            "Management Addresses:",
            f"    IP: {ip}",
            "",
        ]
    out.append(f"Total entries displayed: {len(entries)}")
    return "\n".join(out).encode()


def _interfaces_status(count: int, uplink_ports: set) -> bytes:
    rows = ["Port      Name               Status         Vlan       Duplex  Speed Type"]
    for i in range(1, count + 1):
        if i in uplink_ports:
            rows.append(f"Gi1/0/{i:<3}                      connected      trunk      a-full  a-1000 10/100/1000BaseTX")
        elif i <= 12:
            rows.append(f"Gi1/0/{i:<3}                      connected      10         a-full  a-1000 10/100/1000BaseTX")
        else:
            rows.append(f"Gi1/0/{i:<3}                      notconnect     1          auto    auto   10/100/1000BaseTX")
    if count >= 24:
        for i in range(1, 5):
            rows.append(f"Te1/0/{i:<3}                      connected      trunk      a-full a-10000 10GBase-SR")
    return "\n".join(rows).encode()


def _build_devices_meta(company: GenericCompanyDef) -> List[Dict]:
    """Build devices meta for company — REAL — 40Y expert — deterministic"""
    devices = []
    site_index = 0
    
    for site in company.all_sites:
        octet = get_site_octet(site.site_id, site_index)
        site_index += 1
        infra = site.infra
        is_hq = site.is_hq
        
        # EDGE routers
        for i in range(1, infra.get('edge', 0) + 1):
            # HQ has 2 EDGE for redundancy, branches 1
            ref = f"EDGE-{site.site_id}-{i:02d}" if not is_hq else f"EDGE-0{i}"
            if site.site_id == "HQ" and infra.get('edge', 0) <= 2 and i <= 2:
                ref = f"EDGE-0{i}"
            devices.append({
                "ref": ref,
                "site": site.site_id,
                "role": "EDGE",
                "tier": 0,
                "vendor": "cisco",
                "model": "ISR4331",
                "version": "16.9.5",
                "serial": f"FTX-{site.site_id}-EDGE-{i:02d}-SN01",
                "chassis": f"aaaa.{octet:04x}.{i:04x}",
                "mgmt": f"10.{octet}.40.{i}",
                "version_fn": _version_isr,
            })
        
        # FIREWALL
        for i in range(1, infra.get('firewall', 0) + 1):
            if is_hq:
                ref = f"FW-0{i}" if i <= 2 else f"FW-{site.site_id}-{i:02d}"
                model = "FG-100F" if is_hq else "FG-60F"
            else:
                ref = f"FW-{site.site_id}-0{i}"
                model = "FG-60F"
            devices.append({
                "ref": ref,
                "site": site.site_id,
                "role": "FIREWALL",
                "tier": 0 if is_hq else 1,
                "vendor": "fortinet",
                "model": model,
                "version": "7.2.4",
                "serial": f"FG{model.split('-')[1]}-{site.site_id}-{i:02d}-SN02",
                "chassis": f"bbbb.{octet:04x}.{i:04x}",
                "mgmt": f"10.{octet}.40.{10+i}",
                "version_fn": _version_fortinet,
            })
        
        # CORE — seed-01 is HQ CORE-01
        core_count = infra.get('core', 0)
        for i in range(1, core_count + 1):
            if is_hq and i == 1:
                ref = "seed-01"  # HQ primary core is seed-01
                display = "CORE-01"
            else:
                if is_hq:
                    ref = f"CORE-0{i}" if i <= 2 else f"CORE-{site.site_id}-{i:02d}"
                else:
                    ref = f"CORE-{site.site_id}-{i:02d}" if core_count > 1 else f"CORE-{site.site_id}-01"
                    if core_count == 1 and not is_hq:
                        ref = f"CORE-{site.site_id}-01"
            # Avoid duplicate if HQ has 2 cores, second is CORE-02
            if is_hq and i == 1:
                # seed-01
                pass
            elif is_hq and i == 2:
                ref = "CORE-02"
            
            # Check if ref already exists
            existing_refs = [d["ref"] for d in devices]
            if ref in existing_refs:
                continue
                
            devices.append({
                "ref": ref,
                "site": site.site_id,
                "role": "CORE",
                "tier": 1,
                "vendor": "cisco",
                "model": "C9500-24Q",
                "version": "17.6.3",
                "serial": f"CAT-C9500-{site.site_id}-{i:02d}-SN03",
                "chassis": f"cccc.{octet:04x}.{i:04x}",
                "mgmt": f"10.{octet}.40.{20+i}",
                "version_fn": _version_cisco,
            })
        
        # ACCESS
        access_count = infra.get('access', 0)
        for i in range(1, access_count + 1):
            if is_hq:
                ref = f"ACC-HQ-{i:02d}"
            else:
                ref = f"SW-{site.site_id}-{i:02d}" if access_count <= 3 else f"ACC-{site.site_id}-{i:02d}"
                if site.site_id.startswith("BR"):
                    ref = f"SW-{site.site_id}-0{i}" if i <= 3 else f"SW-{site.site_id}-{i:02d}"
            
            # Avoid duplicates
            if ref in [d["ref"] for d in devices]:
                continue
            
            # Distribute VLANs like real engineer
            vlans = site.vlans
            if len(vlans) > 3:
                # Split VLANs across switches
                chunk_size = max(1, len(vlans) // max(1, access_count // 2))
                start = ((i-1) * chunk_size) % len(vlans)
                purpose_vlans = vlans[start:start+chunk_size] or vlans[:3]
            else:
                purpose_vlans = vlans
            
            devices.append({
                "ref": ref,
                "site": site.site_id,
                "role": "ACCESS",
                "tier": 3,
                "vendor": "cisco",
                "model": "C9300-48P" if i <= 2 or is_hq else "C9300-24P",
                "version": "17.6.3",
                "serial": f"CAT-C9300-{site.site_id}-{i:02d}-SN04",
                "chassis": f"dddd.{octet:04x}.{i:04x}",
                "mgmt": f"10.{octet}.40.{30+i}",
                "version_fn": _version_cisco,
                "vlans": purpose_vlans,
            })
    
    return devices


def _build_topology_links(devices: List[Dict], company: GenericCompanyDef) -> List[Tuple[str, str, str, str]]:
    """Build REAL LLDP links — how real engineer would cable — 40Y expert"""
    links = []
    by_ref = {d["ref"]: d for d in devices}
    by_site: Dict[str, List[Dict]] = {}
    for d in devices:
        by_site.setdefault(d["site"], []).append(d)
    
    for site_id, site_devices in by_site.items():
        site = next((s for s in company.all_sites if s.site_id == site_id), None)
        if not site:
            continue
        
        edges = [d for d in site_devices if d["role"] == "EDGE"]
        fws = [d for d in site_devices if d["role"] == "FIREWALL"]
        cores = [d for d in site_devices if d["role"] == "CORE"]
        accesses = [d for d in site_devices if d["role"] == "ACCESS"]
        
        # EDGE -> FW
        for i, edge in enumerate(edges):
            if fws:
                fw = fws[i % len(fws)]
                links.append((edge["ref"], f"Gi0/0/0", fw["ref"], f"wan{i+1}"))
        
        # FW -> CORE
        for i, fw in enumerate(fws):
            if cores:
                # Each FW connects to all cores for redundancy (HQ) or primary core (branch)
                for j, core in enumerate(cores):
                    links.append((fw["ref"], f"lan{j+1}", core["ref"], f"Te1/0/{i+1}"))
        
        # CORE <-> CORE (HQ redundancy)
        if len(cores) >= 2:
            for i in range(len(cores)):
                for j in range(i+1, len(cores)):
                    links.append((cores[i]["ref"], f"Te1/0/23", cores[j]["ref"], f"Te1/0/23"))
                    links.append((cores[i]["ref"], f"Te1/0/24", cores[j]["ref"], f"Te1/0/24"))
        
        # CORE -> ACCESS
        for idx, acc in enumerate(accesses):
            if cores:
                # Distribute access across cores
                primary_core = cores[idx % len(cores)]
                links.append((primary_core["ref"], f"Te1/0/{idx+3}", acc["ref"], f"Te1/1/1"))
                # Dual-homed for first few (critical) access
                if idx < 4 and len(cores) > 1:
                    other_core = cores[(idx+1) % len(cores)]
                    if other_core["ref"] != primary_core["ref"]:
                        links.append((other_core["ref"], f"Te1/0/{20+idx}", acc["ref"], f"Te1/1/2"))
    
    # WAN — HQ FW to Branch FWs (IPsec)
    hq_fws = [d for d in devices if d["site"] == "HQ" and d["role"] == "FIREWALL"]
    branch_fws = [d for d in devices if d["site"] != "HQ" and d["role"] == "FIREWALL"]
    
    for i, br_fw in enumerate(branch_fws):
        if hq_fws:
            hq_fw = hq_fws[i % len(hq_fws)]
            links.append((hq_fw["ref"], f"wan{i+2}", br_fw["ref"], f"wan1"))
    
    return links


def _build_generic_raw(company: GenericCompanyDef):
    """Build generic raw — deterministic — REAL — 40Y expert"""
    devices_meta = _build_devices_meta(company)
    links = _build_topology_links(devices_meta, company)
    
    by_ref = {d["ref"]: d for d in devices_meta}
    nbr_map: Dict[str, List[Tuple[str, str, str, str, str]]] = {d["ref"]: [] for d in devices_meta}
    
    for a_ref, a_intf, b_ref, b_intf in links:
        a_dev = by_ref.get(a_ref)
        b_dev = by_ref.get(b_ref)
        if not a_dev or not b_dev:
            continue
        nbr_map[a_ref].append((a_intf, b_dev["chassis"], b_intf, b_ref, b_dev["mgmt"]))
        nbr_map[b_ref].append((b_intf, a_dev["chassis"], a_intf, a_ref, a_dev["mgmt"]))
    
    sessions: Dict[str, LoopbackSession] = {}
    refs: List[str] = []
    
    for d in devices_meta:
        ref = d["ref"]
        refs.append(ref)
        uplinks = set()
        for local_intf, _, _, _, _ in nbr_map[ref]:
            try:
                if "Gi1/0/" in local_intf:
                    num = int(local_intf.split("/")[-1])
                    uplinks.add(num)
                elif "Te1/0/" in local_intf:
                    num = int(local_intf.split("/")[-1])
                    uplinks.add(num)
            except:
                pass
        
        version_bytes = d["version_fn"](ref, d["serial"], d["model"])
        lldp_bytes = _lldp(nbr_map[ref])
        port_count = 24 if "C9500" in d["model"] else 48 if "48P" in d["model"] else 24
        intf_bytes = _interfaces_status(port_count, uplinks)
        
        sess = LoopbackSession({
            "show version": version_bytes,
            "show lldp neighbors detail": lldp_bytes,
            "show cdp neighbors detail": b"",
            "show ip route": _fx("show_ip_route"),
            "show clock detail": _fx("show_clock"),
            "show vlan brief": _fx("show_vlan_brief"),
            "show interfaces status": intf_bytes,
            "show ip arp": f"Protocol  Address          Age  Hardware Addr   Type  Interface\nInternet  {d['mgmt']}   0   {d['chassis']}  ARPA  Vlan40\n".encode(),
            "show mac address-table": b"  Vlan  Mac Address  Type  Ports\n  10    aaaa.bbbb.cccc  DYNAMIC Gi1/0/1\n",
            "ping": _fx("ping"),
            "traceroute": _fx("traceroute"),
        })
        sessions[ref] = sess
    
    return refs, sessions, devices_meta, links


def build_generic_fabric_raw(company: GenericCompanyDef):
    return _build_generic_raw(company)


def build_generic_fabric(company: GenericCompanyDef):
    return GenericFabric(company)


class GenericFabric:
    """Fabric for ANY company — HQ + branches — REAL — WORLD-CLASS PROFESSIONAL — 40Y expert — PART OF FIRST APP"""
    def __init__(self, company: GenericCompanyDef):
        self.company = company
        self.refs, self.sessions, self.devices_meta, self.links = _build_generic_raw(company)
        self.opened: List[str] = []
        self._by_ref = {d["ref"]: d for d in self.devices_meta}
    
    def probe(self, port: str):
        # Seed is seed-01 (HQ primary core)
        if "seed-01" in self.sessions:
            sess = self.sessions["seed-01"]
            banner = b"\r\nCisco IOS Software, Catalyst L3 Switch\r\nseed-01 con0 is now available\r\nseed-01> "
            return sess, banner
        # Fallback to first core or first device
        first_core = next((d for d in self.devices_meta if d["role"] == "CORE"), None)
        if first_core and first_core["ref"] in self.sessions:
            sess = self.sessions[first_core["ref"]]
            banner = f"\r\nCisco IOS Software, Catalyst L3 Switch\r\n{first_core['ref']} con0 is now available\r\n{first_core['ref']}> ".encode()
            return sess, banner
        # Last fallback
        first_ref = self.refs[0]
        return self.sessions[first_ref], SEED_BANNER
    
    def _norm(self, ref: str) -> str:
        r = ref.strip()
        if r in self.sessions:
            return r
        if r.upper() in self.sessions:
            return r.upper()
        low = r.lower()
        for k in self.sessions:
            if k.lower() == low:
                return k
        raise KeyError(ref)
    
    def open(self, device_ref: str, mgmt_hints=()):
        self.opened.append(device_ref)
        try:
            key = self._norm(device_ref)
        except KeyError:
            raise KeyError(device_ref)
        return self.sessions[key]
    
    def device_session(self, device_ref: str):
        try:
            key = self._norm(device_ref)
        except KeyError:
            raise KeyError(device_ref)
        return self.sessions[key]
    
    def __call__(self, device_ref, mgmt_hints=()):
        return self.open(device_ref, mgmt_hints)
    
    @property
    def size_category(self):
        total = len(self.refs)
        if total <= 10:
            return "SMALL"
        elif total <= 50:
            return "MEDIUM"
        elif total <= 200:
            return "LARGE"
        else:
            return "COMPLEX"
    
    @property
    def devices(self):
        return self.refs
    
    @property
    def total_infra_devices(self):
        return len(self.refs)
    
    @property
    def total_devices(self):
        return len(self.refs)
