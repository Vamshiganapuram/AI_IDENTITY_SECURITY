#!/usr/bin/env python3
"""Generate Project 1 threat-model files for SecureNova AI Identity Security."""
from __future__ import annotations

import csv
import json
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
OUT.mkdir(exist_ok=True)


def threat(title, ttype, severity, description, mitigation, tid):
    return {
        "ruleId": tid,
        "title": title,
        "type": ttype,
        "modelType": "STRIDE",
        "status": "Open",
        "severity": severity,
        "description": description,
        "mitigation": mitigation,
        "threatId": tid,
    }


def actor(id_, name, x, y, description, threats=None, out=False, reason=""):
    cell = {
        "type": "tm.Actor",
        "size": {"width": 170, "height": 80},
        "position": {"x": x, "y": y},
        "angle": 0,
        "id": id_,
        "z": 1,
        "hasOpenThreats": bool(threats),
        "description": description,
        "outOfScope": out,
        "reasonOutOfScope": reason,
        "providesAuthentication": True,
        "attrs": {
            "text": {"text": name},
            ".element-shape": {
                "class": "element-shape "
                + ("hasOpenThreats isInScope" if threats else "hasNoOpenThreats isInScope")
            },
            ".element-text": {"class": "element-text hasNoOpenThreats isInScope"},
        },
    }
    if threats:
        cell["threats"] = threats
    return cell


def process(id_, name, x, y, description, threats=None):
    cell = {
        "type": "tm.Process",
        "size": {"width": 140, "height": 140},
        "position": {"x": x, "y": y},
        "angle": 0,
        "id": id_,
        "z": 2,
        "hasOpenThreats": bool(threats),
        "description": description,
        "outOfScope": False,
        "reasonOutOfScope": "",
        "attrs": {
            "text": {"text": name},
            ".element-shape": {
                "class": "element-shape "
                + ("hasOpenThreats isInScope" if threats else "hasNoOpenThreats isInScope")
            },
            ".element-text": {"class": "element-text hasNoOpenThreats isInScope"},
        },
    }
    if threats:
        cell["threats"] = threats
    return cell


def store(id_, name, x, y, description, threats=None, creds=False):
    cell = {
        "type": "tm.Store",
        "size": {"width": 170, "height": 80},
        "position": {"x": x, "y": y},
        "angle": 0,
        "id": id_,
        "z": 3,
        "hasOpenThreats": bool(threats),
        "description": description,
        "outOfScope": False,
        "reasonOutOfScope": "",
        "isALog": False,
        "storesCredentials": creds,
        "isEncrypted": True,
        "isSigned": True,
        "attrs": {
            "text": {"text": name},
            ".element-shape": {
                "class": "element-shape "
                + ("hasOpenThreats isInScope" if threats else "hasNoOpenThreats isInScope")
            },
            ".element-text": {"class": "element-text hasNoOpenThreats isInScope"},
        },
    }
    if threats:
        cell["threats"] = threats
    return cell


def flow(id_, label, src, dst, description, protocol, public, vx, vy, threats=None, z=10):
    cell = {
        "type": "tm.Flow",
        "size": {"width": 10, "height": 10},
        "smooth": True,
        "source": {"id": src},
        "target": {"id": dst},
        "vertices": [{"x": vx, "y": vy}],
        "id": id_,
        "labels": [
            {
                "position": 0.5,
                "attrs": {"text": {"text": label, "font-weight": "400", "font-size": "small"}},
            }
        ],
        "z": z,
        "hasOpenThreats": bool(threats),
        "description": description,
        "protocol": protocol,
        "isEncrypted": True,
        "isPublicNetwork": public,
        "attrs": {
            ".marker-target": {"class": "marker-target hasNoOpenThreats isInScope"},
            ".connection": {"class": "connection hasNoOpenThreats isInScope"},
        },
    }
    if threats:
        cell["threats"] = threats
    return cell


def boundary(id_, x1, y1, x2, y2, mx, my, z=20):
    return {
        "type": "tm.Boundary",
        "size": {"width": 10, "height": 10},
        "smooth": True,
        "source": {"x": x1, "y": y1},
        "target": {"x": x2, "y": y2},
        "vertices": [{"x": mx, "y": my}],
        "id": id_,
        "z": z,
        "attrs": {},
        "description": "Trust boundary",
        "isTrustBoundary": True,
    }


