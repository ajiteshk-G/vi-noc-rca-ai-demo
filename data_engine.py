"""Synthetic Dataset & Grounded Intelligence Engine for Vi (Vodafone Idea) NOC RCA & Trouble Ticket Demo.

Generates:
1. 1,000 Historical Resolved Tickets (450 RAN, 300 Transport, 250 Core) across 5 Vi Circles,
   embedding the 46-ticket "Golden Correlation" cluster (INC-Telco-78500 to INC-Telco-78545, RFO-Telco-2026-0811).
2. 100 Open Active Tickets (45 RAN, 30 Transport, 25 Core) including Featured Anchors
   INC-Telco-OPEN-001, INC-Telco-OPEN-002, and INC-Telco-OPEN-003.
3. 6 Systemic Failure Clusters, 5 Executive Query Templates, Cross-Domain Triage Diagnostics,
   Guided CLI Remediation Playbooks, Terminal Pre-Check Simulations, and Executive RCA Markdown Reports.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
import random
from typing import Any, Dict, List


CIRCLES = [
    "Maharashtra/Pune",
    "Delhi-NCR",
    "Gujarat",
    "Mumbai",
    "UP-West",
]

CIRCLE_CODES = {
    "Maharashtra/Pune": "MH-PUN",
    "Delhi-NCR": "DL-NCR",
    "Gujarat": "GJ-AMD",
    "Mumbai": "MUM-BKC",
    "UP-West": "UPW-MRT",
}

SYSTEMIC_CLUSTERS: List[Dict[str, Any]] = [
    {
        "cluster_id": "CLU-01",
        "number": 1,
        "title": "Transport MTU & Buffer Mismatches (Cross-Domain)",
        "short_title": "Transport MTU & Buffer Mismatches",
        "primary_domain": "Transport ➔ 5G Core",
        "filter_domain": "Core",
        "ticket_count": 142,
        "golden_correlation_count": 46,
        "pct_of_total": "14.2%",
        "avg_mttr_before_min": 118,
        "avg_mttr_after_min": 14,
        "mttr_reduction_pct": "88%",
        "severity_profile": "68% P1 • 32% P2",
        "rfo_reference": "RFO-Telco-2026-0811",
        "sample_ticket_range": "INC-Telco-78500 – 78545",
        "root_cause_pattern": (
            "VLAN 402 MTU set to 1420B (vs 1500B) drops DF-marked N4 PFCP frames (>1420B), causing 5G VoNR call drops."
        ),
        "ai_remediation_guardrail": (
            "Enforce 1500B MTU via NETCONF + reset SMF PFCP peer."
        ),
        "badge_color": "red",
    },
    {
        "cluster_id": "CLU-02",
        "number": 2,
        "title": "5G SBI & PFCP Signaling Timeouts",
        "short_title": "5G SBI & PFCP Timeouts",
        "primary_domain": "5G Core",
        "filter_domain": "Core",
        "ticket_count": 168,
        "golden_correlation_count": 0,
        "pct_of_total": "16.8%",
        "avg_mttr_before_min": 84,
        "avg_mttr_after_min": 46,
        "mttr_reduction_pct": "45%",
        "severity_profile": "44% P1 • 46% P2 • 10% P3",
        "rfo_reference": "RFO-Telco-2026-0719",
        "sample_ticket_range": "INC-Telco-78110 – 78277",
        "root_cause_pattern": (
            "HTTP/2 SBI 503/504 timeouts on N11/N7 from NRF token thread starvation and Envoy pool exhaustion."
        ),
        "ai_remediation_guardrail": (
            "Auto-scale Envoy HTTP/2 streams + pre-warm NRF OAuth2 cache."
        ),
        "badge_color": "yellow",
    },
    {
        "cluster_id": "CLU-03",
        "number": 3,
        "title": "Optical Fiber Attenuation & DWDM Degradation",
        "short_title": "Optical Fiber & DWDM",
        "primary_domain": "Transport",
        "filter_domain": "Transport",
        "ticket_count": 188,
        "golden_correlation_count": 0,
        "pct_of_total": "18.8%",
        "avg_mttr_before_min": 142,
        "avg_mttr_after_min": 89,
        "mttr_reduction_pct": "37%",
        "severity_profile": "38% P1 • 48% P2 • 14% P3",
        "rfo_reference": "RFO-Telco-2026-0604",
        "sample_ticket_range": "INC-Telco-78301 – 78488",
        "root_cause_pattern": (
            "DWDM Rx power degradation (-25.8 dBm) from duct micro-bends triggers FEC errors and BGP BFD flaps."
        ),
        "ai_remediation_guardrail": (
            "Trigger proactive MPLS-TE Fast Reroute (Tunnel 104) before hard LOS."
        ),
        "badge_color": "red",
    },
    {
        "cluster_id": "CLU-04",
        "number": 4,
        "title": "Massive MIMO Beamforming & Sleep Lockups",
        "short_title": "mMIMO Sleep Lockups",
        "primary_domain": "RAN",
        "filter_domain": "RAN",
        "ticket_count": 248,
        "golden_correlation_count": 0,
        "pct_of_total": "24.8%",
        "avg_mttr_before_min": 76,
        "avg_mttr_after_min": 41,
        "mttr_reduction_pct": "46%",
        "severity_profile": "18% P1 • 62% P2 • 20% P3",
        "rfo_reference": "RFO-Telco-2026-0902",
        "sample_ticket_range": "INC-Telco-78550 – 78797",
        "root_cause_pattern": (
            "64T64R AAU v24.3 firmware sleep deadlock pins urban sectors in 8T8R mode during evening peak."
        ),
        "ai_remediation_guardrail": (
            "Remote gnb-cli energy-saving override wakes all 64T64R beams without truck rolls."
        ),
        "badge_color": "yellow",
    },
    {
        "cluster_id": "CLU-05",
        "number": 5,
        "title": "Antenna Feedline & VSWR RF Degradation",
        "short_title": "Antenna Feedline & VSWR",
        "primary_domain": "RAN",
        "filter_domain": "RAN",
        "ticket_count": 172,
        "golden_correlation_count": 0,
        "pct_of_total": "17.2%",
        "avg_mttr_before_min": 164,
        "avg_mttr_after_min": 105,
        "mttr_reduction_pct": "36%",
        "severity_profile": "12% P1 • 54% P2 • 34% P3",
        "rfo_reference": "RFO-Telco-2026-0518",
        "sample_ticket_range": "INC-Telco-78798 – 78969",
        "root_cause_pattern": (
            "Moisture ingress on 4.3-10 RF jumpers raises VSWR > 1.85:1, causing PA thermal backoff."
        ),
        "ai_remediation_guardrail": (
            "Shift load via RET tilt + dispatch field rigger with exact sector/port BOM."
        ),
        "badge_color": "blue",
    },
    {
        "cluster_id": "CLU-06",
        "number": 6,
        "title": "Core AMF Registration Throttling & Storms",
        "short_title": "Core AMF Reg Storms",
        "primary_domain": "5G Core",
        "filter_domain": "Core",
        "ticket_count": 82,
        "golden_correlation_count": 0,
        "pct_of_total": "8.2%",
        "avg_mttr_before_min": 92,
        "avg_mttr_after_min": 51,
        "mttr_reduction_pct": "45%",
        "severity_profile": "35% P1 • 45% P2 • 20% P3",
        "rfo_reference": "RFO-Telco-2026-0829",
        "sample_ticket_range": "INC-Telco-78001 – 78082",
        "root_cause_pattern": (
            "Post-power-restore NAS registration floods (>42k req/s) saturate AMF SCTP queues."
        ),
        "ai_remediation_guardrail": (
            "Apply 180s 3GPP UAC access barring + stagger gNodeB SCTP timers."
        ),
        "badge_color": "blue",
    },
]


EXECUTIVE_QUERY_TEMPLATES: List[Dict[str, Any]] = [
    {
        "id": "q1",
        "question": "Which Transport network anomalies most frequently trigger downstream 5G Core VoNR call drops?",
        "headline": "Transport VLAN 402 MTU Mismatches Drive 74.6% of Cross-Domain VoNR Drops",
        "summary_metrics": [
            {"label": "Transport ➔ Core Tickets", "value": "142 (14.2%)", "delta": "#1 Cross-Domain Vector"},
            {"label": "Golden Cluster (VLAN 402)", "value": "46 Tickets", "delta": "MTU 1420B vs 1500B"},
            {"label": "VoNR Call Drop Spike", "value": "14.2% – 16.8%", "delta": "Baseline <0.15%"},
            {"label": "AI Post-Fix MTTR", "value": "14.2 mins", "delta": "-88% vs 118m manual"},
        ],
        "executive_summary": (
            "• **Primary Driver:** **Cluster 1 (142 tickets)** is the #1 upstream trigger of 5G Core VoNR call drops.\n"
            "• **Root Mechanism:** **46 Golden Cluster incidents** traced to `VLAN 402` MTU set to **1420B** on `AGG-RTR-MH-PUN-04`, silently dropping DF-marked N4 PFCP packets (>1420B) between `SMF-MH-PUN-02` and `UPF-MH-PUN-EDGE-01`."
        ),
        "evidence_citations": [
            "INC-Telco-78500–78545 (46 Pune Golden Correlation tickets) • RFO-Telco-2026-0811",
            "INC-Telco-78312 & 78389 (Mumbai-Pune DWDM OSNR flaps) • RFO-Telco-2026-0604",
        ],
        "operational_recommendation": (
            "Block sub-interface MTU < 1500B via NETCONF pre-commit guardrails on N3/N4 VRFs and run 1472B DF-bit TWAMP probes."
        ),
    },
    {
        "id": "q2",
        "question": "Compare MTTR and dominant failure modes between Maharashtra (Pune Hub) and Delhi-NCR circles.",
        "headline": "Pune Led by Transport-Core MTU Faults (260) vs. Delhi-NCR mMIMO Sleep Lockups (220)",
        "summary_metrics": [
            {"label": "Maharashtra/Pune", "value": "260 Tickets", "delta": "MTTR: 58m ➔ 31m (-46.5%)"},
            {"label": "Delhi-NCR", "value": "220 Tickets", "delta": "MTTR: 64m ➔ 38m (-40.6%)"},
            {"label": "Pune Top Fault", "value": "VLAN 402 MTU (38%)", "delta": "46 Golden P1s"},
            {"label": "Delhi Top Fault", "value": "mMIMO Sleep (49%)", "delta": "Evening Peak 18:00–22:00"},
        ],
        "executive_summary": (
            "• **Maharashtra/Pune (260 tickets):** Dominated by cross-domain Transport-to-Core `VLAN 402` MTU drops (`UPF-MH-PUN-EDGE-01`); AI correlation cut MTTR **46.5% (58.4m ➔ 31.2m)**.\n"
            "• **Delhi-NCR (220 tickets):** Skewed toward urban **64T64R mMIMO sleep lockups** (`GNB-DL-CP-408/409`); remote `gnb-cli` wake-up cut MTTR **40.6% (64.0m ➔ 38.0m)**."
        ),
        "evidence_citations": [
            "Pune: INC-Telco-78500–78545 (RFO-Telco-2026-0811)",
            "Delhi-NCR: INC-Telco-78560–78690 (RFO-Telco-2026-0902)",
        ],
        "operational_recommendation": (
            "Enforce N4 VLAN MTU guardrails in Pune; schedule 17:30 IST O-RAN SMO pre-peak sleep-lock overrides in Delhi-NCR."
        ),
    },
    {
        "id": "q3",
        "question": "Which top 5 Core and Transport network elements generated repeated P1 incidents over the past 6 months?",
        "headline": "Top 5 Core & Transport Nodes Account for 63.4% of All P1 Outage Minutes",
        "summary_metrics": [
            {"label": "#1 UPF-MH-PUN-EDGE-01", "value": "34 P1s", "delta": "N4 PFCP Drops (18m MTTR)"},
            {"label": "#2 SMF-MH-PUN-02", "value": "31 P1s", "delta": "PFCP Timeout (16m MTTR)"},
            {"label": "#3 PE-RTR-MUM-BKC-01", "value": "24 P1s", "delta": "BGP / Fiber Flap (42m MTTR)"},
            {"label": "#4 DWDM-MUM-POW-02", "value": "19 P1s", "delta": "Rx <-25dBm (54m MTTR)"},
        ],
        "executive_summary": (
            "• **5G Core Pair (`UPF-MH-PUN-EDGE-01` [34 P1s] & `SMF-MH-PUN-02` [31 P1s]):** Driven by upstream `VLAN 402` MTU truncation.\n"
            "• **Mumbai Optical Pair (`PE-RTR-MUM-BKC-01` [24 P1s] & `DWDM-MUM-POW-02` [19 P1s]):** Driven by soft fiber attenuation on `TenGigE0/0/0/1` (`#5 AMF-GJ-AMD-01`: 14 P1s from NAS storms)."
        ),
        "evidence_citations": [
            "Pune Core: INC-Telco-78500–78545 (RFO-Telco-2026-0811)",
            "Mumbai Optical: INC-Telco-78310–78365 (RFO-Telco-2026-0604)",
            "Gujarat AMF: INC-Telco-78012–78058 (RFO-Telco-2026-0829)",
        ],
        "operational_recommendation": (
            "Lock `VLAN 402` MTU=1500B on `AGG-RTR-MH-PUN-04` and lower MPLS-TE auto-FRR optical threshold to `-22.5 dBm` in Mumbai."
        ),
    },
    {
        "id": "q4",
        "question": "What percentage of RAN tickets were caused by Massive MIMO software sleep lockups versus physical hardware/cable faults?",
        "headline": "55.1% of RAN Tickets Are Software Sleep Lockups (Remote CLI Fix) vs. 38.2% Physical RF Faults",
        "summary_metrics": [
            {"label": "Total RAN Tickets", "value": "450 (45.0%)", "delta": "Largest Domain Share"},
            {"label": "Software Sleep Lockups", "value": "248 (55.1%)", "delta": "Remote Fix in <4 mins"},
            {"label": "Hardware VSWR / Cable", "value": "172 (38.2%)", "delta": "Requires Field Rigger"},
            {"label": "Other (SCTP / PRB)", "value": "30 (6.7%)", "delta": "Parameter Tuning"},
        ],
        "executive_summary": (
            "• **Software (55.1% / 248 tickets):** 64T64R AAU v24.3 sleep-state deadlocks resolved 100% remotely via `gnb-cli`, avoiding ~210 unnecessary truck rolls.\n"
            "• **Hardware (38.2% / 172 tickets):** Physical 4.3-10 jumper moisture & VSWR > 1.85:1 faults requiring tower crew dispatch."
        ),
        "evidence_citations": [
            "Cluster 4 (Software Sleep): INC-Telco-78550–78797 (RFO-Telco-2026-0902)",
            "Cluster 5 (Hardware VSWR): INC-Telco-78798–78969 (RFO-Telco-2026-0518)",
        ],
        "operational_recommendation": (
            "Run `gnb-cli --action get-sleep-mode-state` before any field dispatch and deploy AAU patch `v24.3.8-hotfix2`."
        ),
    },
    {
        "id": "q5",
        "question": "How many historical incidents match the MTU truncation signature on VLAN 402, and what was the verified recovery time?",
        "headline": "46 Historical Tickets Match VLAN 402 (1420B MTU) with 14.2-Minute Verified Recovery",
        "summary_metrics": [
            {"label": "Exact Signature Matches", "value": "46 Tickets", "delta": "INC-Telco-78500 – 78545"},
            {"label": "MTU Drift", "value": "1420B vs 1500B", "delta": "80B N4 PFCP Truncation"},
            {"label": "Verified Recovery MTTR", "value": "14.2 mins", "delta": "18s PFCP Heartbeat Restore"},
            {"label": "Post-Fix Drop Rate", "value": "< 0.02%", "delta": "Down from >14.4% Peak"},
        ],
        "executive_summary": (
            "• **46 Golden Correlation Tickets (`INC-Telco-78500–78545`):** All caused by `interface vlan402` set to `mtu 1420`, dropping DF-marked N4 PFCP setup frames.\n"
            "• **14.2-Min Recovery:** Restoring `mtu 1500` + resetting the SMF PFCP peer recovers N4 heartbeats in **18s** and normalizes VoNR drops (<0.02%) in **150s**."
        ),
        "evidence_citations": [
            "Golden Cluster: INC-Telco-78500–78545 • RFO-Telco-2026-0811",
            "Live Match: INC-Telco-OPEN-001 (98.4% similarity)",
        ],
        "operational_recommendation": (
            "Execute the 3-step `RFO-Telco-2026-0811` CLI playbook on `INC-Telco-OPEN-001` in Tab 3 for <3-minute recovery."
        ),
    },
]


def _generate_historical_tickets() -> List[Dict[str, Any]]:
    """Deterministically generates 1,000 historical resolved tickets:
    - 450 RAN (45%)
    - 300 Transport (30%)
    - 250 Core (25%)
    - Embeds INC-Telco-78500 .. INC-Telco-78545 (46 tickets) as the Golden Correlation Cluster.
    """
    rng = random.Random(20261020)
    base_time = datetime(2026, 10, 20, 12, 0, 0, tzinfo=timezone.utc)
    tickets: List[Dict[str, Any]] = []

    # Exact domain quotas across indices 1..1000 (ticket_id INC-Telco-78001 .. INC-Telco-79000)
    # Golden Correlation occupies indices 500..545 (46 tickets: INC-Telco-78500 .. INC-Telco-78545)
    # Within the 46 Golden Correlation tickets: 20 Core, 16 Transport, 10 RAN (cross-domain cascade!)
    # Remaining 954 tickets: 440 RAN, 284 Transport, 230 Core -> Total: 450 RAN, 300 Transport, 250 Core.
    remaining_domains: List[str] = (["RAN"] * 440) + (["Transport"] * 284) + (["Core"] * 230)
    rng.shuffle(remaining_domains)
    rem_idx = 0

    for idx in range(1, 1001):
        ticket_num = 78000 + idx
        ticket_id = f"INC-Telco-{ticket_num}"
        hours_ago = rng.randint(24, 24 * 180)
        created_dt = base_time - timedelta(hours=hours_ago, minutes=rng.randint(0, 59))

        if 500 <= idx <= 545:
            # Golden Correlation Cluster (46 coordinated records: INC-Telco-78500 to INC-Telco-78545)
            offset = idx - 500
            if offset < 20:
                domain = "Core"
                nodes = "UPF-MH-PUN-EDGE-01, SMF-MH-PUN-02, AGG-RTR-MH-PUN-04 (VLAN 402)"
                summary = "VoNR drop spike (14.4%) & N4 PFCP timeout via VLAN 402 MTU=1420B"
            elif offset < 36:
                domain = "Transport"
                nodes = f"AGG-RTR-MH-PUN-04 (VLAN 402), PE-RTR-MH-PUN-0{(offset % 2) + 1}"
                summary = "VLAN 402 MTU mismatch (1420B vs 1500B) dropping DF N4 PFCP frames"
            else:
                domain = "RAN"
                gnb_id = 101 + (offset - 36)
                nodes = f"GNB-MH-PUN-{gnb_id}, GNB-MH-PUN-{gnb_id + 10}, UPF-MH-PUN-EDGE-01"
                summary = "Pune gNodeB 5QI=1 VoNR bearer drops from upstream VLAN 402 N4 timeout"
            circle = "Maharashtra/Pune"
            severity = "P1-Critical" if offset < 34 else "P2-Major"
            mttr_min = rng.randint(12, 17)
            rfo_id = "RFO-Telco-2026-0811"
            cluster_id = "CLU-01"
            root_cause = "VLAN 402 MTU=1420B on AGG-RTR-MH-PUN-04 dropped DF-marked N4 PFCP (>1420B) packets."
            resolution_steps = "1. show interface vlan402 | include MTU  2. interface vlan402; mtu 1500; commit  3. smf-cli reset-pfcp-peer"
            golden = True
        else:
            golden = False
            domain = remaining_domains[rem_idx]
            rem_idx += 1
            circle = rng.choices(
                CIRCLES,
                weights=[24, 23, 18, 20, 15],
                k=1,
            )[0]
            ccode = CIRCLE_CODES[circle]

            if domain == "RAN":
                if rng.random() < 0.56:
                    cluster_id = "CLU-04"
                    rfo_id = "RFO-Telco-2026-0902"
                    severity = rng.choices(["P1-Critical", "P2-Major", "P3-Minor"], weights=[16, 64, 20], k=1)[0]
                    cell_a = rng.randint(201, 699)
                    nodes = f"GNB-{ccode}-{cell_a}, GNB-{ccode}-{cell_a + 1}"
                    summary = f"64T64R mMIMO cell sleep lockup during peak hours on {nodes}"
                    root_cause = "AAU v24.3 sleep-state deadlock pinned sector in 8T8R mode above 65% PRB load."
                    resolution_steps = f"gnb-cli --cell {cell_a} --action override-energy-saving --state active"
                    mttr_min = rng.randint(28, 52)
                else:
                    cluster_id = "CLU-05"
                    rfo_id = "RFO-Telco-2026-0518"
                    severity = rng.choices(["P1-Critical", "P2-Major", "P3-Minor"], weights=[12, 54, 34], k=1)[0]
                    cell_a = rng.randint(101, 599)
                    nodes = f"GNB-{ccode}-{cell_a}, RRU-{ccode}-S{(idx % 3) + 1}"
                    summary = f"Antenna feedline VSWR alarm (>1.92:1) & UL RSSI imbalance on {nodes}"
                    root_cause = "4.3-10 RF jumper moisture ingress caused return loss spike and PA backoff."
                    resolution_steps = "RET tilt offload + replaced 4.3-10 jumper (verified VSWR < 1.25:1)."
                    mttr_min = rng.randint(75, 130)
            elif domain == "Transport":
                if rng.random() < 0.66:
                    cluster_id = "CLU-03"
                    rfo_id = "RFO-Telco-2026-0604"
                    severity = rng.choices(["P1-Critical", "P2-Major", "P3-Minor"], weights=[36, 48, 16], k=1)[0]
                    rtr_id = (idx % 8) + 1
                    dwdm_id = (idx % 6) + 1
                    nodes = f"PE-RTR-{ccode}-0{rtr_id}, DWDM-{ccode}-0{dwdm_id}"
                    summary = f"DWDM optical attenuation (-25.{idx % 9} dBm) & BGP BFD flaps on {nodes}"
                    root_cause = "Secondary fiber span micro-bend degraded Rx power below FEC threshold."
                    resolution_steps = "mpls traffic-eng fast-reroute trigger --tunnel-id 104"
                    mttr_min = rng.randint(35, 88)
                else:
                    cluster_id = "CLU-01"
                    rfo_id = "RFO-Telco-2026-0811"
                    severity = rng.choices(["P1-Critical", "P2-Major", "P3-Minor"], weights=[45, 45, 10], k=1)[0]
                    vlan_id = rng.choice([402, 408, 512, 604])
                    nodes = f"AGG-RTR-{ccode}-0{(idx % 5) + 1} (VLAN {vlan_id}), PE-RTR-{ccode}-02"
                    summary = f"Sub-interface VLAN {vlan_id} MTU mismatch (1420B) & DSCP EF buffer drops"
                    root_cause = f"VLAN {vlan_id} set to 1420B MTU (vs 1500B), dropping DF-marked packets."
                    resolution_steps = f"interface vlan{vlan_id}; mtu 1500; commit"
                    mttr_min = rng.randint(15, 34)
            else:
                # 5G Core
                if rng.random() < 0.68:
                    cluster_id = "CLU-02"
                    rfo_id = "RFO-Telco-2026-0719"
                    severity = rng.choices(["P1-Critical", "P2-Major", "P3-Minor"], weights=[42, 46, 12], k=1)[0]
                    nodes = f"SMF-{ccode}-0{(idx % 3) + 1}, UPF-{ccode}-EDGE-0{(idx % 2) + 1}"
                    summary = f"5G Core N4 PFCP timeouts & HTTP/2 SBI 503/504 errors on {nodes}"
                    root_cause = "NRF OAuth2 token cache contention & Envoy HTTP/2 stream saturation."
                    resolution_steps = "smf-cli reset-pfcp-peer + scaled SMF Envoy HTTP/2 worker pods."
                    mttr_min = rng.randint(24, 58)
                else:
                    cluster_id = "CLU-06"
                    rfo_id = "RFO-Telco-2026-0829"
                    severity = rng.choices(["P1-Critical", "P2-Major", "P3-Minor"], weights=[34, 48, 18], k=1)[0]
                    nodes = f"AMF-{ccode}-0{(idx % 3) + 1}, AUSF-{ccode}-01"
                    summary = f"AMF NAS registration storm (>38k req/s) & SIP 500 timeout on {nodes}"
                    root_cause = "Post-power-restore UE re-registration flood saturated AMF SCTP queues."
                    resolution_steps = "Activated 180s 3GPP UAC barring profile + rebalanced AMF GUAMI weights."
                    mttr_min = rng.randint(30, 62)

        resolved_dt = created_dt + timedelta(minutes=mttr_min)
        tickets.append(
            {
                "ticket_id": ticket_id,
                "timestamp": created_dt.strftime("%Y-%m-%d %H:%M IST"),
                "resolved_at": resolved_dt.strftime("%Y-%m-%d %H:%M IST"),
                "mttr_minutes": mttr_min,
                "circle": circle,
                "domain": domain,
                "severity": severity,
                "status": "Resolved",
                "affected_nodes": nodes,
                "alarm_summary": summary,
                "root_cause": root_cause,
                "resolution_steps": resolution_steps,
                "rfo_id": rfo_id,
                "cluster_id": cluster_id,
                "is_golden_correlation": golden,
            }
        )

    return tickets


def _build_open_ticket_details(ticket: Dict[str, Any]) -> Dict[str, Any]:
    """Generates concise Cross-Domain Triage, CLI Playbook, Pre-Check Simulation, and Executive RCA Markdown
    for any of the 100 Open Active Tickets (with exact showcase specs for 001, 002, and 003).
    """
    tid = ticket["ticket_id"]
    circle = ticket["circle"]
    domain = ticket["domain"]
    severity = ticket["severity"]
    nodes = ticket["affected_nodes"]
    summary = ticket["alarm_summary"]
    ts = ticket["timestamp"]

    if tid == "INC-Telco-OPEN-001":
        triage = {
            "confidence_score": "98.4%",
            "similarity_score": "98.4%",
            "matched_cluster": "Cluster 1: Transport MTU & Buffer Mismatches (Golden Correlation)",
            "operational_impact": {
                "headline": "28,400 VoNR Subscribers Impacted Across 22 Pune gNodeBs",
                "metrics": [
                    {"label": "VoNR Call Drop Rate", "value": "14.6%", "status": "critical", "sub": "Baseline: 0.12% (>120x)"},
                    {"label": "N4 PFCP Timeouts", "value": "1,840 / min", "status": "critical", "sub": "SMF-02 ➔ UPF-EDGE-01"},
                    {"label": "Affected Subscribers", "value": "~28,400 UEs", "status": "warning", "sub": "Pune Metro Hub"},
                    {"label": "RAN Blast Radius", "value": "22 gNodeBs", "status": "warning", "sub": "GNB-MH-PUN-101..122"},
                ],
                "narrative": (
                    "P1 VoNR call teardown across **22 Pune gNodeBs** anchored on `UPF-MH-PUN-EDGE-01` and `SMF-MH-PUN-02`."
                ),
            },
            "cross_domain_correlation": {
                "headline": "Rule-Less Vector Correlation: 5G Core + IP Transport + RAN",
                "topology_path": [
                    {"layer": "RAN (22 Cells)", "node": "GNB-MH-PUN-101..122", "symptom": "5QI=1 VoNR Bearer Drops", "state": "warn"},
                    {"layer": "IP Transport (Root)", "node": "AGG-RTR-MH-PUN-04 [VLAN 402]", "symptom": "MTU 1420B vs Required 1500B", "state": "critical"},
                    {"layer": "5G Core (N4)", "node": "SMF-MH-PUN-02 ⇄ UPF-EDGE-01", "symptom": "PFCP Setup (>1420B, DF=1) Dropped", "state": "critical"},
                ],
                "narrative": (
                    "• **Core (`SMF-MH-PUN-02`):** N4 PFCP Session Establishment retries at 31.4% (64B heartbeats OK).\n"
                    "• **Transport (`AGG-RTR-MH-PUN-04`):** `VLAN 402` dropping 1,840 oversize frames/min (`mtu 1420`).\n"
                    "• **RAN (`22 Pune gNodeBs`):** Correlated `NGAP_PDU_SESSION_SETUP_FAIL` spike."
                ),
            },
            "hypothesized_root_cause": {
                "protocol_reference": "3GPP TS 29.244 (N4 PFCP) & RFC 1191 (PMTU)",
                "diagnosis": (
                    "`VLAN 402` on `AGG-RTR-MH-PUN-04` is set to **MTU 1420B** (instead of **1500B**), silently dropping DF-marked VoNR N4 PFCP setup packets (**1,456–1,488B**) between `SMF-MH-PUN-02` and `UPF-MH-PUN-EDGE-01`."
                ),
            },
            "historical_knowledge_match": {
                "similarity_pct": "98.4%",
                "matched_tickets": "INC-Telco-78500 – 78545 (46 Golden Tickets)",
                "rfo_id": "RFO-Telco-2026-0811",
                "historical_mttr": "14.2 mins (vs. 118m manual)",
                "summary": (
                    "**98.4% match** to **46 Golden Cluster tickets (`RFO-Telco-2026-0811`)**—resolved by setting `VLAN 402` MTU to `1500` and resetting the SMF PFCP peer."
                ),
            },
        }
        playbook = {
            "title": "VLAN 402 MTU Restoration & N4 PFCP Peer Reset",
            "estimated_recovery_time": "2 mins 30 secs",
            "risk_level": "Low (Hitless Sub-Interface Update)",
            "steps": [
                {
                    "step": 1,
                    "title": "Verify VLAN 402 MTU",
                    "target_node": "AGG-RTR-MH-PUN-04",
                    "description": "Confirm 1420B MTU mismatch and oversize frame drop counter.",
                    "command": "show interface vlan402 | include MTU",
                },
                {
                    "step": 2,
                    "title": "Restore MTU (1420B ➔ 1500B)",
                    "target_node": "AGG-RTR-MH-PUN-04",
                    "description": "Set standard 1500-byte MTU on VLAN 402.",
                    "command": "configure terminal; interface vlan402; mtu 1500; commit",
                },
                {
                    "step": 3,
                    "title": "Reset SMF N4 PFCP Peer",
                    "target_node": "SMF-MH-PUN-02",
                    "description": "Re-establish N4 PFCP association with UPF 10.160.44.12.",
                    "command": "smf-cli --node SMF-MH-PUN-02 --action reset-pfcp-peer --peer-ip 10.160.44.12",
                },
            ],
            "simulation_logs": [
                {"time": "12:31:02.110 IST", "type": "cmd", "text": "vi-noc@AGG-RTR-MH-PUN-04# show interface vlan402 | include MTU"},
                {"time": "12:31:02.420 IST", "type": "warn", "text": "  MTU 1420 bytes | in-oversize-drops: 27,640 [MISMATCH DETECTED]"},
                {"time": "12:31:03.050 IST", "type": "cmd", "text": "vi-noc@AGG-RTR-MH-PUN-04# configure terminal; interface vlan402; mtu 1500; commit"},
                {"time": "12:31:04.600 IST", "type": "ok", "text": "✓ MTU Verified: 1500 (1472B DF-bit probe 5/5 received, 0% loss)"},
                {"time": "12:31:05.120 IST", "type": "cmd", "text": "vi-noc@SMF-MH-PUN-02$ smf-cli --node SMF-MH-PUN-02 --action reset-pfcp-peer --peer-ip 10.160.44.12"},
                {"time": "12:31:07.010 IST", "type": "ok", "text": "✓ PFCP Heartbeat: OK (N4 Setup Success 99.98%)"},
                {"time": "12:31:08.450 IST", "type": "ok", "text": "✓ Call Drop Rate: Restored <0.02% across 22 Pune gNodeBs"},
            ],
            "verification_badges": [
                "✓ MTU Verified: 1500",
                "✓ PFCP Heartbeat: OK",
                "✓ Call Drop Rate: Restored <0.02%",
            ],
        }
    elif tid == "INC-Telco-OPEN-002":
        triage = {
            "confidence_score": "96.8%",
            "similarity_score": "96.8%",
            "matched_cluster": "Cluster 3: Optical Fiber Attenuation & DWDM Degradation",
            "operational_impact": {
                "headline": "Mumbai BKC Backbone Degraded • 18.4 Gbps Traffic at Risk",
                "metrics": [
                    {"label": "Optical Rx Power", "value": "-25.8 dBm", "status": "critical", "sub": "Threshold: -21.0 dBm (-4.8 dB)"},
                    {"label": "BGP Flaps", "value": "14 / 15m", "status": "critical", "sub": "PE-RTR-BKC-01 ⇄ DWDM-POW-02"},
                    {"label": "Packet Loss", "value": "6.8%", "status": "warning", "sub": "Pre-FEC BER > 1.4e-3"},
                    {"label": "Blast Radius", "value": "42 L3VPNs", "status": "warning", "sub": "BKC + 18 gNodeBs"},
                ],
                "narrative": (
                    "P1 optical attenuation between `PE-RTR-MUM-BKC-01` and `DWDM-MUM-POW-02` (`TenGigE0/0/0/1`), causing BFD drops and BGP route flaps."
                ),
            },
            "cross_domain_correlation": {
                "headline": "L0 DWDM Span ➔ L3 MPLS/BGP Control Plane",
                "topology_path": [
                    {"layer": "L0 DWDM", "node": "DWDM-MUM-POW-02 [Ch-34]", "symptom": "Rx -25.8 dBm & OSNR Drop", "state": "critical"},
                    {"layer": "L3 IP/MPLS", "node": "PE-RTR-MUM-BKC-01 [Te0/0/0/1]", "symptom": "CRC Errors & BFD Flapping", "state": "critical"},
                    {"layer": "Service Layer", "node": "BKC UPF & 42 L3VPNs", "symptom": "6.8% Packet Loss", "state": "warn"},
                ],
                "narrative": (
                    "• **L0 Optical (`DWDM-MUM-POW-02`):** Rx power (`-25.8 dBm`) hovers above `-27.0 dBm` LOS cutoff, preventing auto-cutover.\n"
                    "• **L3 Routing (`PE-RTR-MUM-BKC-01`):** Uncorrectable FEC bursts drop BFD keepalives every 45s."
                ),
            },
            "hypothesized_root_cause": {
                "protocol_reference": "ITU-T G.709 OTN & RFC 4090 (MPLS-TE FRR)",
                "diagnosis": (
                    "Soft fiber attenuation (**-25.8 dBm**) on `TenGigE0/0/0/1` corrupts BFD packets without triggering hard LOS, pinning traffic to the degraded span instead of **MPLS-TE Tunnel 104**."
                ),
            },
            "historical_knowledge_match": {
                "similarity_pct": "96.8%",
                "matched_tickets": "INC-Telco-78310 – 78365 (Cluster 3)",
                "rfo_id": "RFO-Telco-2026-0604",
                "historical_mttr": "8.5 mins via MPLS-TE FRR (vs. 142m splice)",
                "summary": (
                    "**96.8% match** to **Cluster 3 (`RFO-Telco-2026-0604`)**—resolved immediately via MPLS-TE Fast Reroute onto `--tunnel-id 104`."
                ),
            },
        }
        playbook = {
            "title": "Optical Power Check & MPLS-TE Fast Reroute Switchover",
            "estimated_recovery_time": "1 min 45 secs",
            "risk_level": "Low (Sub-50ms Hitless MPLS-TE Switchover)",
            "steps": [
                {
                    "step": 1,
                    "title": "Check Optical Rx Power",
                    "target_node": "PE-RTR-MUM-BKC-01",
                    "description": "Inspect DOM optical Rx power and pre-FEC BER on TenGigE0/0/0/1.",
                    "command": "show optical-power interface TenGigE0/0/0/1",
                },
                {
                    "step": 2,
                    "title": "Trigger MPLS-TE FRR (Tunnel 104)",
                    "target_node": "PE-RTR-MUM-BKC-01",
                    "description": "Steer traffic onto clean protection path Tunnel 104.",
                    "command": "mpls traffic-eng fast-reroute trigger --tunnel-id 104",
                },
            ],
            "simulation_logs": [
                {"time": "12:31:10.105 IST", "type": "cmd", "text": "vi-noc@PE-RTR-MUM-BKC-01# show optical-power interface TenGigE0/0/0/1"},
                {"time": "12:31:10.480 IST", "type": "warn", "text": "  Rx Power: -25.8 dBm [LOW ALARM] | Pre-FEC BER: 1.48e-03"},
                {"time": "12:31:11.200 IST", "type": "cmd", "text": "vi-noc@PE-RTR-MUM-BKC-01# mpls traffic-eng fast-reroute trigger --tunnel-id 104"},
                {"time": "12:31:11.890 IST", "type": "ok", "text": "✓ MPLS-TE Tunnel 104 switched to protection ring in 19.4 ms (Rx: -9.4 dBm)"},
                {"time": "12:31:13.150 IST", "type": "ok", "text": "✓ BGP Neighbor Stable | Packet Loss: 0.00%"},
            ],
            "verification_badges": [
                "✓ Optical Path: Tunnel 104 (-9.4 dBm)",
                "✓ BGP BFD: Stable (0 Flaps)",
                "✓ Packet Loss: Restored 0.00%",
            ],
        }
    elif tid == "INC-Telco-OPEN-003":
        triage = {
            "confidence_score": "97.6%",
            "similarity_score": "97.6%",
            "matched_cluster": "Cluster 4: Massive MIMO Beamforming & Sleep Lockups",
            "operational_impact": {
                "headline": "12,000 Urban 5G Subscribers Impacted in Connaught Place (Delhi-NCR)",
                "metrics": [
                    {"label": "Affected UEs", "value": "12,000 UEs", "status": "critical", "sub": "Delhi Connaught Place"},
                    {"label": "Antenna State", "value": "8T8R Sleep Lock", "status": "critical", "sub": "Expected: 64T64R Active"},
                    {"label": "DL Throughput", "value": "14.2 Mbps", "status": "warning", "sub": "Baseline: 310 Mbps (-95%)"},
                    {"label": "PRB Load", "value": "98.6%", "status": "warning", "sub": "GNB-DL-CP-408 & 409"},
                ],
                "narrative": (
                    "P2 degradation on `GNB-DL-CP-408/409`: 64T64R mMIMO cells failed to wake from sleep mode during evening peak (**12,000 UEs** impacted)."
                ),
            },
            "cross_domain_correlation": {
                "headline": "RAN PM Telemetry + Clean Transport eCPRI Verification",
                "topology_path": [
                    {"layer": "RAN AAU", "node": "GNB-DL-CP-408 & 409", "symptom": "Sleep State Deadlock (Pinned 8T8R)", "state": "critical"},
                    {"layer": "Fronthaul", "node": "DU-DL-CP-04 ⇄ AAU-408", "symptom": "eCPRI Clean (VSWR 1.18:1 Normal)", "state": "ok"},
                    {"layer": "5G Core UPF", "node": "UPF-DL-NCR-EDGE-02", "symptom": "N3 Latency 2.8ms (0% Loss)", "state": "ok"},
                ],
                "narrative": (
                    "• **Transport & RF:** 0% N3 packet loss and normal VSWR (`1.18:1`) rule out hardware faults (no truck roll needed).\n"
                    "• **RAN PM (`GNB-DL-CP-408/409`):** `pmMimoSleepStateDuration=100%` at `98.6%` PRB load confirms software sleep lockup."
                ),
            },
            "hypothesized_root_cause": {
                "protocol_reference": "3GPP TS 38.300 & O-RAN WG2 Energy Saving",
                "diagnosis": (
                    "AAU firmware `v24.3` mutex deadlock on `GNB-DL-CP-408/409` pinned sectors in `SLEEP_DEEP_8T8R` mode (disabling 56/64 TRX chains) during peak handover load."
                ),
            },
            "historical_knowledge_match": {
                "similarity_pct": "97.6%",
                "matched_tickets": "INC-Telco-78550 – 78797 (248 RAN Tickets)",
                "rfo_id": "RFO-Telco-2026-0902",
                "historical_mttr": "3.8 mins via remote gnb-cli (vs. 76m reboot)",
                "summary": (
                    "**97.6% match** to **Cluster 4 (`RFO-Telco-2026-0902`)**—waking 64T64R beams remotely via `gnb-cli` restores throughput in <2 mins."
                ),
            },
        }
        playbook = {
            "title": "RAN mMIMO Sleep Check & Forced 64T64R Wake-Up",
            "estimated_recovery_time": "1 min 20 secs",
            "risk_level": "Low (Hitless Remote Wake-Up — 0 Drops)",
            "steps": [
                {
                    "step": 1,
                    "title": "Check Cell Sleep Mode State",
                    "target_node": "GNB-DL-CP-408 / 409",
                    "description": "Query sleep state and active TRX chains on Cell 408.",
                    "command": "gnb-cli --cell 408 --action get-sleep-mode-state",
                },
                {
                    "step": 2,
                    "title": "Force Active 64T64R Mode",
                    "target_node": "GNB-DL-CP-408 / 409",
                    "description": "Override sleep lock and activate all 64T64R beams.",
                    "command": "gnb-cli --cell 408 --action override-energy-saving --state active",
                },
            ],
            "simulation_logs": [
                {"time": "12:31:15.040 IST", "type": "cmd", "text": "vi-noc@SMO-DL-NCR-01$ gnb-cli --cell 408 --action get-sleep-mode-state"},
                {"time": "12:31:15.490 IST", "type": "warn", "text": "  Cell 408: state=SLEEP_DEEP_LOCKED | active_trx=8T8R | PRB_Load=98.6%"},
                {"time": "12:31:16.120 IST", "type": "cmd", "text": "vi-noc@SMO-DL-NCR-01$ gnb-cli --cell 408 --action override-energy-saving --state active"},
                {"time": "12:31:17.950 IST", "type": "ok", "text": "✓ 64T64R Verified: 16/16 SSB beams active | PRB Load: 54.2%"},
                {"time": "12:31:18.610 IST", "type": "ok", "text": "✓ 12,000 Subscribers Restored: DL 298.4 Mbps"},
            ],
            "verification_badges": [
                "✓ Sleep Override: 64T64R Active",
                "✓ PRB Load: Normalized (54.2%)",
                "✓ 12,000 UEs: Restored (298 Mbps)",
            ],
        }
    else:
        # Tailored concise triage & playbook for INC-Telco-OPEN-004 .. INC-Telco-OPEN-100
        first_node = nodes.split(",")[0].strip()
        if domain == "Core":
            triage = {
                "confidence_score": "95.2%",
                "similarity_score": "95.2%",
                "matched_cluster": "Cluster 2: 5G SBI & PFCP Signaling Timeouts",
                "operational_impact": {
                    "headline": f"5G Core Signaling Degradation on {nodes} ({circle})",
                    "metrics": [
                        {"label": "Signaling Errors", "value": "11.8%", "status": "critical", "sub": f"{first_node} N4/SBI"},
                        {"label": "Impacted Sessions", "value": "9,400 UEs", "status": "warning", "sub": circle},
                        {"label": "N4 RTT Latency", "value": "184 ms", "status": "critical", "sub": "SLA: <15 ms"},
                        {"label": "Correlated RAN", "value": "14 gNodeBs", "status": "warning", "sub": "Setup Delays"},
                    ],
                    "narrative": f"{severity} in {circle} on `{nodes}`: {summary}",
                },
                "cross_domain_correlation": {
                    "headline": f"Core + Transport Correlation ({circle})",
                    "topology_path": [
                        {"layer": "RAN Access", "node": f"{circle} Cluster", "symptom": "Bearer Setup Delays", "state": "warn"},
                        {"layer": "IP Transport", "node": f"AGG-RTR-{CIRCLE_CODES.get(circle, 'MH-PUN')}-02", "symptom": "VLAN 402 MTU / Queue Drift", "state": "warn"},
                        {"layer": "5G Core", "node": nodes, "symptom": summary, "state": "critical"},
                    ],
                    "narrative": f"• Correlated Core signaling spikes on `{nodes}` with upstream transport MTU/queue drift across 14 `{circle}` gNodeBs.",
                },
                "hypothesized_root_cause": {
                    "protocol_reference": "3GPP TS 29.244 (N4 PFCP) & TS 29.500 (SBI)",
                    "diagnosis": f"PFCP peer congestion on `{first_node}` triggered by N4 transport sub-interface MTU/buffer mismatch.",
                },
                "historical_knowledge_match": {
                    "similarity_pct": "95.2%",
                    "matched_tickets": "INC-Telco-78115–78240 & 78500–78545",
                    "rfo_id": "RFO-Telco-2026-0719 / 0811",
                    "historical_mttr": "16.5 mins via CLI",
                    "summary": f"**95.2% match** to `{circle}` Core cluster—enforce 1500B MTU and reset PFCP peer on `{first_node}`.",
                },
            }
            playbook = {
                "title": f"5G Core N4 & MTU Remediation ({first_node})",
                "estimated_recovery_time": "2 mins 10 secs",
                "risk_level": "Low (Hitless Peer Reset)",
                "steps": [
                    {
                        "step": 1,
                        "title": "Verify VLAN 402 MTU",
                        "target_node": first_node,
                        "description": "Check interface MTU and N4 retry counters.",
                        "command": "show interface vlan402 | include MTU",
                    },
                    {
                        "step": 2,
                        "title": "Set 1500B Sub-Interface MTU",
                        "target_node": f"AGG-RTR-{CIRCLE_CODES.get(circle, 'MH-PUN')}-02",
                        "description": "Lock N4 signaling interface MTU to 1500B.",
                        "command": "configure terminal; interface vlan402; mtu 1500; commit",
                    },
                    {
                        "step": 3,
                        "title": "Reset PFCP Peer Pool",
                        "target_node": first_node,
                        "description": f"Reset hung PFCP association on {first_node}.",
                        "command": f"smf-cli --node {first_node} --action reset-pfcp-peer --peer-ip 10.160.44.12",
                    },
                ],
                "simulation_logs": [
                    {"time": "12:31:02.100 IST", "type": "cmd", "text": f"vi-noc@{first_node}# show interface vlan402 | include MTU"},
                    {"time": "12:31:02.600 IST", "type": "warn", "text": "  VLAN 402: PFCP Retries=14.2%, MTU drift detected"},
                    {"time": "12:31:03.400 IST", "type": "cmd", "text": f"vi-noc@{first_node}# configure terminal; interface vlan402; mtu 1500; commit"},
                    {"time": "12:31:04.500 IST", "type": "ok", "text": "✓ MTU Verified: 1500"},
                    {"time": "12:31:05.300 IST", "type": "cmd", "text": f"vi-noc@{first_node}$ smf-cli --node {first_node} --action reset-pfcp-peer --peer-ip 10.160.44.12"},
                    {"time": "12:31:07.200 IST", "type": "ok", "text": "✓ PFCP Heartbeat: OK | Call Drop Rate: Restored <0.02%"},
                ],
                "verification_badges": [
                    "✓ MTU Verified: 1500",
                    "✓ PFCP Heartbeat: OK",
                    "✓ Call Drop Rate: Restored <0.02%",
                ],
            }
        elif domain == "Transport":
            triage = {
                "confidence_score": "96.1%",
                "similarity_score": "96.1%",
                "matched_cluster": "Cluster 3: Optical Fiber Attenuation & DWDM Degradation",
                "operational_impact": {
                    "headline": f"Optical Transport Degradation on {nodes} ({circle})",
                    "metrics": [
                        {"label": "Optical Rx", "value": "-24.9 dBm", "status": "critical", "sub": "-4.1 dB vs baseline"},
                        {"label": "Packet Loss", "value": "5.4%", "status": "critical", "sub": f"{first_node} Te0/0/0/1"},
                        {"label": "BGP Flaps", "value": "9 / 10m", "status": "warning", "sub": "BFD Timeouts"},
                        {"label": "RAN Sites", "value": "16 gNodeBs", "status": "warning", "sub": f"{circle} Ring"},
                    ],
                    "narrative": f"{severity} transport degradation in {circle} on `{nodes}`: {summary}",
                },
                "cross_domain_correlation": {
                    "headline": f"L0 DWDM ➔ L3 MPLS/BGP Correlation ({circle})",
                    "topology_path": [
                        {"layer": "L0 Optical", "node": nodes, "symptom": "Attenuation (-24.9 dBm) & BER", "state": "critical"},
                        {"layer": "L3 MPLS", "node": first_node, "symptom": "BFD & BGP Route Flaps", "state": "critical"},
                        {"layer": "5G Backhaul", "node": f"{circle} Ring", "symptom": "GTP-U Jitter (16 gNodeBs)", "state": "warn"},
                    ],
                    "narrative": f"• Correlated `-24.9 dBm` optical Rx power on `{nodes}` with L3 BFD flaps (soft fiber fault above LOS cutoff).",
                },
                "hypothesized_root_cause": {
                    "protocol_reference": "ITU-T G.709 OTN & RFC 4090 (MPLS-TE FRR)",
                    "diagnosis": f"Soft optical attenuation on `{first_node}` (`TenGigE0/0/0/1`) corrupting BFD frames without triggering hard LOS.",
                },
                "historical_knowledge_match": {
                    "similarity_pct": "96.1%",
                    "matched_tickets": "INC-Telco-78301 – 78488 (188 Tickets)",
                    "rfo_id": "RFO-Telco-2026-0604",
                    "historical_mttr": "9.2 mins via MPLS-TE FRR",
                    "summary": f"**96.1% match** to `RFO-Telco-2026-0604`—switch traffic onto MPLS-TE protection Tunnel 104.",
                },
            }
            playbook = {
                "title": f"Optical Check & MPLS-TE FRR Switchover ({first_node})",
                "estimated_recovery_time": "1 min 45 secs",
                "risk_level": "Low (Hitless Protection Switchover)",
                "steps": [
                    {
                        "step": 1,
                        "title": "Check Optical Rx Power",
                        "target_node": first_node,
                        "description": f"Inspect DOM Rx power on {first_node}.",
                        "command": "show optical-power interface TenGigE0/0/0/1",
                    },
                    {
                        "step": 2,
                        "title": "Trigger MPLS-TE FRR (Tunnel 104)",
                        "target_node": first_node,
                        "description": "Switch traffic onto protection Tunnel 104.",
                        "command": "mpls traffic-eng fast-reroute trigger --tunnel-id 104",
                    },
                ],
                "simulation_logs": [
                    {"time": "12:31:02.100 IST", "type": "cmd", "text": f"vi-noc@{first_node}# show optical-power interface TenGigE0/0/0/1"},
                    {"time": "12:31:02.650 IST", "type": "warn", "text": "  Rx Power: -24.9 dBm [LOW ALARM] | Pre-FEC BER: 1.12e-03"},
                    {"time": "12:31:03.400 IST", "type": "cmd", "text": f"vi-noc@{first_node}# mpls traffic-eng fast-reroute trigger --tunnel-id 104"},
                    {"time": "12:31:05.000 IST", "type": "ok", "text": "✓ Tunnel 104 Active (Rx: -9.8 dBm) | Packet Loss: 0.00%"},
                ],
                "verification_badges": [
                    "✓ Tunnel 104 Active (-9.8 dBm)",
                    "✓ BGP Neighbor: Stable",
                    "✓ Packet Loss: 0.00%",
                ],
            }
        else:
            # RAN
            cell_num = "".join([c for c in first_node if c.isdigit()]) or "408"
            triage = {
                "confidence_score": "96.9%",
                "similarity_score": "96.9%",
                "matched_cluster": "Cluster 4: Massive MIMO Beamforming & Sleep Lockups",
                "operational_impact": {
                    "headline": f"RAN mMIMO Degradation on {nodes} ({circle})",
                    "metrics": [
                        {"label": "Affected UEs", "value": "8,600 UEs", "status": "critical", "sub": circle},
                        {"label": "Antenna State", "value": "8T8R Sleep Lock", "status": "critical", "sub": first_node},
                        {"label": "PRB Load", "value": "94.8%", "status": "warning", "sub": "DL <18 Mbps"},
                        {"label": "RRC Drops", "value": "3.8%", "status": "warning", "sub": "Baseline <0.25%"},
                    ],
                    "narrative": f"{severity} RAN degradation in {circle} on `{nodes}`: {summary}",
                },
                "cross_domain_correlation": {
                    "headline": f"RAN PM + Clean eCPRI Verification ({nodes})",
                    "topology_path": [
                        {"layer": "RAN AAU", "node": nodes, "symptom": summary, "state": "critical"},
                        {"layer": "Backhaul", "node": f"CSR-{CIRCLE_CODES.get(circle, 'DL-NCR')}-09", "symptom": "0% Packet Loss (2.4ms)", "state": "ok"},
                        {"layer": "5G Core UPF", "node": f"UPF-{CIRCLE_CODES.get(circle, 'DL-NCR')}-EDGE-01", "symptom": "N3 GTP-U Healthy", "state": "ok"},
                    ],
                    "narrative": f"• Clean N3/eCPRI transport metrics confirm software AAU sleep lockup on `{nodes}` (no hardware fault).",
                },
                "hypothesized_root_cause": {
                    "protocol_reference": "3GPP TS 38.300 & O-RAN WG2 Energy Saving",
                    "diagnosis": f"AAU v24.3 sleep-mode mutex deadlock on `{nodes}` preventing 64T64R wake-up under high PRB load.",
                },
                "historical_knowledge_match": {
                    "similarity_pct": "96.9%",
                    "matched_tickets": "INC-Telco-78550 – 78797 (248 RAN Tickets)",
                    "rfo_id": "RFO-Telco-2026-0902",
                    "historical_mttr": "4.1 mins via remote CLI",
                    "summary": f"**96.9% match** to `RFO-Telco-2026-0902`—run remote `gnb-cli` sleep override on `{first_node}`.",
                },
            }
            playbook = {
                "title": f"RAN Sleep Check & Forced 64T64R Override ({first_node})",
                "estimated_recovery_time": "1 min 20 secs",
                "risk_level": "Low (Hitless Remote CLI Override)",
                "steps": [
                    {
                        "step": 1,
                        "title": "Check Cell Sleep State",
                        "target_node": first_node,
                        "description": f"Query sleep state on cell {cell_num}.",
                        "command": f"gnb-cli --cell {cell_num} --action get-sleep-mode-state",
                    },
                    {
                        "step": 2,
                        "title": "Override Sleep Lock to 64T64R",
                        "target_node": first_node,
                        "description": f"Force cell {cell_num} into active 64T64R mode.",
                        "command": f"gnb-cli --cell {cell_num} --action override-energy-saving --state active",
                    },
                ],
                "simulation_logs": [
                    {"time": "12:31:02.100 IST", "type": "cmd", "text": f"vi-noc@SMO$ gnb-cli --cell {cell_num} --action get-sleep-mode-state"},
                    {"time": "12:31:02.550 IST", "type": "warn", "text": f"  Cell {cell_num}: state=SLEEP_LOCKED | PRB_Load=94.8%"},
                    {"time": "12:31:03.200 IST", "type": "cmd", "text": f"vi-noc@SMO$ gnb-cli --cell {cell_num} --action override-energy-saving --state active"},
                    {"time": "12:31:04.900 IST", "type": "ok", "text": f"✓ Cell {cell_num} ACTIVE_64T64R | PRB Load: 51.4%"},
                ],
                "verification_badges": [
                    f"✓ Cell {cell_num}: 64T64R Active",
                    "✓ PRB Load: Normalized (51.4%)",
                    "✓ Throughput: Restored",
                ],
            }

    rca_markdown = f"""# EXECUTIVE RCA REPORT — {tid}
