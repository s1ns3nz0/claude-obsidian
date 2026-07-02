---
type: meta
title: "Concepts Index"
updated: 2026-04-07
tags:
  - meta
  - index
  - concept
domain: knowledge-management
status: evergreen
related:
  - "[[index]]"
  - "[[dashboard]]"
  - "[[Wiki Map]]"
  - "[[Hot Cache]]"
  - "[[LLM Wiki Pattern]]"
  - "[[Compounding Knowledge]]"
  - "[[LLM Wiki Pattern]]"
  - "[[Hot Cache]]"
  - "[[Compounding Knowledge]]"
---

# Concepts Index

Navigation: [[index]] | [[entities/_index|Entities]] | [[sources/_index|Sources]]

All concept pages — ideas, patterns, and frameworks extracted from sources.

---

## Knowledge Management

- [[LLM Wiki Pattern]] — the core architecture for persistent, compounding knowledge bases
- [[Hot Cache]] — ~500-word session context file, updated after every ingest
- [[Compounding Knowledge]] — why the wiki grows more valuable over time, unlike RAG
- [[DragonScale Memory]] — memory-layer spec: fold operator, deterministic page addresses, semantic tiling, boundary-first autoresearch (status: shipped v0.4, all four mechanisms opt-in)
- [[Persistent Wiki Artifact]]: durable Markdown page as the LLM's memory object (developing)
- [[Source-First Synthesis]]: provenance discipline for LLM wiki layers (developing)
- [[Query-Time Retrieval]]: query synthesis with citations, complementary to Obsidian search (developing)

---

---

## UAV-AI-SOC

- [[UAV-AI-SOC Core Layer]] — pure domain layer (`core/`); no external I/O; owns data contracts, exceptions, config (Doc 01)
- [[Alert Model]] — Pydantic inbound event contract; fail-fast Severity enum validation at the boundary (Doc 01)
- [[SOCPlatformError Exception Hierarchy]] — expected-failure exception tree; graceful degradation via selective catch (Doc 01)
- [[Settings SecretStr]] — centralized Pydantic config; `SecretStr` log masking; `lru_cache` singleton (Doc 01)
- [[에이전트 오케스트레이션 파이프라인]] — 6-stage fixed pipeline (Triage→Investigation→Validation→Response/RuleUpdate→Report); LangGraph; single conditional branch (Doc 02)
- [[LangGraph]] — LangChain graph orchestrator; `add_node`, `add_edge`, `add_conditional_edges`; used for SOC pipeline (Doc 02)
- [[BaseSOCAgent]] — abstract base class `async def run(state: SOCState) -> SOCState`; also `BaseWorkerAgent` for periodic workers (Doc 02)
- [[SOCState]] — shared state TypedDict flowing through the pipeline; list keys auto-concatenate; `total=False` for partial returns (Doc 01 + 02)
- [[고정 파이프라인 토폴로지]] — fixed pipeline vs. single-agent vs. autonomous-collaboration topology; choice rationale for SOC (Doc 02)
- [[RAG]] — Retrieval-Augmented Generation: hybrid vector+BM25 search, deterministic confidence scoring, source guardrails, graceful degradation, RAGAS evaluation (UAV-AI-SOC 시스템디자인 Doc 03)
- [[GraphRAG]] — graph-augmented retrieval: curated YAML knowledge graph, deterministic token-match scoring, neighborhood expansion, kill-chain adjacency inference; contrasts with standard LLM extraction pipeline (Doc 04)
- [[Knowledge Graph]] — general concepts: graph schemas, entity extraction vs. curation, entity resolution, hop traversal, community detection; tradeoff table (Doc 04)
- [[CompositeRetriever]] — hybrid combinator: parallel flat RAG + graph RAG via asyncio.gather; source-keyed deduplication; mutual fault isolation (Doc 04)

- [[RAGAS 품질 측정]] — faithfulness/answer_relevancy/context_relevancy 세 메트릭; fire-and-forget 비동기; Prometheus 게이지; graceful degrade (Doc 16)
- [[Causal Reasoning Chain]] — 결정론 인과 룰 YAML; LLM은 자연어 설명만; MITRE 기법 ID 매핑; OSCAL 감사 문서 임베드 (Doc 16)
- [[Data Lineage Snapshot]] — git SHA·llm_model·policy_hashes·settings_fingerprint; SecretStr 마스킹; opt-in; 감사 재현성 (Doc 16)
- [[GNSS Domain Context]] — GPSJam.org + OpenSky Network; S1 시나리오 confidence 보강; 포이즈닝 방어; 좌표 fallback (Doc 16)

---

## AI Tooling / MCP

- [[DevSpace]] — self-hosted MCP server exposing a local project to ChatGPT/Claude via tunnel + owner-password gating (PyTorchKR news, 2026-07-01)

---

## Add new concepts here as they are extracted from sources.