def write_threat_dragon():
    agent_threats = [
        threat(
            "Spoofed AI agent presents stolen OBO token",
            "Spoofing",
            "High",
            "An attacker replays or forges an Auth0 on-behalf-of access token so a fake agent calls internal APIs and MCP tools as a legitimate customer-service agent. Trust boundary: User Layer -> Agent Layer.",
            "Bind tokens to agent instance (cnf/DPoP), short TTL, mTLS, Ed25519 request signing, deny implicit trust between agents.",
            "t-agent-spoof",
        ),
        threat(
            "Prompt injection discloses LLM API key and M2M secret",
            "Information disclosure",
            "High",
            "Direct or indirect prompt injection (OWASP LLM01) causes the orchestrator to echo secrets from environment, tool traces, or system prompt (LLM07). Trust boundary: Agent Layer -> LLM provider.",
            "Never place secrets in prompts; secret store + short-lived keys; output guardrails/JWT regex; tool-result redaction.",
            "t-agent-infodisc",
        ),
        threat(
            "Agent elevates from user-delegated scope to admin API scope",
            "Elevation of privilege",
            "High",
            "Confused-deputy / scope creep: the agent uses M2M client credentials with overlapping admin scopes after a spoofed identity or poisoned RAG instruction (OWASP LLM09).",
            "Separate M2M clients per privilege; Auth0 RBAC + API authorization; step-up re-auth for privileged tools; Zero Trust re-verification.",
            "t-agent-eop",
        ),
        threat(
            "Missing non-human identity audit trail",
            "Repudiation",
            "Medium",
            "Agent, MCP, and RAG actions are not bound to a durable actor ID, so operators cannot prove who invoked which tool.",
            "Signed audit events with agent_id, user_sub, client_id, tool name, and RAG chunk IDs; immutable log store.",
            "t-agent-repudiation",
        ),
        threat(
            "Unbounded tool loops exhaust LLM and API quotas",
            "Denial of service",
            "Medium",
            "A malicious prompt or poisoned chunk causes recursive MCP/tool calls, exhausting tokens and customer-service capacity.",
            "Rate limits per agent identity, max tool-call depth, circuit breakers, Auth0 suspicious IP throttling for user entry.",
            "t-agent-dos",
        ),
        threat(
            "RAG context or tool arguments tampered in transit/store",
            "Tampering",
            "High",
            "Chunks or MCP payloads are modified so the agent executes attacker-chosen tools (RAG poisoning / supply chain).",
            "Sign and hash chunks; ingest allow-list; MCP tool schema allow-list; integrity checks before retrieval.",
            "t-agent-tamper",
        ),
    ]

    cells = [
        actor(
            "id-human-user",
            "Human User\n(OIDC + PKCE)",
            40,
            360,
            "Customer or CSR authenticating via Auth0 Universal Login (OAuth 2.0 Authorization Code + PKCE / OIDC).",
        ),
        actor(
            "id-auth0",
            "Auth0 Tenant\n(IdP / SSO)",
            40,
            80,
            "Federated identity: Universal Login, Social and Enterprise connections, Attack Protection, MFA, M2M clients.",
        ),
        actor(
            "id-llm",
            "LLM Provider\n(API key)",
            1080,
            80,
            "External model service account authenticated with rotated LLM API keys. Out of org network but in scope for key governance.",
        ),
        process(
            "id-agent",
            "AI Agent\nOrchestrator",
            380,
            300,
            "Non-human identity that acts on behalf of the user: OBO user token + constrained M2M client. Calls REST, RAG, MCP, and LLM.",
            agent_threats,
        ),
        process(
            "id-api",
            "Internal REST\nAPI",
            720,
            80,
            "Resource server validating Auth0 JWTs. Audience-bound scopes for tickets and customer data.",
        ),
        process(
            "id-rag",
            "RAG Pipeline\nService Identity",
            720,
            300,
            "Workload identity that embeds, retrieves, and ranks knowledge chunks for the agent.",
        ),
        process(
            "id-mcp",
            "MCP Server\nIdentity",
            720,
            520,
            "Tool host authenticating agents via OAuth resource indicators and optional Ed25519-signed invocations.",
        ),
        store(
            "id-secrets",
            "Secrets / LLM API keys",
            380,
            520,
            "Short-lived LLM API keys and M2M client secrets. Credential store.",
            creds=True,
        ),
        store(
            "id-vectordb",
            "Vector DB / RAG chunks",
            1000,
            300,
            "Indexed knowledge and ticket-derived chunks. Integrity-sensitive.",
        ),
        store(
            "id-audit",
            "Identity audit log",
            1000,
            520,
            "Append-only identity events for humans, agents, OAuth clients, and MCP.",
        ),
        boundary("tb-user-agent", 250, 20, 250, 700, 250, 360, 40),
        boundary("tb-agent-internal", 620, 20, 620, 700, 620, 360, 41),
        boundary("tb-internal-ext", 960, 20, 960, 250, 960, 120, 42),
        flow(
            "f-user-auth0",
            "OIDC / PKCE login",
            "id-human-user",
            "id-auth0",
            "Authorization Code + PKCE; ID token + access token.",
            "HTTPS/OIDC",
            True,
            20,
            240,
            z=10,
        ),
        flow(
            "f-auth0-agent",
            "OBO + M2M JWT",
            "id-auth0",
            "id-agent",
            "User access token exchanged / constrained for agent; M2M client credentials token.",
            "HTTPS/OAuth2",
            False,
            240,
            200,
            z=11,
        ),
        flow(
            "f-user-agent",
            "Chat / task prompt",
            "id-human-user",
            "id-agent",
            "User natural-language task to agent. Crosses User Layer trust boundary.",
            "WSS/HTTPS",
            True,
            220,
            400,
            z=12,
        ),
        flow(
            "f-agent-api",
            "JWT API call",
            "id-agent",
            "id-api",
            "Agent calls internal REST with user-delegated or M2M JWT. Crosses Agent->Internal boundary.",
            "HTTPS/JWT",
            False,
            600,
            200,
            z=13,
        ),
        flow(
            "f-agent-rag",
            "Retrieve chunks",
            "id-agent",
            "id-rag",
            "Query embedding + top-k chunks returned into agent context.",
            "gRPC/HTTPS",
            False,
            600,
            360,
            z=14,
        ),
        flow(
            "f-rag-vec",
            "ANN search / ingest",
            "id-rag",
            "id-vectordb",
            "Pipeline service identity reads/writes embeddings.",
            "TLS",
            False,
            900,
            340,
            z=15,
        ),
        flow(
            "f-agent-mcp",
            "MCP tool invoke",
            "id-agent",
            "id-mcp",
            "Signed tool call with agent identity and user correlation ID.",
            "MCP/HTTPS",
            False,
            600,
            500,
            z=16,
        ),
        flow(
            "f-agent-llm",
            "Inference (API key)",
            "id-agent",
            "id-llm",
            "Prompt + tools to LLM. Must not include long-lived secrets.",
            "HTTPS",
            True,
            900,
            160,
            z=17,
        ),
        flow(
            "f-agent-secrets",
            "Fetch short-lived key",
            "id-agent",
            "id-secrets",
            "Runtime secret retrieval; rotation.",
            "HTTPS",
            False,
            420,
            500,
            z=18,
        ),
        flow(
            "f-mcp-audit",
            "Identity events",
            "id-mcp",
            "id-audit",
            "Tool invocation audit with agent and user IDs.",
            "TLS",
            False,
            900,
            560,
            z=19,
        ),
    ]

    model = {
        "version": "2.3.0",
        "summary": {
            "title": "SecureNova AI Identity System — Project 1 Threat Model",
            "owner": "AI Identity Security Analyst",
            "description": (
                "STRIDE threat model of SecureNova Inc. LLM customer-service platform. "
                "Identities: human users, AI agent, OAuth M2M client, LLM API key, "
                "RAG pipeline service identity, MCP server identity. "
                "Trust boundaries: User Layer | Agent Layer | Internal API Layer."
            ),
            "id": 0,
        },
        "detail": {
            "contributors": [{"name": "AI Identity Security Analyst"}],
            "diagrams": [
                {
                    "title": "AI Identity Data-Flow Diagram",
                    "thumbnail": "./public/content/images/thumbnail.stride.jpg",
                    "diagramType": "STRIDE",
                    "id": 0,
                    "diagramJson": {"cells": cells},
                    "size": {"height": 760, "width": 1280},
                    "cells": cells,
                }
            ],
            "diagramTop": 1,
            "reviewer": "SecureNova Security Team",
            "threatTop": 6,
        },
    }
    path = OUT / "SecureNova_AI_Identity_ThreatDragon.json"
    path.write_text(json.dumps(model, indent=2), encoding="utf-8")
    return path