**Circle:** `{circle}` | **Domain:** `{domain}` | **Severity:** `{severity}` | **Nodes:** `{nodes}`  
**Matched RFO:** `{triage["historical_knowledge_match"]["rfo_id"]}` ({triage["historical_knowledge_match"]["similarity_pct"]} Match) | **Recovery Time:** `{playbook["estimated_recovery_time"]}` *(vs. {triage["historical_knowledge_match"]["historical_mttr"]})*

## 1. Executive Summary
{triage["operational_impact"]["narrative"]}

## 2. Root Cause ({triage["hypothesized_root_cause"]["protocol_reference"]})
- **Diagnosis:** {triage["hypothesized_root_cause"]["diagnosis"]}
- **Historical Citations:** {triage["historical_knowledge_match"]["matched_tickets"]} (`{triage["historical_knowledge_match"]["rfo_id"]}`)

## 3. Executed Remediation & Verification
{chr(10).join([f"- **Step {s['step']} ({s['target_node']}):** `{s['command']}`" for s in playbook["steps"]])}
- **Post-Check Status:** {", ".join(playbook["verification_badges"])}

## 4. Preventive Guardrails (CAPA)
- **NetOps Config Guard:** Block sub-interface MTU drift (<1500B) & enforce proactive MPLS-TE optical thresholds via NETCONF.
- **Closed-Loop AI:** Auto-trigger `{triage["historical_knowledge_match"]["rfo_id"]}` playbook via Vertex AI + O-RAN SMO on signature match.
"""

    return {
        **ticket,
        "triage": triage,
        "playbook": playbook,
        "rca_markdown": rca_markdown,
    }


def _generate_open_tickets() -> List[Dict[str, Any]]:
    """Deterministically generates 100 Open Active Tickets:
    - 45 Open RAN Tickets
    - 30 Open Transport Tickets
    - 25 Open 5G Core Tickets
    - Includes exact showcase anchors INC-Telco-OPEN-001, INC-Telco-OPEN-002, INC-Telco-OPEN-003.
    """
    rng = random.Random(20261021)
    base_time = datetime(2026, 10, 20, 12, 25, 0, tzinfo=timezone.utc)

    raw_tickets: List[Dict[str, Any]] = [
        {
            "ticket_id": "INC-Telco-OPEN-001",
            "timestamp": "2026-10-20 12:18 IST",
            "circle": "Maharashtra/Pune",
            "domain": "Core",
            "domain_label": "5G Core",
            "severity": "P1-Critical",
            "status": "Investigating - L2 NOC",
            "affected_nodes": "UPF-MH-PUN-EDGE-01, SMF-MH-PUN-02",
            "alarm_summary": "Spike in VoNR call drops (>14%) and PDU session establishment timeouts on N4 interface.",
            "root_cause": "Pending Diagnostic Analysis",
            "resolution_steps": "Pending Diagnostic Analysis",
            "is_featured": True,
            "featured_badge": "Featured Anchor #1 • 5G Core / MTU Cascade",
        },
        {
            "ticket_id": "INC-Telco-OPEN-002",
            "timestamp": "2026-10-20 12:11 IST",
            "circle": "Mumbai",
            "domain": "Transport",
            "domain_label": "IP Transport",
            "severity": "P1-Critical",
            "status": "Investigating - L2 NOC",
            "affected_nodes": "PE-RTR-MUM-BKC-01, DWDM-MUM-POW-02",
            "alarm_summary": "Fiber span attenuation on secondary link causing packet loss and BGP neighbor flapping.",
            "root_cause": "Pending Diagnostic Analysis",
            "resolution_steps": "Pending Diagnostic Analysis",
            "is_featured": True,
            "featured_badge": "Featured Anchor #2 • Mumbai Optical Backbone",
        },
        {
            "ticket_id": "INC-Telco-OPEN-003",
            "timestamp": "2026-10-20 11:54 IST",
            "circle": "Delhi-NCR",
            "domain": "RAN",
            "domain_label": "RAN",
            "severity": "P2-Major",
            "status": "Open - Unassigned",
            "affected_nodes": "GNB-DL-CP-408, GNB-DL-CP-409",
            "alarm_summary": "Massive MIMO cell sleep mode lockup during evening peak hours affecting 12,000 subscribers.",
            "root_cause": "Pending Diagnostic Analysis",
            "resolution_steps": "Pending Diagnostic Analysis",
            "is_featured": True,
            "featured_badge": "Featured Anchor #3 • Delhi Urban mMIMO Lockup",
        },
    ]

    # Remaining 97 tickets: 44 RAN (total 45), 29 Transport (total 30), 24 Core (total 25)
    rem_domains: List[str] = (["RAN"] * 44) + (["Transport"] * 29) + (["Core"] * 24)
    rng.shuffle(rem_domains)

    ran_templates = [
        ("Massive MIMO beam tilt degradation and SSB RSRP drop (-112 dBm) on n78 sector", "P2-Major"),
        ("gNodeB SCTP multi-homing link flapping on N2 interface causing RRC connection drops", "P2-Major"),
        ("High PRB congestion (>96%) and VoNR packet scheduling delay during peak hour", "P3-Minor"),
        ("Antenna feedline VSWR alarm (1.94:1) and RF return loss degradation on sector 2", "P2-Major"),
        ("Massive MIMO 64T64R energy-saving sleep mode wake-up timeout impacting 6,500 UEs", "P1-Critical"),
    ]
    transport_templates = [
        ("DWDM optical power attenuation (-25.2 dBm) on metro ring span causing pre-FEC BER spike", "P1-Critical"),
        ("BGP route flapping and BFD control packet timeouts on aggregation trunk", "P2-Major"),
        ("Backhaul sub-interface VLAN 402 MTU mismatch (1420B) dropping DF-marked jumbo frames", "P1-Critical"),
        ("MPLS ring switchover packet discards and QoS DSCP EF egress buffer congestion", "P2-Major"),
    ]
    core_templates = [
        ("PFCP session timeouts on N4 interface between SMF and edge UPF causing bearer drops", "P1-Critical"),
        ("HTTP/2 SBI 503/504 service unavailable errors on N11 AMF-to-SMF signaling bus", "P2-Major"),
        ("AMF NAS registration storm (>34,000 req/s) following regional feeder power restore", "P1-Critical"),
        ("UPF GTP-U N3 packet discards and tail-drop counter surge on edge user-plane node", "P2-Major"),
        ("IMS P-CSCF SIP 500 Server Internal Error during VoNR call setup", "P3-Minor"),
    ]

    for i, dom in enumerate(rem_domains, start=4):
        tid = f"INC-Telco-OPEN-{i:03d}"
        circle = CIRCLES[(i * 3) % len(CIRCLES)]
        ccode = CIRCLE_CODES[circle]
        mins_ago = rng.randint(15, 23 * 60)
        ts_dt = base_time - timedelta(minutes=mins_ago)
        status = "Open - Unassigned" if i % 2 == 0 else "Investigating - L2 NOC"

        if dom == "RAN":
            tmpl, sev = ran_templates[i % len(ran_templates)]
            c1 = 200 + (i * 3) % 500
            nodes = f"GNB-{ccode}-{c1}, GNB-{ccode}-{c1 + 1}"
            d_label = "RAN"
        elif dom == "Transport":
            tmpl, sev = transport_templates[i % len(transport_templates)]
            nodes = f"PE-RTR-{ccode}-0{(i % 6) + 1}, DWDM-{ccode}-0{(i % 4) + 1}"
            d_label = "IP Transport"
        else:
            tmpl, sev = core_templates[i % len(core_templates)]
            nodes = f"UPF-{ccode}-EDGE-0{(i % 3) + 1}, SMF-{ccode}-0{(i % 2) + 1}"
            d_label = "5G Core"

        raw_tickets.append(
            {
                "ticket_id": tid,
                "timestamp": ts_dt.strftime("%Y-%m-%d %H:%M IST"),
                "circle": circle,
                "domain": dom,
                "domain_label": d_label,
                "severity": sev,
                "status": status,
                "affected_nodes": nodes,
                "alarm_summary": tmpl,
                "root_cause": "Pending Diagnostic Analysis",
                "resolution_steps": "Pending Diagnostic Analysis",
                "is_featured": False,
                "featured_badge": "",
            }
        )

    return [_build_open_ticket_details(t) for t in raw_tickets]


HISTORICAL_TICKETS: List[Dict[str, Any]] = _generate_historical_tickets()
OPEN_TICKETS: List[Dict[str, Any]] = _generate_open_tickets()
OPEN_TICKETS_MAP: Dict[str, Dict[str, Any]] = {t["ticket_id"]: t for t in OPEN_TICKETS}
HISTORICAL_TICKETS_MAP: Dict[str, Dict[str, Any]] = {t["ticket_id"]: t for t in HISTORICAL_TICKETS}
