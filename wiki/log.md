---
type: meta
title: "Operation Log"
updated: 2026-04-08
tags:
  - meta
  - log
status: evergreen
related:
  - "[[index]]"
  - "[[hot]]"
  - "[[overview]]"
  - "[[sources/_index]]"
---

# Operation Log

Navigation: [[index]] | [[hot]] | [[overview]]

Append-only. New entries go at the TOP. Never edit past entries.

Entry format: `## [YYYY-MM-DD] operation | Title`

Parse recent entries: `grep "^## \[" wiki/log.md | head -10`

---

## [2026-07-02] ingest | PyTorchKR news pipeline test — DevSpace MCP article
- Source: https://discuss.pytorch.kr/t/devspace-chatgpt-mcp/10994 (선택 기사 #1, PyTorchKR 텔레그램 알림 파이프라인의 첫 end-to-end 테스트)
- Raw copy: `.raw/pytorch-devspace-mcp.md`
- Source page: `wiki/sources/DevSpace-ChatGPT-Local-MCP.md`
- Concept created: `wiki/concepts/DevSpace.md` (self-hosted MCP server, tunnel + owner-password gating pattern)
- Indexes updated: `wiki/sources/_index.md` (Articles), `wiki/concepts/_index.md` (new "AI Tooling / MCP" section)
- Purpose: validate the "텔레그램 알림 → 사용자가 기사 선택 → Claude 요약·인제스트 → wiki 반영 → Quartz 동기화" 수동 파이프라인 end-to-end

## [2026-07-02] backfill | UAV-AI-SOC 시스템디자인 wave-1 manifest+log reconciliation
- Wave-1 (docs 00, 01, 05) ingest agents finished the content writes but lost their manifest/log updates to a parallel-write race — `flock` unavailable on macOS, so `wiki-lock.sh` fell through to unsynchronized reads. Later waves clobbered wave-1 bookkeeping.
- Reconciled: added missing `.raw/.manifest.json` entries for docs 00/01/05 with `backfilled: 2026-07-02` marker; added this single consolidated log entry rather than three fictitious ingest entries.
- Content verified in-place:
  - Doc 00 → `wiki/sources/UAV-AI-SOC-시스템디자인-00.md` (series overview anchor)
  - Doc 01 → `wiki/sources/UAV-AI-SOC-시스템디자인-01.md`, concepts: `UAV-AI-SOC Core Layer`, `SOCState`, `SOCPlatformError Exception Hierarchy`, `Settings SecretStr`, `Alert Model`
  - Doc 05 → `wiki/sources/UAV-AI-SOC-시스템디자인-05.md`, concepts: `Experience Memory`, `Memory Poisoning`, `Self-Improvement Loop`, `ExperienceRecord`, `Asymmetric Trust`, `Provenance Trust`
- Series index: 00 added to `ingested_docs` frontmatter; table already showed all 17 rows complete.
- Followup: patch `scripts/wiki-lock.sh` to use Python-based cross-process lock on macOS (see prior log note in doc 04 entry), or install `brew install util-linux`. Track separately.

## [2026-07-02] ingest | UAV-AI-SOC 시스템디자인 12 — 다중 Judge 앙상블 (판정 강화)
- Source: `.raw/UAV-AI-SOC/시스템디자인/12 - 다중 Judge 앙상블 (판정 강화).md`
- Domain: UAV-AI-SOC | Series doc 12 of 16 | Language: Korean
- Created: `wiki/sources/UAV-AI-SOC-시스템디자인-12.md`, `wiki/concepts/Multi-Judge Ensemble.md`, `wiki/concepts/Signal Veto.md`, `wiki/concepts/Verdict Aggregation.md`
- Updated: `wiki/references/UAV-AI-SOC-시스템디자인.md` (doc 12 marked 완료; 3 new concept links; 12 added to ingested_docs), `.raw/.manifest.json` (doc 12 entry)
- Key: ValidationAgent의 단일 judge 한계(결정론 단독=애매한 케이스 침묵, LLM 단독=인젝션 취약, 이진 출력=KPI 불가)를 세 직교 판정자(SignalJudge·LlmJudge·ExperienceJudge)로 해결; SignalJudge만 거부권 보유 — LLM이 점수 1.0을 줘도 물리 신호 없으면 강제 FP 확정; composite_score(0~1 연속값)는 RAGAS/Prometheus 연결 가능

## [2026-07-02] ingest | UAV-AI-SOC 시스템디자인 16 — 도메인 컨텍스트 · 인과 · 재현성 · 품질 [SERIES COMPLETE]
- Source: `.raw/UAV-AI-SOC/시스템디자인/16 - 도메인 컨텍스트 · 인과 · 재현성 · 품질.md`
- Domain: UAV-AI-SOC | Series terminal doc (16 of 16) | Language: Korean
- Created: `wiki/sources/UAV-AI-SOC-시스템디자인-16.md`, `wiki/concepts/RAGAS 품질 측정.md`, `wiki/concepts/Causal Reasoning Chain.md`, `wiki/concepts/Data Lineage Snapshot.md`, `wiki/concepts/GNSS Domain Context.md`
- Updated: `wiki/references/UAV-AI-SOC-시스템디자인.md` (series_complete=true; Doc 16 row; 4 new concept links; Series complete callout), `wiki/concepts/_index.md` (4 Doc 16 concepts), `.raw/.manifest.json` (Doc 16 entry with series_terminal=true)
- Key: Four orthogonal trust pillars — GNSS/Airspace context for S1-scenario confidence boosting (community sources do confidence only, never severity), deterministic causal chain YAML with LLM for explanation only, `LineageSnapshot` capturing git-SHA+model+policy-hashes for audit reproducibility (opt-in `LINEAGE_ENABLED`), RAGAS fire-and-forget async KPI (faithfulness/answer_relevancy/context_relevancy) with graceful degrade