def mx_cell(eid, value, x, y, w, h, style, parent="1"):
    return f'''        <mxCell id="{eid}" value="{escape(value)}" style="{style}" vertex="1" parent="{parent}">
          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>
        </mxCell>'''


def mx_edge(eid, source, target, label=""):
    lab = f' value="{escape(label)}"' if label else ""
    return f'''        <mxCell id="{eid}"{lab} style="endArrow=classic;html=1;rounded=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="{source}" target="{target}">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>'''


GOAL = "rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontStyle=1;fontSize=14;"
OR_N = "rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontStyle=1;"
AND_N = "rhombus;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontStyle=1;"
LEAF = "rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=11;"
MID = "rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=12;"


def tree_page(name, page_id, goal, nodes, edges):
    body = "\n".join(nodes + edges)
    return f'''  <diagram id="{page_id}" name="{name}">
    <mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="1100" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
{body}
      </root>
    </mxGraphModel>
  </diagram>'''


def write_drawio():
    # Tree 1 — LLM API Key Exfiltration
    t1_nodes = [
        mx_cell("g1", "GOAL: LLM API Key Exfiltration", 620, 40, 280, 60, GOAL),
        mx_cell("or1", "OR", 700, 130, 80, 70, OR_N),
        mx_cell("n1", "Prompt injection forces secret disclosure\n(OWASP LLM01 / LLM07)", 80, 240, 260, 70, MID),
        mx_cell("n2", "Steal from agent configuration / env", 400, 240, 240, 70, MID),
        mx_cell("n3", "Harvest from logs, traces, or RAG", 700, 240, 240, 70, MID),
        mx_cell("n4", "Compromise CI / secret store", 1000, 240, 240, 70, MID),
        mx_cell("or2", "OR", 160, 340, 80, 60, OR_N),
        mx_cell("and2", "AND", 460, 340, 80, 60, AND_N),
        mx_cell("or3", "OR", 760, 340, 80, 60, OR_N),
        mx_cell("or4", "OR", 1060, 340, 80, 60, OR_N),
        mx_cell("l1", "Direct injection: ignore policy, print env", 20, 460, 220, 60, LEAF),
        mx_cell("l2", "Indirect injection via ticket/RAG chunk", 250, 460, 230, 60, LEAF),
        mx_cell("l3", "Read process environment / .env", 400, 540, 200, 50, LEAF),
        mx_cell("l4", "Tool that dumps config to chat", 620, 540, 200, 50, LEAF),
        mx_cell("l5", "Debug traces include Authorization header", 700, 460, 240, 60, LEAF),
        mx_cell("l6", "RAG credential harvesting from runbooks", 960, 460, 230, 60, LEAF),
        mx_cell("l7", "Over-privileged deploy identity", 1000, 540, 220, 50, LEAF),
        mx_cell("l8", "Unrotated long-lived provider key", 1240, 540, 220, 50, LEAF),
        mx_cell("map1", "ATLAS: AML.T0051 Prompt Injection\n+ AML.T0083 Credentials from Agent Config\n+ AML.T0055 Unsecured Credentials", 520, 640, 420, 80, MID),
    ]
    t1_edges = [
        mx_edge("e1", "g1", "or1"),
        mx_edge("e2", "or1", "n1"),
        mx_edge("e3", "or1", "n2"),
        mx_edge("e4", "or1", "n3"),
        mx_edge("e5", "or1", "n4"),
        mx_edge("e6", "n1", "or2"),
        mx_edge("e7", "n2", "and2"),
        mx_edge("e8", "n3", "or3"),
        mx_edge("e9", "n4", "or4"),
        mx_edge("e10", "or2", "l1"),
        mx_edge("e11", "or2", "l2"),
        mx_edge("e12", "and2", "l3"),
        mx_edge("e13", "and2", "l4"),
        mx_edge("e14", "or3", "l5"),
        mx_edge("e15", "or3", "l6"),
        mx_edge("e16", "or4", "l7"),
        mx_edge("e17", "or4", "l8"),
        mx_edge("e18", "or2", "map1"),
    ]

    t2_nodes = [
        mx_cell("g2", "GOAL: Agent Identity Spoofing\n(elevated API scope)", 580, 30, 320, 70, GOAL),
        mx_cell("orA", "OR", 700, 130, 80, 70, OR_N),
        mx_cell("a1", "Abuse valid Auth0 tokens", 80, 230, 220, 60, MID),
        mx_cell("a2", "Forge / weaken JWT validation", 360, 230, 230, 60, MID),
        mx_cell("a3", "Impersonate MCP or agent peer", 660, 230, 230, 60, MID),
        mx_cell("a4", "Confused deputy / scope creep", 960, 230, 240, 60, MID),
        mx_cell("orB", "OR", 150, 330, 80, 60, OR_N),
        mx_cell("orC", "OR", 430, 330, 80, 60, OR_N),
        mx_cell("andD", "AND", 730, 330, 80, 60, AND_N),
        mx_cell("andE", "AND", 1040, 330, 80, 60, AND_N),
        mx_cell("b1", "Steal user OBO access token (XSS/logs)", 20, 450, 230, 55, LEAF),
        mx_cell("b2", "Steal M2M client_id + secret", 260, 450, 210, 55, LEAF),
        mx_cell("b3", "alg=none / wrong JWKS audience", 360, 530, 220, 55, LEAF),
        mx_cell("b4", "Replay expired token (no nbf/exp check)", 600, 530, 240, 55, LEAF),
        mx_cell("b5", "Stand up rogue MCP with trusted name", 660, 450, 240, 55, LEAF),
        mx_cell("b6", "No agent-to-agent re-verification", 920, 450, 230, 55, LEAF),
        mx_cell("b7", "M2M client has admin + user scopes", 960, 530, 240, 55, LEAF),
        mx_cell("b8", "RAG tells agent to call privileged tool", 1220, 530, 250, 55, LEAF),
        mx_cell("map2", "ATLAS: AML.T0073 Impersonation\n+ AML.T0012 Valid Accounts\nOWASP LLM09 / over-privileged agent", 540, 640, 400, 80, MID),
    ]
    t2_edges = [
        mx_edge("f1", "g2", "orA"),
        mx_edge("f2", "orA", "a1"),
        mx_edge("f3", "orA", "a2"),
        mx_edge("f4", "orA", "a3"),
        mx_edge("f5", "orA", "a4"),
        mx_edge("f6", "a1", "orB"),
        mx_edge("f7", "a2", "orC"),
        mx_edge("f8", "a3", "andD"),
        mx_edge("f9", "a4", "andE"),
        mx_edge("f10", "orB", "b1"),
        mx_edge("f11", "orB", "b2"),
        mx_edge("f12", "orC", "b3"),
        mx_edge("f13", "orC", "b4"),
        mx_edge("f14", "andD", "b5"),
        mx_edge("f15", "andD", "b6"),
        mx_edge("f16", "andE", "b7"),
        mx_edge("f17", "andE", "b8"),
        mx_edge("f18", "orA", "map2"),
    ]

    t3_nodes = [
        mx_cell("g3", "GOAL: RAG Chunk Poisoning\n(manipulate agent behavior)", 560, 30, 340, 70, GOAL),
        mx_cell("orX", "OR", 700, 130, 80, 70, OR_N),
        mx_cell("c1", "Write poisoned document into ingest path", 60, 230, 260, 60, MID),
        mx_cell("c2", "Supply-chain / third-party KB compromise", 400, 230, 260, 60, MID),
        mx_cell("c3", "Adversarial embedding / retrieval hijack", 740, 230, 260, 60, MID),
        mx_cell("c4", "Indirect prompt in user-sourced content", 1080, 230, 280, 60, MID),
        mx_cell("andP", "AND", 150, 330, 80, 60, AND_N),
        mx_cell("orQ", "OR", 500, 330, 80, 60, OR_N),
        mx_cell("andR", "AND", 800, 330, 80, 60, AND_N),
        mx_cell("orS", "OR", 1160, 330, 80, 60, OR_N),
        mx_cell("d1", "Compromise RAG pipeline identity", 20, 450, 220, 55, LEAF),
        mx_cell("d2", "Bypass ingest allow-list / no signing", 250, 450, 230, 55, LEAF),
        mx_cell("d3", "Poison vendor FAQ / connector", 400, 530, 230, 55, LEAF),
        mx_cell("d4", "Malicious PR into knowledge repo", 650, 530, 230, 55, LEAF),
        mx_cell("d5", "Craft chunk that always ranks top-k", 740, 450, 240, 55, LEAF),
        mx_cell("d6", "No integrity hash on stored chunks", 1000, 450, 230, 55, LEAF),
        mx_cell("d7", "Support ticket with hidden instructions", 1080, 530, 250, 55, LEAF),
        mx_cell("d8", "Email/web page fetched into index", 1340, 530, 220, 55, LEAF),
        mx_cell("map3", "ATLAS: AML.T0070 RAG Poisoning\n+ AML.T0051.001 Indirect Prompt Injection\nOWASP LLM08 / LLM supply chain", 540, 640, 420, 80, MID),
    ]
    t3_edges = [
        mx_edge("h1", "g3", "orX"),
        mx_edge("h2", "orX", "c1"),
        mx_edge("h3", "orX", "c2"),
        mx_edge("h4", "orX", "c3"),
        mx_edge("h5", "orX", "c4"),
        mx_edge("h6", "c1", "andP"),
        mx_edge("h7", "c2", "orQ"),
        mx_edge("h8", "c3", "andR"),
        mx_edge("h9", "c4", "orS"),
        mx_edge("h10", "andP", "d1"),
        mx_edge("h11", "andP", "d2"),
        mx_edge("h12", "orQ", "d3"),
        mx_edge("h13", "orQ", "d4"),
        mx_edge("h14", "andR", "d5"),
        mx_edge("h15", "andR", "d6"),
        mx_edge("h16", "orS", "d7"),
        mx_edge("h17", "orS", "d8"),
        mx_edge("h18", "orX", "map3"),
    ]

    xml = (
        '<mxfile host="app.diagrams.net" modified="2026-08-19T00:00:00.000Z" agent="SecureNova-Capstone" version="22.1.0" type="device">\n'
        + tree_page("Attack Tree 1 - LLM API Key Exfiltration", "page-keyexfil", "g", t1_nodes, t1_edges)
        + "\n"
        + tree_page("Attack Tree 2 - Agent Identity Spoofing", "page-spoof", "g", t2_nodes, t2_edges)
        + "\n"
        + tree_page("Attack Tree 3 - RAG Chunk Poisoning", "page-rag", "g", t3_nodes, t3_edges)
        + "\n</mxfile>\n"
    )
    path = OUT / "SecureNova_Attack_Trees.drawio"
    path.write_text(xml, encoding="utf-8")
    # also split copies for easier open-all-nodes screenshots
    (OUT / "AttackTree1_LLM_API_Key_Exfiltration.drawio").write_text(
        '<mxfile host="app.diagrams.net">\n'
        + tree_page("Attack Tree 1 - LLM API Key Exfiltration", "page-keyexfil", "g", t1_nodes, t1_edges)
        + "\n</mxfile>\n",
        encoding="utf-8",
    )
    (OUT / "AttackTree2_Agent_Identity_Spoofing.drawio").write_text(
        '<mxfile host="app.diagrams.net">\n'
        + tree_page("Attack Tree 2 - Agent Identity Spoofing", "page-spoof", "g", t2_nodes, t2_edges)
        + "\n</mxfile>\n",
        encoding="utf-8",
    )
    (OUT / "AttackTree3_RAG_Chunk_Poisoning.drawio").write_text(
        '<mxfile host="app.diagrams.net">\n'
        + tree_page("Attack Tree 3 - RAG Chunk Poisoning", "page-rag", "g", t3_nodes, t3_edges)
        + "\n</mxfile>\n",
        encoding="utf-8",
    )
    return path


