"""
Enterprise — REAL multi-branch company framework — WORLD-CLASS PROFESSIONAL
from zero to handover — 40Y expert — ULTRA LEGENDARY

Supports ANY institution: trading, hospital, factory, school, hotel, bank, retail, government, office, datacenter
with any size, branches, devices — with absolute ultra precision, zero hallucinations.

How a real network engineer builds a complete network:
Requirements → Survey → HLD → LLD → IP/VLAN → Security → WAN → 
Equipment → Rack & Cabling → Staging → Config → Deployment → 
Integration → Testing → Failover → Troubleshooting → Monitoring → 
As-Built → Handover → Operations

This module is PART OF THE FIRST APPLICATION — not a second app.
It makes the first app world-class professional for any real scenario.

Institution types differ: hospital ≠ factory ≠ trading — different VLANs, services, compliance, device ratios.
This framework adapts with microscopic precision — 40Y expert quality.
"""

# Al-Nour — specific example (trading)
from .al_nour import (
    AL_NOUR_COMPANY,
    HQ_SITE,
    BRANCH_SITES,
    VLAN_PLAN,
    IP_PLAN,
    WAN_DESIGN,
    SERVICES,
    SITE_OCTET,
    site_subnet,
    site_gateway,
    PHYSICAL_INVENTORY,
)
from .fabric import AlNourFabric, build_al_nour_fabric, build_al_nour_fabric_raw
from .docs import generate_all_docs
from .configs import generate_all_configs

# Institution types — generic — WORLD-CLASS
from .institution_types import (
    InstitutionType,
    SizeCategory,
    VlanTemplate,
    ServiceTemplate,
    InstitutionProfile,
    BASE_VLANS,
    INSTITUTION_VLANS,
    ALL_VLANS,
    BASE_SERVICES,
    INSTITUTION_SERVICES,
    ALL_SERVICES,
    INSTITUTION_PROFILES,
    get_institution_profile,
    get_vlans_for_institution,
    get_services_for_institution,
    calculate_devices_for_site,
    estimate_infra_for_site,
    get_all_institution_types,
)

# Generic company builder — ANY institution
from .generic_company import (
    GenericSiteSpec,
    GenericCompanyDef,
    build_generic_company,
    company_to_dict,
    get_site_octet,
    build_hospital_example,
    build_factory_example,
    build_school_example,
    build_hotel_example,
    build_bank_example,
)

# Generic fabric — ANY company
from .generic_fabric import (
    GenericFabric,
    build_generic_fabric,
    build_generic_fabric_raw,
)

# Generic configs — ANY company
from .generic_configs import (
    generate_all_configs_generic,
)

# Generic workflow v2 — institution-aware — WORLD-CLASS
from .generic_workflow import (
    get_workflow_for_institution,
    get_workflow_for_company,
    generate_generic_docs,
    INSTITUTION_WORKFLOW_ADDITIONS,
)
from .generic_troubleshooting import (
    get_scenarios_for_institution,
    get_all_generic_scenarios,
    INSTITUTION_SCENARIOS,
)
from .generic_testing import (
    generate_all_tests_generic,
    tests_to_dict_generic,
)

# Workflow, troubleshooting, testing — generic (base)
from .workflow import WORKFLOW_STEPS, get_workflow, workflow_to_dict, workflow_progress, WorkflowPhase
from .troubleshooting import SCENARIOS, get_scenario, get_all_scenarios, rca_for_symptom, ScenarioType
from .testing import generate_all_tests, tests_to_dict, TestLayer, TestVerdict

__all__ = [
    # Al-Nour specific (backward compat)
    "AL_NOUR_COMPANY",
    "HQ_SITE",
    "BRANCH_SITES",
    "VLAN_PLAN",
    "IP_PLAN",
    "WAN_DESIGN",
    "SERVICES",
    "SITE_OCTET",
    "site_subnet",
    "site_gateway",
    "PHYSICAL_INVENTORY",
    "AlNourFabric",
    "build_al_nour_fabric",
    "build_al_nour_fabric_raw",
    "generate_all_docs",
    "generate_all_configs",
    # Institution types — generic — WORLD-CLASS
    "InstitutionType",
    "SizeCategory",
    "VlanTemplate",
    "ServiceTemplate",
    "InstitutionProfile",
    "BASE_VLANS",
    "INSTITUTION_VLANS",
    "ALL_VLANS",
    "BASE_SERVICES",
    "INSTITUTION_SERVICES",
    "ALL_SERVICES",
    "INSTITUTION_PROFILES",
    "get_institution_profile",
    "get_vlans_for_institution",
    "get_services_for_institution",
    "calculate_devices_for_site",
    "estimate_infra_for_site",
    "get_all_institution_types",
    # Generic company
    "GenericSiteSpec",
    "GenericCompanyDef",
    "build_generic_company",
    "company_to_dict",
    "get_site_octet",
    "build_hospital_example",
    "build_factory_example",
    "build_school_example",
    "build_hotel_example",
    "build_bank_example",
    # Generic fabric
    "GenericFabric",
    "build_generic_fabric",
    "build_generic_fabric_raw",
    # Generic configs
    "generate_all_configs_generic",
    # Generic workflow v2 — institution-aware — WORLD-CLASS
    "get_workflow_for_institution",
    "get_workflow_for_company",
    "generate_generic_docs",
    "INSTITUTION_WORKFLOW_ADDITIONS",
    "get_scenarios_for_institution",
    "get_all_generic_scenarios",
    "INSTITUTION_SCENARIOS",
    "generate_all_tests_generic",
    "tests_to_dict_generic",
    # Workflow etc. (base)
    "WORKFLOW_STEPS",
    "get_workflow",
    "workflow_to_dict",
    "workflow_progress",
    "WorkflowPhase",
    "SCENARIOS",
    "get_scenario",
    "get_all_scenarios",
    "rca_for_symptom",
    "ScenarioType",
    "generate_all_tests",
    "tests_to_dict",
    "TestLayer",
    "TestVerdict",
]