## [2026-07-02] ingest | UAV-AI-SOC 시스템디자인 15 — 위협 인텔 자동화 (Threat Landscape · Auto KQL)
- Source: `.raw/UAV-AI-SOC/시스템디자인/15 - 위협 인텔 자동화 (Threat Landscape · Auto KQL).md`
- Domain: UAV-AI-SOC | Series doc 15 of 16 | Language: Korean
- Created: `wiki/sources/UAV-AI-SOC-시스템디자인-15.md`, `wiki/concepts/Threat Landscape Agent.md`, `wiki/concepts/Auto KQL Rule Agent.md`
- Updated: `wiki/concepts/Detection-as-Code.md` (Doc 15 cross-ref + two new related links), `wiki/concepts/Threat Intel Feed.md` (Doc 15 CISA KEV extension cross-ref), `wiki/references/UAV-AI-SOC-시스템디자인.md` (doc 15 complete; 2 new concept links), `.raw/.manifest.json` (doc 15 entry)
- Key: Doc 07 made KQL immutable to AI; Doc 15 extends that by making the ATT&CK coverage list self-updating (ThreatLandscapeAgent) and letting LLM draft initial KQL stubs for new T-ids (AutoKqlRuleAgent) — all still gated behind PR + human review; KqlValidator blacklists external_table/http_get to block LLM data-exfil prompt injection

## [2026-07-02] ingest | UAV-AI-SOC 시스템디자인 14 — 자가발전 실연동
- Source: `.raw/UAV-AI-SOC/시스템디자인/14 - 자가발전 실연동.md`
- Domain: UAV-AI-SOC | Series doc 14 of 16 | Language: Korean
- Created: `wiki/sources/UAV-AI-SOC-시스템디자인-14.md`, `wiki/concepts/OutcomeProbeAgent Pipeline.md`
- Updated: `wiki/concepts/Self-Improvement Loop.md` (plumbing cross-ref + zero-user-code section), `wiki/references/UAV-AI-SOC-시스템디자인.md` (doc 14 complete; 1 new concept link), `.raw/.manifest.json` (doc 14 entry)
- Key: Doc 05/06 designed the self-improvement loop conceptually; doc 14 is the plumbing that makes it run with zero user code — SimBridge auto-hook accumulates telemetry windows in-stream, OutcomeProbeAgent applies a deterministic decision matrix (not LLM interpretation) and fans out to three write gates, learning worker scheduler activates workers from settings alone; the full SITL→label→memory→recall cycle now requires no human intervention

## [2026-07-02] ingest | UAV-AI-SOC 시스템디자인 13 — IoA 공격자 중심 방어
- Source: `.raw/UAV-AI-SOC/시스템디자인/13 - IoA 공격자 중심 방어.md`
- Domain: UAV-AI-SOC | Series doc 13 of 16 | Language: Korean
- Created: `wiki/sources/UAV-AI-SOC-시스템디자인-13.md`, `wiki/concepts/IoA (Indicator of Attack).md`, `wiki/concepts/Attacker-Centric Defense.md`
- Updated: `wiki/entities/MITRE ATT&CK.md` (IoA role section: ATT&CK T-IDs as IoA vocabulary), `wiki/references/UAV-AI-SOC-시스템디자인.md` (doc 13 complete; 2 new concept links), `.raw/.manifest.json` (doc 13 entry)
- Key: IoC(사후 증거물)는 도구만 바꿔도 우회되지만 IoA(사전 행위 지표)는 TTP 시퀀스를 추적해 동일 공격자를 재인식한다. n=2 마르코프로 다음 MITRE 기법을 결정론적으로 예측(LLM 미사용); 예측이 자동 대응을 트리거할 수 있으므로 통계 기반 재현 가능성이 필수. priority 강등은 explicit + CONFIRMED_TP 조건만 허용해 FP 폭탄 조작을 차단.

## [2026-07-02] ingest | UAV-AI-SOC 시스템디자인 07 — 탐지·룰 자동개선 (Detection-as-Code)
- Source: `.raw/UAV-AI-SOC/시스템디자인/07 - 탐지·룰 자동개선 (Detection-as-Code).md`
- Domain: UAV-AI-SOC | Series doc 07 of 16 | Language: Korean
- Created: `wiki/sources/UAV-AI-SOC-시스템디자인-07.md`, `wiki/concepts/Detection-as-Code.md`, `wiki/concepts/Watchlist-as-Detection-Data.md`
- Updated: `wiki/references/UAV-AI-SOC-시스템디자인.md` (doc 07 complete; 2 new concept links), `.raw/.manifest.json`
- Key: KQL query logic is permanently immutable to AI; only watchlist data (the tables KQL reads) is AI-editable via auto-generated GitHub PRs — no-auto-merge invariant closes the adversarial false-positive-induction attack vector

## [2026-07-02] ingest | UAV-AI-SOC 시스템디자인 10 — 보안 위협모델 + 방어
- Source: `.raw/UAV-AI-SOC/시스템디자인/10 - 보안 위협모델 + 방어.md`
- Domain: UAV-AI-SOC | Series doc 10 of 16 | Language: Korean
- Created: `wiki/sources/UAV-AI-SOC-시스템디자인-10.md`, `wiki/concepts/Defense-in-Depth.md`, `wiki/concepts/Attack Surface.md`
- Updated: `wiki/concepts/Memory Poisoning.md` (doc 10 cross-ref + Multi-Judge ensemble note), `wiki/references/UAV-AI-SOC-시스템디자인.md` (doc 10 complete; 2 new concept links), `.raw/.manifest.json`
- Key: AI SOC becomes its own attack target; automation/self-improvement expand the attack surface; 5-layer GPS spoofing concealment scenario illustrates defense-in-depth — all five must be bypassed simultaneously; ATT&CK coverage gaps classified into 5 archetypes (A–E), split into addressable vs. inherent gaps for prioritization