STRIDE_ROWS = [
    # flow, S, T, R, I, D, E
    (
        "F1 Human user → Auth0 (OIDC+PKCE)",
        "Credential stuffing / fake Universal Login (phishing SSO)",
        "Tamper authorize redirect / PKCE verifier",
        "Login success without MFA log binding",
        "Auth code leak in Referer / browser history",
        "Auth0 brute-force without Attack Protection",
        "Bypass MFA / hijack enterprise connection",
    ),
    (
        "F2 Human user → AI agent (chat prompt)",
        "Attacker session as customer (stolen cookie)",
        "Modify prompt in transit (MITM if TLS broken)",
        "User denies sending jailbreak prompt",
        "PII in chat captured by third-party plugin",
        "Prompt flood / token exhaustion",
        "User claims CSR role in prompt (role elevation LLM01)",
    ),
    (
        "F3 Auth0 → Agent (OBO user JWT)",
        "Stolen bearer token used by rogue agent",
        "Rewrite scopes in unsigned/weak JWT",
        "No token-use audit (repudiation of API calls)",
        "JWT in browser storage / HAR files",
        "Token endpoint flooded (client credentials)",
        "Token with extra audience/admin scopes",
    ),
    (
        "F4 Agent M2M client → Auth0 token endpoint",
        "Leaked client_secret impersonates M2M client",
        "Substitute token request parameters",
        "M2M minting not attributed to workload",
        "Client secret in repo or prompt context",
        "Credential stuffing against M2M client",
        "M2M client authorized to privileged APIs",
    ),
    (
        "F5 Agent → Internal REST API",
        "Spoofed agent JWT accepted (wrong JWKS)",
        "Tamper request body after authn",
        "API logs lack agent_id / user_sub",
        "Excessive customer PII in responses to model",
        "High-rate ticket export",
        "IDOR / scope confusion (confused deputy)",
    ),
    (
        "F6 Agent → RAG pipeline",
        "Rogue service uses stolen RAG workload identity",
        "Inject/alter query embeddings",
        "Retrievals not logged with chunk IDs",
        "Sensitive runbooks retrieved into context",
        "Retrieval storms / vector DB saturation",
        "Query filter bypass returns restricted tenants",
    ),
    (
        "F7 RAG pipeline → Vector DB",
        "Stolen DB creds as pipeline identity",
        "Overwrite embeddings (chunk poisoning)",
        "Ingest jobs without signed operator identity",
        "Dump all chunks including secrets",
        "Drop index / resource exhaustion",
        "Write path used by read-only identity",
    ),
    (
        "F8 Agent → MCP server tools",
        "Fake MCP peer / tool name spoofing",
        "Tool-argument injection / schema abuse",
        "Tool calls without signed audit",
        "Tool returns secrets into LLM context",
        "Recursive tool loop DoS",
        "Unallowlisted tool with admin side effects",
    ),
    (
        "F9 Agent → LLM provider (API key)",
        "Other tenant/key used if key leaked",
        "Prompt/template tampering in gateway",
        "Provider logs not correlated to agent_id",
        "System prompt / key echo (LLM07)",
        "Cost/availability abuse via long context",
        "Model asked to invoke privileged tools",
    ),
    (
        "F10 MCP / Agent → Audit log store",
        "Attacker writes fake ‘success’ audit as agent",
        "Alter or delete audit events",
        "Unsigned logs enable repudiation",
        "Audit store contains raw tokens",
        "Log flood hides identity incidents",
        "Disable logging via admin API",
    ),
    (
        "F11 Secrets store → Agent (LLM key rotation)",
        "Workload identity spoof to checkout keys",
        "Replace secret with attacker-controlled key",
        "Key checkout not attributable",
        "Key material logged by sidecar",
        "Lock out rotation (availability of inference)",
        "Agent obtains prod + admin provider keys",
    ),
    (
        "F12 Enterprise SSO IdP → Auth0 connection",
        "Federated IdP impersonation",
        "SAML/OIDC assertion tampering",
        "SSO events not in SecureNova SIEM",
        "Group claims leak internal org chart",
        "IdP outage blocks all agents",
        "Wrong group → admin role mapping",
    ),
]