## [2026-07-02] ingest | UAV-AI-SOC 시스템디자인 08 — 외부 연동 (TI·샌드박스·취약점)
- Source: `.raw/UAV-AI-SOC/시스템디자인/08 - 외부 연동 (TI·샌드박스·취약점).md`
- Domain: UAV-AI-SOC | Series doc 08 of 16 | Language: Korean
- Created: `wiki/sources/UAV-AI-SOC-시스템디자인-08.md`, `wiki/concepts/Threat Intel Feed.md`, `wiki/concepts/Sandbox Detonation.md`, `wiki/concepts/Vulnerability Enrichment.md`
- Updated: `wiki/references/UAV-AI-SOC-시스템디자인.md` (doc 08 complete; 3 new concept links), `.raw/.manifest.json` (doc 08 entry)
- Key: Three external enrichment tools (TI/Sandbox/Vuln) share a 4-layer pattern (Protocol → Stub → real adapter with client_factory injection → Composite worst-case merge); each confirmed malicious signal adds confidence +0.2; asyncio.gather parallelizes all three; UAV-specific additions GnssJamTool and AirspaceTool add domain-aware context; community sources may boost confidence but are barred from touching severity engine

## [2026-07-02] ingest | UAV-AI-SOC 시스템디자인 09 — 배포·운영 (토폴로지·스케일·관측)
- Source: `.raw/UAV-AI-SOC/시스템디자인/09 - 배포·운영 (토폴로지·스케일·관측).md`
- Domain: UAV-AI-SOC | Series doc 09 of 16 | Language: Korean
- Created: `wiki/sources/UAV-AI-SOC-시스템디자인-09.md`, `wiki/concepts/2-Deployment 하이브리드 토폴로지.md`, `wiki/concepts/GitOps ArgoCD.md`, `wiki/concepts/Prometheus Observability.md`
- Updated: `wiki/references/UAV-AI-SOC-시스템디자인.md` (doc 09 complete; 3 new concept links), `.raw/.manifest.json` (doc 09 entry)
- Key: ADR D6 separates hot-path (single replica, stateful) from learning (HPA, stateless) — state consistency vs. throughput elasticity; Prometheus rendered with stdlib only (zero external deps); "ghost metric" test cross-validates dashboard panel references against live /metrics output

## [2026-07-02] ingest | UAV-AI-SOC 시스템디자인 11 — 검증 (테스트·벤치마크)
- Source: `.raw/UAV-AI-SOC/시스템디자인/11 - 검증 (테스트·벤치마크).md`
- Domain: UAV-AI-SOC | Series doc 11 of 16 | Language: Korean
- Created: `wiki/sources/UAV-AI-SOC-시스템디자인-11.md`, `wiki/concepts/벤치마크 하네스.md`, `wiki/concepts/ATLAS 레드팀 벤치마크.md`, `wiki/concepts/회귀 게이트.md`
- Updated: `wiki/references/UAV-AI-SOC-시스템디자인.md` (doc 11 complete; 3 new concept links), `.raw/.manifest.json` (doc 11 entry)
- Key: 400+ tests all run without network (Protocol injection + determinism principle); ATLAS T0020 red-team target robust success rate 0.0 (falsifiable defense proof); 5-stage CI pipeline (ruff → mypy → pytest 400+ → benchmarks G2 → RAGAS sim)

## [2026-07-02] ingest | UAV-AI-SOC 시스템디자인 06 — 환경검증 오라클
- Source: `.raw/UAV-AI-SOC/시스템디자인/06 - 환경검증 오라클.md`
- Domain: UAV-AI-SOC | Series doc 06 of 16 | Language: Korean
- Created: `wiki/sources/UAV-AI-SOC-시스템디자인-06.md`, `wiki/concepts/환경검증 오라클.md`
- Updated: `wiki/concepts/Asymmetric Trust.md` (oracle cross-ref), `wiki/references/UAV-AI-SOC-시스템디자인.md` (doc 06 complete)
- Key: "텍스트는 거짓말해도 물리는 못 한다" — physical telemetry from sim engine is tamper-proof; INCONCLUSIVE verdicts are never written to memory (grey-zone blockade)

## [2026-07-02] ingest | UAV-AI-SOC 시스템디자인 04 — GraphRAG (관계를 검색하기)
- Source: `.raw/UAV-AI-SOC/시스템디자인/04 - GraphRAG.md`
- Domain: UAV-AI-SOC | Series doc 04 of N | Language: Korean
- Created: `wiki/sources/UAV-AI-SOC-GraphRAG-04.md`, `wiki/concepts/GraphRAG.md`, `wiki/concepts/Knowledge Graph.md`, `wiki/concepts/CompositeRetriever.md`, `wiki/entities/MITRE ATT&CK.md`
- Updated: `wiki/references/UAV-AI-SOC-시스템디자인.md` (Doc 04 row marked complete; 5 new concept links), `wiki/concepts/_index.md` (3 new UAV-AI-SOC entries), `wiki/entities/_index.md` (Frameworks section + MITRE ATT&CK), `wiki/concepts/RAG.md` (Extension: GraphRAG section + Doc 04 cross-reference)
- Key concepts: UAV-AI-SOC skips standard GraphRAG steps 1-3 and 5 (LLM entity extraction, entity resolution, community detection/summarization) in favor of human-curated YAML graph (`data/mitre_attack_graph.yaml`); deterministic lexical token-match scoring (`score()`, `_scenario_terms()`); neighborhood expansion (`neighborhood()`) as local-search equivalent; kill-chain adjacency inference as global-search replacement; `CompositeRetriever` (asyncio.gather, source-keyed dedup, mutual fault isolation via `_safe()`); two-graph architecture (static knowledge graph vs. dynamic IoA visualization graph)
- Cross-references: [[RAG]] (doc #03, flat RAG prerequisite; source guardrail splits `kb/` from `graph/`), [[Query-Time Retrieval]], [[DragonScale Memory]] (this vault's analogous BM25+rerank retrieval)
- Note: wiki-lock.sh `acquire` failed on macOS (flock not available); single-writer session, no parallel agents, no corruption risk. Sequential writes applied.
- No contradictions detected with existing pages.

## [2026-07-02] ingest | UAV-AI-SOC 시스템디자인 02 — 에이전트 오케스트레이션 (파이프라인)
- Source: `.raw/UAV-AI-SOC/시스템디자인/02 - 에이전트 오케스트레이션 (파이프라인).md`
- Domain: UAV-AI-SOC | Series doc 02 of N | Language: Korean
- Created: `wiki/sources/UAV-AI-SOC-시스템디자인-02-에이전트-오케스트레이션.md`, `wiki/concepts/에이전트 오케스트레이션 파이프라인.md`, `wiki/concepts/LangGraph.md`, `wiki/concepts/BaseSOCAgent.md`, `wiki/concepts/고정 파이프라인 토폴로지.md`, `wiki/entities/UAV-AI-SOC.md`
- Updated: `wiki/references/UAV-AI-SOC-시스템디자인.md` (Doc 02 row complete), `wiki/concepts/SOCState.md` (GNSS walkthrough + Doc 02 source link added), `wiki/concepts/_index.md` (5 new UAV-AI-SOC Doc 02 concept entries), `wiki/entities/_index.md` (Projects section + UAV-AI-SOC entry)
- Key concepts: 6-agent fixed pipeline (Triage→Investigation→Validation→Response/RuleUpdate→Report), LangGraph `add_conditional_edges` (single branch point), `_timed` decorator for per-node latency KPI (MTTT/MTTC), dependency injection via `None` defaults, `signal_judge` 3-way verdict (has_signal AND has_rule AND corroborated), S5 guardrail (policy-engine severity floor overrides LLM suggestion), `BaseWorkerAgent` for periodic workers, Validation ensemble (3 judges, asyncio.gather), Report 4-embed extensions
- Cross-references: [[SOCState]] (extended from Doc 01 with Doc 02 walkthrough), [[RAG]] (Investigation sources), [[wiki/references/UAV-AI-SOC-시스템디자인]] (series index updated)
- Note: wiki-lock.sh acquire failed on macOS (flock not available); single-writer session, no corruption risk.
- No contradictions detected with existing pages.

## [2026-07-02] ingest | UAV-AI-SOC 시스템디자인 03 — RAG (검색 증강)
- Source: `.raw/UAV-AI-SOC/시스템디자인/03 - RAG (검색 증강).md`
- Domain: UAV-AI-SOC | Series doc 03 of N
- Created: `wiki/sources/UAV-AI-SOC-03-RAG.md`, `wiki/concepts/RAG.md`, `wiki/references/UAV-AI-SOC-시스템디자인.md` (new series index)
- Updated: `wiki/references/UAV-AI-SOC-시스템디자인.md` (Doc 03 row), `wiki/concepts/_index.md` (UAV-AI-SOC section), `wiki/concepts/Query-Time Retrieval.md` (cross-reference to [[RAG]])
- Key concepts: RAGFlow on-premises hybrid search (vector+BM25), deterministic confidence formula from retrieval scores (no LLM self-assessment), source-origin guardrail (`kb/` prefix whitelist defends against prompt injection at score 0.99), graceful degradation to confidence 0.2, RAGAS async evaluation layer
- Cross-reference: [[Query-Time Retrieval]] (academic RAG lineage), [[DragonScale Memory]] (this vault's analogous BM25+cosine retrieval)
- No contradictions detected with existing pages.

## [2026-04-24] save | v1.6.0 public release notes (Teams, Karpathy-style)
- Type: release doc + visual assets
- Locations (new): `docs/releases/v1.6.0.md` (346 lines, 6 sections, Karpathy-style prose), `wiki/meta/dragonscale-mechanism-overview.svg` (4-mechanism diagram with shared .vault-meta/ gate), `wiki/meta/dragonscale-6-test-flow.svg` (validation timeline), `wiki/meta/dragonscale-frontier-graph.svg` (M4 candidate + 3 filed pages)
- Locations (modified): `wiki/meta/2026-04-24-v1.6.0-release-session.md` (cross-reference added pointing to public release notes)
- Scope: Teams approach. R1 (chair) wrote 3 original SVGs per SVG Diagram Style Guide. R2 (codex worker) drafted Karpathy-style release prose. R3 (chair) stitched SVGs, pivoted Wikipedia imagery to text links only (no binary vendoring per permission). R4 (codex verifier) returned ACCEPT WITH FIXES, 3 wording fixes on version narrative. R5 (chair) applied fixes, committed.
- Style: direct, short, signal-dense, lists over prose, no em dashes, no marketing terms. Verifier confirmed zero em-dashes and zero banned marketing language ('revolutionary', 'seamless', 'world-class', 'game-changing', 'unlock', 'transform').
- Distribution (all three destinations covered): (1) `docs/releases/v1.6.0.md` public-facing file (commit `85515bb`), (2) `wiki/meta/2026-04-24-v1.6.0-release-session.md` internal engineering record (cross-linked), (3) GitHub Release body (user to paste from docs/releases/v1.6.0.md when ready to `gh release create v1.6.0`).
- Wikipedia imagery: referenced as text link to `https://en.wikipedia.org/wiki/Dragon_curve` rather than hotlinked or vendored. Cleaner license-wise (no CC-BY-SA attribution needed) and no external dependency. The 3 original SVGs carry the visual load instead.
- PII scan post-write: `docs/releases/v1.6.0.md` + all three SVGs are clean. No `/home/` paths, no real emails, no tokens.
- Next recommended: user runs `gh release create v1.6.0 --notes-file docs/releases/v1.6.0.md` when ready to cut the public release. This also creates the annotated tag.

## [2026-04-24] save | DragonScale end-to-end validation pass (Teams, 6 tests)
- Type: validation + first real fold + first real autoresearch
- Tests executed (all green):
  - T0 ollama pull `nomic-embed-text`: done (274MB, 15s wall)
  - T1 M1 dry-run k=3 via codex: DRY-RUN OK, 8 children, no em-dashes
  - T2 M2 real allocate: counter advanced 2 to 3, got `c-000002` (unassigned reservation; gap acceptable per spec)
  - T3 M3 full tiling with model present: 41 pages scanned, 21 embedded, 20 correctly skipped (meta/excluded/embed-error), 0 errors at >=0.9, 15 pairs in 0.8-0.9 review band (top 0.8822 Compounding Knowledge vs LLM Wiki Pattern, a legitimate semantic neighbor), report at `wiki/meta/tiling-report-2026-04-24.md`
  - T4 M1 commit via codex: first real fold committed, `wiki/folds/fold-k3-from-2026-04-23-to-2026-04-24-n8.md` (115 lines, 8 children, flat extractive). Flips the long-standing "no fold committed yet" status
  - T6 M4 autoresearch no-topic via codex: selected "How does the LLM Wiki pattern work?" as candidate (score 1.7022, #3 after skipping top-1 source + top-2 self-reference); 6 web fetches (Karpathy gist, RAG paper arXiv 2005.11401, MemGPT arXiv 2310.08560, Obsidian docs); 3 new concept pages filed, each with Primary Sources
- Locations (new): `wiki/folds/fold-k3-from-2026-04-23-to-2026-04-24-n8.md`, `wiki/meta/tiling-report-2026-04-24.md`, `wiki/concepts/Persistent Wiki Artifact.md`, `wiki/concepts/Source-First Synthesis.md`, `wiki/concepts/Query-Time Retrieval.md`
- Locations (modified): `.vault-meta/address-counter.txt` (2 to 3), `wiki/index.md` (3 concept links), `wiki/concepts/_index.md` (3 concept links)
- Scope: six-test menu the user approved. Codex gpt-5.4 for T1/T4/T6 (sub-agent delegation); chair for T0/T2/T3 (one-shot shell) and all integration (index, log, hot, commit).
- Style: all new content uses colons or parens instead of em-dashes. Pre-existing em-dashes in index entries and wiki/concepts/_index.md left as-is (clean-room boundary; deferred to F-slice style pass).
- Tests still green: `make test` passes (74+ assertions).
- Integration: chair added the 3 new concepts to `wiki/index.md` and `wiki/concepts/_index.md` with colon-style descriptions so the fresh pages are discoverable. The cluster extends `[[How does the LLM Wiki pattern work?]]` and cross-references `[[LLM Wiki Pattern]]`.
- Next recommended slice: either (G) commit this test batch and declare v1.6.0 validated, or (H) run a second fold k=3 now that 8 newer entries exist above this one and close the hierarchical-fold-not-yet-supported loop in a future phase.

## [2026-04-24] save | v1.6.0 closeout (Teams, chair-led)
- Type: docs + release hygiene
- Locations (new): wiki/meta/2026-04-24-v1.6.0-release-session.md (release session summary, 346 lines), wiki/meta/boundary-frontier-2026-04-24.md (first M4 run artifact against this vault), docs/dragonscale-guide.md (user-facing DragonScale guide, 563 lines)
- Locations (modified): wiki/hot.md (tag-claim fix, Scripts line adds boundary-score, tests line adds test_boundary_score, push-line drift, tiling line-count, one em-dash), docs/install-guide.md (version 1.5.0 to 1.6.0, DragonScale callout expanded to all four mechanisms, "hierarchical log folds" corrected to "flat extractive log folds", points to docs/dragonscale-guide.md), README.md (DragonScale parenthetical expanded to all four mechanisms plus guide link)
- Scope: Teams approach, chair-led. Slice A (2 codex read-only explorers: closeout punch list + doc-surface map). Slice B (6 bounded writes: 4 chair, 2 codex workers, non-overlapping write scopes). Slice C (codex adversarial verifier, ACCEPT WITH FIXES). Slice D (fix pass + log entry + manual commit of docs + README).
- Verifier: C1 found 11 items across 6 files. All 11 applied. Flag typos `--allow-remote-ollama` and `--report PATH` corrected in release-session; boundary-frontier provenance corrected to `--top 7` to match default vs explicit top; hot.md tiling line-count claim stripped to avoid drift; hot.md "local tag only" corrected to "local commits only, no git tag"; install-guide log-fold wording corrected from "hierarchical" to "flat extractive"; dragonscale-guide rollback wording corrected (`.vault-meta/` is a shared gate across M2+M3+M4, not per-mechanism).
- Model: codex gpt-5.4 used throughout. User requested gpt-5.5; not reachable via codex CLI 0.123.0 / this account at the time. models_cache lists max gpt-5.4, and the API rejects gpt-5.5 with "does not exist or you do not have access". Existing config already has `service_tier = "fast"` and `sandbox_mode = "workspace-write"`, matching the "fast for chatgpt with permission of full access" intent.
- Tests: `make test` passes. test_allocate_address.sh (shell, 12 assertions), test_tiling_check.py (python, 18 assertions), test_boundary_score.py (python, 44 assertions). Zero ollama dependency.
- Tags: still no local v1.5.0 / v1.5.1 / v1.6.0 tags. User controls tag creation and push. Pre-existing tags unchanged (v1.1, v1.4.0 through v1.4.3).
- Deliberately NOT done: no real M1 fold committed; no M3 end-to-end run (needs `ollama pull nomic-embed-text`); pre-existing em-dashes in install-guide.md and README.md left untouched (clean-room boundary, not in write scope this slice); CLAUDE.md pre-existing uncommitted change left untouched.
- Next recommended slice: either (E) push to origin/main and create annotated tags v1.5.0, v1.5.1, v1.6.0 in landing order, or (F) dedicated style pass to scrub pre-existing em-dashes across install-guide.md, README.md, and any other wiki files flagged by a grep scan.

## [2026-04-24] save | DragonScale Phase 4 — boundary-first autoresearch shipped (v1.6.0)
- Type: feature release
- Locations (new): scripts/boundary-score.py (with --top, --page, --json, stdout-only CLI), tests/test_boundary_score.py (40+ assertions)
- Locations (modified): skills/autoresearch/SKILL.md (new Topic Selection section A/B/C with helper-failure fallback), commands/autoresearch.md (no-topic candidate flow with agenda-control label), wiki/concepts/DragonScale Memory.md (v0.4: M4 flipped from NOT IMPLEMENTED to shipped; exact formula without recency floor; filename-stem disclosure; fence-handling qualifiers), CHANGELOG.md, .claude-plugin/{plugin,marketplace}.json (1.5.0 -> 1.6.0), Makefile (test-boundary target), wiki/hot.md, wiki/index.md, wiki/concepts/_index.md (status drift resolved).
- Scope: boundary-first autoresearch as opt-in Topic Selection mode. `/autoresearch` without a topic surfaces top-5 frontier pages; user picks/overrides/declines. Explicit helper-failure fallback to user-ask. Labeled "agenda control" throughout to match the spec's scope disclosure.
- Correctness: filename-stem resolution including folder-qualified `[[notes/Foo]]` -> Foo.md. Self-loops, unresolved targets, meta-targets, symlinks, and vault escapes all excluded. Code-fence parser handles backticks AND tildes with CommonMark length tracking (longer opening fence is not closed by shorter inner fence). Indented blocks intentionally not filtered (Obsidian bullet convention).
- Recency: exp(-days/30), no floor. Stale pages approach zero weight so they do not dominate frontier ranking.
- Review rounds: codex adversarial Phase 4 round 1 (10 items: 7 reject + 3 refine). Round 2 (7 accept + 3 still-reject: folder-qualified stem, docstring floor mention, hot.md historical drift). Round 3 (3 accept, PASS).
- Phase 3.6 (pre-Phase-4 hardening) already landed as v1.5.1: tiling --report VAULT_ROOT confinement, rollout baseline, AGENTS.md consistency, wiki-ingest .raw/ contradiction, install-guide version.
- All four DragonScale mechanisms now shipped and opt-in. 44 commits ahead of origin/main, no push.

## [2026-04-24] save | DragonScale Phase 3.5 — cross-phase hardening to v1.5.0
- Type: release hardening
- Locations (new): bin/setup-dragonscale.sh (opt-in installer), tests/test_allocate_address.sh, tests/test_tiling_check.py, Makefile, CHANGELOG.md
- Locations (modified): hooks/hooks.json (+.vault-meta/ staging), agents/wiki-ingest.md (single-writer rule for addresses), agents/wiki-lint.md (Mechanism 2+3 checks), skills/wiki-ingest/SKILL.md (aligned non-DragonScale wording), wiki/concepts/DragonScale Memory.md (M2 severity matches lint, M4 marked NOT IMPLEMENTED, seed page gets address c-000001), .claude-plugin/{plugin.json,marketplace.json} (1.4.2/1.4.3 → 1.5.0), README.md (11 skills + DragonScale callout), wiki/hot.md (refreshed for v1.5.0), .raw/.manifest.json (address_map now has DragonScale Memory.md → c-000001), .gitignore (.vault-meta/.tiling.lock + cache), .vault-meta/address-counter.txt (advanced to 2).
- Scope: resolve the 10 hold-ship items from the cross-phase audit. Add reproducible test harness (make test passes). Version-bump plugin.json and marketplace.json to 1.5.0. Create CHANGELOG.md. Refresh hot cache.
- Review rounds: codex 3.5a (5/5 accept on doc/agent fixes), codex final holistic (10/10 accept on audit items + 2 surgical regression fixes: wiki-ingest/wiki-lint non-DragonScale wording alignment, README skill count).
- Tests: `make test` runs 12 shell assertions (allocator) + 18 python assertions (tiling-check). All pass; no ollama dependency.
- Phase 3.5 complete. Repo state: 6 developer commits added this pass (f2e73c1, 2b49a0c, 8b28e48, 19ad7e4, 365f557, 2e7dd16). Total 39 commits ahead of origin/main. No push.

## [2026-04-24] save | DragonScale Phase 3 — semantic tiling MVP
- Type: skill update + new script + threshold state
- Locations: scripts/tiling-check.py (485 lines), .vault-meta/tiling-thresholds.json (seed defaults), skills/wiki-lint/SKILL.md (109-line Semantic Tiling section + item #10 in checks), wiki/concepts/DragonScale Memory.md (Mechanism 3 cost framing clarified)
- Scope: opt-in embedding-based duplicate detection via ollama nomic-embed-text. Default bands error>=0.90, review>=0.80, explicitly documented as conservative seeds (not literature-backed interpolation). Calibration procedure documented, not automated.
- Security: default OLLAMA_URL locked to 127.0.0.1; non-localhost requires --allow-remote-ollama flag. Symlinks and vault-root escapes rejected before file reads (prevents data exfil).
- Correctness: cache keyed on sha256(model+body); orphan GC on save; model-drift auto-invalidation on load.
- Concurrency: flock(LOCK_EX) on .vault-meta/.tiling.lock; per-PID temp file for atomic writes.
- Scale: warn >500 pages; hard-fail exit 4 at >5000 pages.
- Exit codes: 0/2/3/4/10/11 distinctly surfaced in wiki-lint wiring (not collapsed into "unknown").
- Review rounds: 4 codex exec adversarial passes covering security, cache correctness, feature gate, inclusion logic, scale, threshold honesty, concurrency, exit codes, model drift, terminology coupling.
  Round 1: 10 items -> 7 reject + 3 refine.
  Round 2: 6 accept + 4 still-reject (symlink ordering, prose sync, exit-code wiring, terminology in checklist + "no API cost" claim).
  Round 3: 3 accept + 1 still-reject (cost-framing phrasing).
  Round 4: accept.
- Final verdict: 10/10 accept.
- Phase 3 complete. All three DragonScale mechanisms that were in-scope for the initial spec are now shipped as opt-in features. Mechanism 4 (boundary-first autoresearch) was flagged as agenda-control out-of-scope per the v0.2 scope boundary; may or may not ship as a future phase.

## [2026-04-23] save | DragonScale Phase 2 — deterministic page addresses MVP
- Type: skill update + new script
- Locations: scripts/allocate-address.sh, skills/wiki-ingest/SKILL.md (Address Assignment section), skills/wiki-lint/SKILL.md (Address Validation section), wiki/concepts/DragonScale Memory.md (Mechanism 2 rewritten v0.2→v0.3), .vault-meta/address-counter.txt, .raw/.manifest.json (new)
- Scope: MVP address format `c-NNNNNN` (creation-order counter, zero-padded 6 digits). Rollout baseline 2026-04-23. Legacy pages exempt until deliberate backfill (future `l-` prefix). No content hash, no fold-ancestry encoding in the MVP (both deferred).
- Concurrency: atomic allocation via flock-guarded Bash helper. Counter recovery from max observed `c-` address, never silent reset to 1.
- Lint: post-rollout pages without address are errors; legacy pages without address are informational. Optional `.vault-meta/legacy-pages.txt` manifest grandfathers pages with missing/wrong `created:` metadata.
- Re-ingest idempotency: `.raw/.manifest.json` `address_map` preserves path→address mapping across re-ingests and renames.
- Naming: mechanism renamed from "content-addressable paths" to "deterministic page addresses" (the MVP is a counter, not a content hash; the old name was overclaim).
- Review rounds: 2 codex exec adversarial passes. Round 1: 8 rejects covering counter mutation, race conditions, uniqueness atomicity, missing-file recovery, terminology drift, silent regression path, legacy classification, re-ingest idempotency. Round 2: 7 accept + 1 reject (manifest.json absent). Round 3 (item 8 only): accept after creating `.raw/.manifest.json`.
- Final verdict: 8/8 accept.
- Phase 2 complete. Phase 3 (semantic tiling lint) gated on human approval.

## [2026-04-23] save | DragonScale Phase 1 — wiki-fold skill shipped
- Type: skill
- Location: skills/wiki-fold/SKILL.md, skills/wiki-fold/references/fold-template.md
- Scope: flat extractive fold over raw wiki/log.md entries. Dry-run default via Bash stdout (no Write tool, avoids PostToolUse hook residue). Structural idempotency via deterministic fold_id. Duplicate-range detection. Fold-of-folds explicitly out of scope.
- Review rounds: 3 codex exec adversarial passes. Round 1: 1 refine + 6 reject across 7 items (allowed-tools, hook-mutation risk, idempotency claim, dry-run faithfulness, children structure, Mechanism 1 coverage, auto-commit conflict). Round 2: 6 accept + 1 reject (25/26 count inversion). Round 3 (item 4 only): accept.
- Final verdict: 7/7 accept.
- Dry-run artifact: /tmp/wiki-fold-dry-run-v2.md (not committed). fold_id: fold-k3-from-2026-04-10-to-2026-04-23-n8.
- Phase 1 complete. Phase 2 (content-addressable paths) gated on human approval.

## [2026-04-23] save | DragonScale Memory v0.2 — post-adversarial-review
- Type: concept revision
- Location: wiki/concepts/DragonScale Memory.md
- Review: codex exec adversarial review rejected all 7 load-bearing claims in v0.1
- Changes: weakened LSM analogy, removed strong prompt-cache claim, replaced 0.85 threshold with calibration procedure, justified 2^k as MVP convenience, acknowledged scope-boundary leak for boundary-first autoresearch, added Operational Policies section (retention/tombstones/versioning/conflict/concurrency/provenance/ACL), tagged claims as [sourced]/[derived]/[conjecture], narrowed tagging scope per re-review
- Re-review result: 7/7 accepted (after one surgical fix on tagging-scope language)
- Phase 0 complete. Phase 1 (wiki-fold skill) gated on human approval.

## [2026-04-23] save | DragonScale Memory — Phase 0 design doc (proposed)
- Type: concept
- Location: wiki/concepts/DragonScale Memory.md
- From: brainstorming session on applying Heighway dragon curve properties to LLM wiki memory architecture
- Scope: memory-layer only, NOT agent reasoning. Four mechanisms: (1) fold operator (LSM-style exponential compaction at 2^k log entries), (2) content-addressable page paths for prompt-cache stability, (3) semantic tiling lint (embedding-based dedup, 0.85 cosine threshold), (4) boundary-first autoresearch scoring
- Status: proposed. Phase 0 pending codex adversarial review. Phase 1+ (fold skill, address anchors, tiling lint, boundary score) gated on review pass.
- Primary sources verified: Dragon curve (Wikipedia, boundary dim 1.523627086), Regular paperfolding sequence (OEIS A014577), LSM trees (arXiv 2504.17178, LevelDB 10x level ratio), MemGPT (arXiv 2310.08560), Anthropic prompt caching docs (5min/1hr TTL, 20-block lookback)
- Links updated: wiki/concepts/_index.md, wiki/index.md

## [2026-04-15] save | Claude SEO v1.9.0 Slides and GitHub Release
- Type: session
- Location: wiki/meta/2026-04-15-slides-and-release-session.md
- From: built 15-slide HTML presentation deck (v190.html), fixed hardcoded path in release_report.py, pushed 68 files to GitHub, tagged v1.9.0, created GitHub release with PDF asset
- Key lessons: Path.home() not hardcoded paths, git pull --rebase before big pushes, Chrome blocks file:// cross-origin images, .claude/ always in .gitignore
- Release: https://github.com/AgriciDaniel/claude-seo/releases/tag/v1.9.0

## [2026-04-15] save | Claude SEO v1.9.0 Release Report — PDF Complete
- Type: session
- Location: wiki/meta/2026-04-15-release-report-session.md
- From: full session completing the v1.9.0 PDF release report. Dark theme, 13 pages, 1.53 MB. Fixed logo (double-space filename), empty spaces, page-break orphans, file:// URL encoding.
- Key fixes: `urllib.parse.quote()` for file:// URIs; `display:table-cell` is atomic in WeasyPrint (no page-break); fixed `height:297mm` causes empty space; replaced orphan tables with paragraphs
- Challenge v2 added: keyword LEADS, $600 prize pool, deadline April 28
- Output: `~/Desktop/Claude-SEO-v1.9.0-Release-Report.pdf`

## [2026-04-14] save | Claude SEO v1.9.0 — Pro Hub Challenge Integration Session
- Type: session + 4 concept pages + 1 entity page
- Location: wiki/meta/2026-04-14-claude-seo-v190-session.md
- From: full v1.9.0 implementation session — reviewed 5 community submissions, integrated 4 new skills (seo-cluster, seo-sxo, seo-drift, seo-ecommerce), enhanced seo-hreflang, added DataForSEO cost guardrails
- Pages created: [[2026-04-14-claude-seo-v190-session]], [[Claude SEO]], [[Pro Hub Challenge]], [[Semantic Topic Clustering]], [[Search Experience Optimization]], [[SEO Drift Monitoring]]
- Review rounds: 4 (code review x3 + cybersecurity audit). Score: 87 → 93 → 97 → 85 security
- Key learnings: always verify subagent output (40-line count error caught), insertion-point bugs caught by max-effort plan review, pre-existing security debt identified (10 of 15 findings)

## [2026-04-14] save | SVG Diagram Style Guide
- Type: concept
- Location: wiki/concepts/SVG Diagram Style Guide.md
- From: extracted design tokens from 17 production SVGs in claude-ads/assets/diagrams/
- Covers: colors, typography, layout primitives, card patterns, arrow connectors, numbered circles, file naming

## [2026-04-14] save | Community CTA Footer Rollout
- Type: decision
- Location: wiki/meta/2026-04-14-community-cta-rollout.md
- From: session adding Skool community footer to 6 skill repos (claude-ads, claude-seo, claude-obsidian, claude-blog, banana-claude, claude-cybersecurity)
- Key insight: frequency calibration per tool type; single-point orchestrator instruction pattern

## [2026-04-10] save | Backlink Empire - Blog Posts, Karpathy Gist, GitHub Cross-Linking
- Type: session
- Location: wiki/meta/2026-04-10-backlink-empire-session.md
- From: full session covering blog creation (claude-obsidian + claude-canvas), Karpathy gist comment, 26 GitHub README updates with Author/community/backlink sections, homepage URLs on 10 repos, topics on 25 repos, rankenstein.pro backlinks on 5 SEO repos
- Blog posts: agricidaniel.com/blog/claude-obsidian-ai-second-brain, agricidaniel.com/blog/claude-canvas-ai-visual-production
- Impact: ~87 new backlinks from DA 96 github.com, 6 rankenstein.pro backlinks, 25 Skool community links

## [2026-04-08] save | claude-obsidian v1.4 Release Session
- Type: session
- Location: wiki/meta/claude-obsidian-v1.4-release-session.md
- From: full release cycle covering v1.1 (URL/vision/delta tracking, 3 new skills), v1.4.0 (audit response, multi-agent compat, Bases dashboard, em dash scrub, security history rewrite), and v1.4.1 (plugin install command hotfix)
- Key lessons: plugin install is 2-step (marketplace add then install), allowed-tools is not valid frontmatter, Bases uses filters/views/formulas not Dataview syntax, hook context does not survive compaction, git filter-repo needs 2 passes for full scrub

## [2026-04-08] ingest | Claude + Obsidian Ecosystem Research
- Type: research ingest
- Source: `.raw/claude-obsidian-ecosystem-research.md`
- Queries: 6 parallel web searches + 12 repo deep-reads
- Pages created: [[claude-obsidian-ecosystem]], [[cherry-picks]], [[claude-obsidian-ecosystem-research]], [[Ar9av-obsidian-wiki]], [[Nexus-claudesidian-mcp]], [[ballred-obsidian-claude-pkm]], [[rvk7895-llm-knowledge-bases]], [[kepano-obsidian-skills]], [[Claudian-YishenTu]]
- Key finding: 16+ active Claude+Obsidian projects; 13 cherry-pick features identified for v1.3.0+
- Top gap confirmed: no delta tracking, no URL ingestion, no auto-commit

## [2026-04-07] session | Full Audit, System Setup & Plugin Installation
- Type: session
- Location: wiki/meta/full-audit-and-system-setup-session.md
- From: 12-area repo audit, 3 fixes, plugin installed to local system, folder renamed

## [2026-04-07] session | claude-obsidian v1.2.0 Release Session
- Type: session
- Location: wiki/meta/claude-obsidian-v1.2.0-release-session.md
- From: full build session — v1.2.0 plan execution, cosmic-brain→claude-obsidian rename, legal/security audit, branded GIFs, PDF install guide, dual GitHub repos


- Source: `.raw/` (first ingest)
- Pages updated: [[index]], [[log]], [[hot]], [[overview]]
- Key insight: The wiki pattern turns ephemeral AI chat into compounding knowledge — one user dropped token usage by 95%.

## [2026-04-07] setup | Vault initialized

- Plugin: claude-obsidian v1.1.0
- Structure: seed files + first ingest complete
- Skills: wiki, wiki-ingest, wiki-query, wiki-lint, save, autoresearch