RISKS = [
    {
        "id": "R-01",
        "threat": "LLM API key exfiltration via prompt injection",
        "asset": "LLM API key / model service account",
        "flow": "F9 / Agent identity",
        "stride": "Information Disclosure",
        "atlas": "AML.T0051",
        "owasp": "LLM01, LLM07",
        "L": 5,
        "I": 5,
        "owner": "AI Platform / Secrets Owner",
        "treatment": "Mitigate: secret isolation, output guardrails, 1h key rotation",
    },
    {
        "id": "R-02",
        "threat": "Agent identity spoofing to elevated API scope",
        "asset": "OAuth M2M client + user OBO token",
        "flow": "F3, F4, F5",
        "stride": "Spoofing / Elevation of Privilege",
        "atlas": "AML.T0073",
        "owasp": "LLM09",
        "L": 4,
        "I": 5,
        "owner": "IAM / Auth0 Administrator",
        "treatment": "Mitigate: DPoP/cnf, split clients, Auth0 RBAC, MFA on humans",
    },
    {
        "id": "R-03",
        "threat": "RAG chunk poisoning manipulating agent tools",
        "asset": "Vector DB / RAG pipeline identity",
        "flow": "F6, F7",
        "stride": "Tampering",
        "atlas": "AML.T0070",
        "owasp": "LLM08 / supply chain",
        "L": 4,
        "I": 4,
        "owner": "Knowledge Engineering Lead",
        "treatment": "Mitigate: signed chunks, dual-control ingest, retrieval allow-list",
    },
    {
        "id": "R-04",
        "threat": "Indirect prompt injection from tickets into RAG",
        "asset": "AI agent context window",
        "flow": "F2, F6",
        "stride": "Tampering / EoP",
        "atlas": "AML.T0051.001",
        "owasp": "LLM01",
        "L": 5,
        "I": 4,
        "owner": "Agent Runtime Owner",
        "treatment": "Mitigate: untrusted-content delimiters, tool confirmation",
    },
    {
        "id": "R-05",
        "threat": "MCP tool spoofing / unauthorized tool invocation",
        "asset": "MCP server identity",
        "flow": "F8",
        "stride": "Spoofing / EoP",
        "atlas": "AML.T0073 / tool invocation",
        "owasp": "LLM09",
        "L": 3,
        "I": 5,
        "owner": "MCP Platform Owner",
        "treatment": "Mitigate: mTLS, tool allow-list, Ed25519 bind, Zero Trust re-auth",
    },
    {
        "id": "R-06",
        "threat": "M2M client secret in prompt or repository",
        "asset": "OAuth M2M client",
        "flow": "F4, F11",
        "stride": "Information Disclosure",
        "atlas": "AML.T0083 / AML.T0055",
        "owasp": "LLM02 / LLM07",
        "L": 4,
        "I": 5,
        "owner": "Secrets Owner",
        "treatment": "Mitigate: no secrets in prompts; vault; rotate 24h",
    },
    {
        "id": "R-07",
        "threat": "Missing audit for non-human identities",
        "asset": "Audit log store",
        "flow": "F10",
        "stride": "Repudiation",
        "atlas": "AML.T0012 supporting",
        "owasp": "LLM10 (unbounded agency) / logging",
        "L": 4,
        "I": 3,
        "owner": "SOC / Detection Engineering",
        "treatment": "Mitigate: mandatory identity event schema + SIEM use cases",
    },
    {
        "id": "R-08",
        "threat": "Auth0 brute force / credential stuffing on Universal Login",
        "asset": "Human user identities",
        "flow": "F1",
        "stride": "Spoofing / DoS",
        "atlas": "AML.T0012 Valid Accounts",
        "owasp": "LLM08 adjacent (account takeover)",
        "L": 4,
        "I": 4,
        "owner": "Auth0 Administrator",
        "treatment": "Mitigate: Attack Protection, MFA, suspicious IP throttling",
    },
    {
        "id": "R-09",
        "threat": "System prompt / policy extraction",
        "asset": "Agent system prompt & guardrail policy",
        "flow": "F9",
        "stride": "Information Disclosure",
        "atlas": "AML.T0056",
        "owasp": "LLM07",
        "L": 3,
        "I": 3,
        "owner": "Agent Runtime Owner",
        "treatment": "Accept residual; monitor; do not store secrets in prompt",
    },
    {
        "id": "R-10",
        "threat": "Recursive MCP/tool loop denial of service",
        "asset": "Agent + LLM quota + APIs",
        "flow": "F8, F9",
        "stride": "Denial of Service",
        "atlas": "AML.T0048 related availability",
        "owasp": "LLM10",
        "L": 3,
        "I": 4,
        "owner": "SRE / AI Platform",
        "treatment": "Mitigate: depth limits, per-identity rate limits, budgets",
    },
    {
        "id": "R-11",
        "threat": "Enterprise SSO group-to-role mis-mapping",
        "asset": "Human admin / CSR roles",
        "flow": "F12",
        "stride": "Elevation of Privilege",
        "atlas": "AML.T0012",
        "owasp": "Access control",
        "L": 2,
        "I": 5,
        "owner": "IAM / Auth0 Administrator",
        "treatment": "Mitigate: least privilege mappings, access reviews",
    },
    {
        "id": "R-12",
        "threat": "PII leakage from API responses into model logs",
        "asset": "Customer PII",
        "flow": "F5, F9",
        "stride": "Information Disclosure",
        "atlas": "AML.T0057 LLM Data Leakage",
        "owasp": "LLM06 / LLM02",
        "L": 4,
        "I": 4,
        "owner": "Privacy + AI Platform",
        "treatment": "Mitigate: DLP/guardrails, minimize fields, provider ZDR",
    },
]


def write_csvs():
    stride_path = OUT / "STRIDE_Threat_Matrix.csv"
    with stride_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "Identity flow",
                "Spoofing (S)",
                "Tampering (T)",
                "Repudiation (R)",
                "Information Disclosure (I)",
                "Denial of Service (D)",
                "Elevation of Privilege (E)",
            ]
        )
        w.writerows(STRIDE_ROWS)

    risk_path = OUT / "Risk_Register.csv"
    with risk_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "Risk ID",
                "Threat",
                "Asset / identity",
                "Identity flow",
                "STRIDE",
                "MITRE ATLAS",
                "OWASP LLM",
                "Likelihood (1-5)",
                "Impact (1-5)",
                "Risk Score (L×I)",
                "Rank",
                "Owner",
                "Treatment",
            ]
        )
        ranked = sorted(RISKS, key=lambda r: r["L"] * r["I"], reverse=True)
        for i, r in enumerate(ranked, 1):
            w.writerow(
                [
                    r["id"],
                    r["threat"],
                    r["asset"],
                    r["flow"],
                    r["stride"],
                    r["atlas"],
                    r["owasp"],
                    r["L"],
                    r["I"],
                    r["L"] * r["I"],
                    i,
                    r["owner"],
                    r["treatment"],
                ]
            )
    return stride_path, risk_path


def write_html_workbook():
    """Excel-openable HTML with two sheets simulated as one workbook page."""
    # ranked risks
    ranked = sorted(RISKS, key=lambda r: r["L"] * r["I"], reverse=True)

    def td(x):
        return f"<td>{escape(str(x))}</td>"

    stride_trs = []
    for row in STRIDE_ROWS:
        stride_trs.append("<tr>" + "".join(td(c) for c in row) + "</tr>")

    risk_trs = []
    for i, r in enumerate(ranked, 1):
        score = r["L"] * r["I"]
        color = "#f8cecc" if score >= 20 else "#fff2cc" if score >= 12 else "#d5e8d4"
        risk_trs.append(
            f'<tr style="background:{color}">'
            + td(r["id"])
            + td(r["threat"])
            + td(r["asset"])
            + td(r["flow"])
            + td(r["stride"])
            + td(r["atlas"])
            + td(r["owasp"])
            + td(r["L"])
            + td(r["I"])
            + td(score)
            + td(i)
            + td(r["owner"])
            + td(r["treatment"])
            + "</tr>"
        )

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"/>
<title>SecureNova Project 1 — STRIDE Matrix and Risk Register</title>
<style>
body {{ font-family: Calibri, Arial, sans-serif; margin: 16px; }}
h1,h2 {{ color: #1a365d; }}
table {{ border-collapse: collapse; font-size: 11px; width: 100%; margin-bottom: 28px; }}
th, td {{ border: 1px solid #4a5568; padding: 6px; vertical-align: top; }}
th {{ background: #1a365d; color: #fff; }}
caption {{ font-weight: bold; text-align: left; margin: 8px 0; font-size: 14px; }}
.note {{ font-size: 12px; color: #2d3748; }}
</style></head>
<body>
<h1>SecureNova Inc. — AI Identity Security Capstone</h1>
<h2>Project 1: STRIDE Threat Matrix (all six categories × identity flows)</h2>
<p class="note">Scoring context: Likelihood × Impact (1–5) is applied in the Risk Register. Trust boundaries: User Layer | Agent Layer | Internal API Layer.</p>
<table>
<caption>STRIDE Threat Matrix — SecureNova AI Identity Flows</caption>
<tr>
<th>Identity flow</th><th>Spoofing</th><th>Tampering</th><th>Repudiation</th>
<th>Information Disclosure</th><th>Denial of Service</th><th>Elevation of Privilege</th>
</tr>
{''.join(stride_trs)}
</table>
<h2>Risk Register (12 threats, scored and ranked)</h2>
<p class="note">Formula: Risk Score = Likelihood × Impact. Rank 1 is highest score. Owners assigned for governance.</p>
<table>
<caption>AI Identity Risk Register — ranked</caption>
<tr>
<th>Risk ID</th><th>Threat</th><th>Asset / identity</th><th>Flow</th><th>STRIDE</th>
<th>MITRE ATLAS</th><th>OWASP LLM</th><th>L</th><th>I</th><th>Score</th>
<th>Rank</th><th>Owner</th><th>Treatment</th>
</tr>
{''.join(risk_trs)}
</table>
</body></html>
"""
    path = OUT / "STRIDE_Matrix_and_Risk_Register.xls"
    # Excel opens HTML if named .xls in many environments; also save .html
    path.write_text(html, encoding="utf-8")
    (OUT / "STRIDE_Matrix_and_Risk_Register.html").write_text(html, encoding="utf-8")
    return path


def write_guide():
    text = r"""# Project 1 — Screenshot Playbook (Mettl)

Take **full-screen** shots. The **browser URL** or window title must be visible. Put them in **one Word document**, titled, in this order, then **Save as PDF**.

## Files to open

| # | Required screenshot | Open this |
|---|---------------------|-----------|
| 1 | Threat Dragon DFD | Import `deliverables/SecureNova_AI_Identity_ThreatDragon.json` into https://www.threatdragon.com |
| 2 | Threat Dragon STRIDE panel | Click the **AI Agent Orchestrator** process (red/open threats) → Threats panel shows ≥3 STRIDE items |
| 3 | Attack tree 1 | https://app.diagrams.net → Open `AttackTree1_LLM_API_Key_Exfiltration.drawio` |
| 4 | Attack tree 2 | Open `AttackTree2_Agent_Identity_Spoofing.drawio` |
| 5 | Attack tree 3 | Open `AttackTree3_RAG_Chunk_Poisoning.drawio` |
| 6 | STRIDE matrix | Open `STRIDE_Matrix_and_Risk_Register.html` in Excel or browser (full table) |
| 7 | Risk register | Same file — scroll to Risk Register (≥10 scored rows) |
| 8 | MITRE ATLAS | https://atlas.mitre.org/techniques/AML.T0051 (LLM Prompt Injection) — maps to Attack Tree 1 |

## Threat Dragon import

1. Go to https://www.threatdragon.com
2. Create / open a local model (skip GitHub login if offered — use **local** / download).
3. **Open** / import the JSON from `deliverables`.
4. Confirm three trust-boundary lines: **User Layer** (left), **Agent Layer** (center), **Internal API Layer** (right).
5. Screenshot 1: entire DFD with URL bar.
6. Click **AI Agent Orchestrator**. Screenshot 2: threat list with Spoofing, Information Disclosure, Elevation of Privilege (and others).

If import fails on a newer Threat Dragon (x6 format), recreate using the labels in the Word report DFD description — same components.

## draw.io

1. https://app.diagrams.net → **Open Existing Diagram** → Device → select the `.drawio` file.
2. View → **Fit** so **all nodes are visible**, including the ATLAS mapping box at the bottom.
3. URL must show `app.diagrams.net`.

## ATLAS (required AML.TXXXX page)

Primary page for the ZIP screenshots:

- Attack Tree 1 → **AML.T0051** LLM Prompt Injection  
  https://atlas.mitre.org/techniques/AML.T0051

Also record in the report (not extra required screenshots unless asked):

- Attack Tree 2 → **AML.T0073** Impersonation  
  https://atlas.mitre.org/techniques/AML.T0073
- Attack Tree 3 → **AML.T0070** RAG Poisoning  
  https://atlas.mitre.org/techniques/AML.T0070

## Word → PDF → ZIP

1. One `.docx` with titled screenshots in order 1–8.
2. File → Save As → PDF (`Project1_Threat_Model.pdf`).
3. ZIP that PDF (later add other project PDFs if the course requires one ZIP for all projects).
4. Upload ZIP to Mettl.
"""
    (ROOT / "SCREENSHOT_PLAYBOOK.md").write_text(text, encoding="utf-8")


def write_report_md():
    ranked = sorted(RISKS, key=lambda r: r["L"] * r["I"], reverse=True)
    lines = [
        "# Project 1 — Threat Model the AI Identity System",
        "",
        "**Course:** AI Identity Security Capstone  ",
        "**Organization:** SecureNova Inc.  ",
        "**Role:** AI Identity Security Analyst  ",
        "**Model:** LLM-powered customer service (Auth0, RAG, MCP, REST APIs)",
        "",
        "## 1. Threat modelling — identity inventory",
        "",
        "SecureNova’s platform has **human and non-human identities**. Each identity has an authentication mechanism and a least-privilege level.",
        "",
        "| Identity type | Authentication mechanism | Privilege level |",
        "|---------------|--------------------------|-----------------|",
        "| Human user (customer) | Auth0 Universal Login; OAuth 2.0 Authorization Code + **PKCE**; **OIDC** ID token | Own profile, own tickets, own chat session. No API-key or M2M secret access. |",
        "| Human user (CSR / supervisor) | Same + **MFA**; Enterprise Connection SSO | Assigned queue; no LLM provider keys; no Auth0 tenant admin. |",
        "| Human user (security admin) | OIDC + MFA + Auth0 dashboard RBAC | Tenant attack-protection config and audit review. No standing production LLM keys in browser. |",
        "| AI agent (customer-service orchestrator) | **On-Behalf-Of** user access token + confidential **M2M** client credentials (short-lived JWT) | Delegated user scopes **plus** constrained tool scopes. Cannot mint admin tokens. |",
        "| OAuth M2M client | Client Credentials grant against Auth0; JWT `aud` = internal APIs | `tickets:read`, `tickets:write`, `kb:search` only. Separate client for admin jobs. |",
        "| LLM API key (model service account) | Provider secret from vault; **rotated** (e.g. hourly/daily) | Inference only. Never placed in prompts, RAG, or MCP responses. |",
        "| RAG pipeline service identity | Workload identity / M2M JWT to vector DB | Read for retrieve; **separate** identity for ingest/write. |",
        "| MCP server identity | OAuth resource server + mTLS; optional **Ed25519** invocation signatures | Execute **allow-listed** tools only; no implicit trust of peer agents (Zero Trust re-verification). |",
        "",
        "### Trust boundaries",
        "",
        "1. **User Layer** — browsers, Universal Login, social/enterprise IdPs, public chat channel.",
        "2. **Agent Layer** — orchestrator, secret checkout, prompt assembly, LLM calls.",
        "3. **Internal API Layer** — REST resource servers, RAG/vector DB, MCP tools, audit store.",
        "",
        "STRIDE is applied on every flow that **crosses** these boundaries (see matrix).",
        "",
        "## 2. STRIDE matrix and Threat Dragon DFD",
        "",
        "The OWASP Threat Dragon model is `deliverables/SecureNova_AI_Identity_ThreatDragon.json`.",
        "",
        "The **AI Agent Orchestrator** process is populated with all six STRIDE categories (screenshot the threat panel on that process).",
        "",
        "Full flow-by-flow STRIDE text is in `deliverables/STRIDE_Threat_Matrix.csv` and the HTML workbook.",
        "",
        "## 3. Attack trees (draw.io) and scoring",
        "",
        "Formula used everywhere: **Risk Score = Likelihood × Impact** (each 1–5).",
        "",
        "| Tree | Goal | Highest path (illustrative) | L | I | Score | Closest ATLAS ID |",
        "|------|------|-----------------------------|---|---|-------|------------------|",
        "| 1 | LLM API key exfiltration via prompt injection | Direct/indirect injection + secrets in runtime context | 5 | 5 | **25** | **AML.T0051** |",
        "| 2 | Agent identity spoofing → elevated API scope | Stolen OBO/M2M material + over-broad client | 4 | 5 | **20** | **AML.T0073** |",
        "| 3 | RAG chunk poisoning | Ingest write + unsigned chunks | 4 | 4 | **16** | **AML.T0070** |",
        "",
        "Supporting techniques to cite in narrative: AML.T0083 (credentials from agent configuration), AML.T0055 (unsecured credentials), AML.T0012 (valid accounts), AML.T0051.001 (indirect prompt injection).",
        "",
        "## 4. MITRE ATLAS mapping",
        "",
        "| Attack path | Closest technique | URL |",
        "|-------------|-------------------|-----|",
        "| Prompt injection → key leak | AML.T0051 LLM Prompt Injection | https://atlas.mitre.org/techniques/AML.T0051 |",
        "| Spoof agent / abuse tokens | AML.T0073 Impersonation | https://atlas.mitre.org/techniques/AML.T0073 |",
        "| Poison retrieval corpus | AML.T0070 RAG Poisoning | https://atlas.mitre.org/techniques/AML.T0070 |",
        "",
        "Screenshot **AML.T0051** for the required ATLAS evidence (it is the primary technique on Attack Tree 1).",
        "",
        "## 5. Risk-ranked register with owners",
        "",
        "| Rank | ID | Score | Threat | Owner |",
        "|------|----|-------|--------|-------|",
    ]
    for i, r in enumerate(ranked, 1):
        lines.append(f"| {i} | {r['id']} | {r['L']*r['I']} | {r['threat']} | {r['owner']} |")
    lines += [
        "",
        "Full columns (STRIDE, ATLAS, treatment) are in `deliverables/Risk_Register.csv`.",
        "",
        "## 6. Alignment notes (for the wider capstone list)",
        "",
        "Project 1 evidence already touches: AI identity attack surface; STRIDE on identity flows; OAuth2+PKCE/OIDC via Auth0; federated SSO; short-lived M2M/LLM keys; prompt injection (LLM01/LLM07); agent spoofing and RAG poisoning (LLM09 / supply chain); Zero Trust (no implicit agent trust); OWASP LLM mapping; Auth0 attack protection as a control on F1; monitoring via the audit-log identity flow.",
        "",
        "Guardrails, Ed25519 binding, NIST AI RMF policy text, and red-team execution belong in later projects — not required as extra screenshots here.",
        "",
    ]
    (ROOT / "Project1_Threat_Model_Report.md").write_text("\n".join(lines), encoding="utf-8")


def write_identities_csv():
    path = OUT / "Identity_Inventory.csv"
    rows = [
        ["Identity type", "Authentication mechanism", "Privilege level"],
        [
            "Human user (customer)",
            "Auth0 Universal Login; OAuth 2.0 Auth Code + PKCE; OIDC",
            "Own tickets/PII/chat only",
        ],
        [
            "Human user (CSR)",
            "OIDC + MFA + Enterprise SSO",
            "Assigned cases; no LLM keys",
        ],
        [
            "Human security admin",
            "OIDC + MFA + Auth0 RBAC",
            "Tenant security config; no standing LLM keys",
        ],
        [
            "AI agent orchestrator",
            "OBO user JWT + M2M client credentials (short-lived)",
            "Delegated user scopes + constrained tools",
        ],
        [
            "OAuth M2M client",
            "Client Credentials grant / Auth0 JWT",
            "tickets:* and kb:search; not admin",
        ],
        [
            "LLM API key",
            "Provider key from vault; rotated",
            "Inference only",
        ],
        [
            "RAG pipeline service identity",
            "Workload / M2M JWT",
            "Retrieve read; ingest uses separate write identity",
        ],
        [
            "MCP server identity",
            "OAuth RS + mTLS + optional Ed25519",
            "Allow-listed tools only",
        ],
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)


def main():
    write_threat_dragon()
    write_drawio()
    write_csvs()
    write_html_workbook()
    write_identities_csv()
    write_guide()
    write_report_md()
    print("Wrote", OUT)


if __name__ == "__main__":
    main()
