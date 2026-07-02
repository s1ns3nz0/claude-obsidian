---
type: source
title: "DevSpace: ChatGPT를 내 컴퓨터의 로컬 코드에 연결하는 자체 호스팅 MCP 서버"
created: 2026-07-02
updated: 2026-07-02
tags:
  - source
  - mcp
  - coding-agent
  - self-hosted
status: current
related:
  - "[[DevSpace]]"
  - "[[sources/_index]]"
raw_file: ".raw/pytorch-devspace-mcp.md"
---

# Source: DevSpace — ChatGPT를 로컬 코드에 연결하는 자체 호스팅 MCP 서버

**Type**: News article (PyTorchKR 읽을거리&정보공유)
**Original URL**: https://discuss.pytorch.kr/t/devspace-chatgpt-mcp/10994
**Author**: 9bow (박정환)
**Published**: 2026-07-01
**Retrieved**: 2026-07-02

## Summary

DevSpace는 ChatGPT(또는 Claude 등 MCP 지원 클라이언트)가 사용자 컴퓨터의 로컬 프로젝트를 직접 읽고 수정하고 실행할 수 있게 해주는 자체 호스팅 MCP 서버다. 파일을 업로드하는 기존 방식을 뒤집어, 로컬에서 서버를 띄우고 사용자가 통제하는 HTTPS 터널(Cloudflare Tunnel, ngrok 등)로 노출한 뒤, 소유자 비밀번호로 연결을 승인하는 구조다. 제공 도구는 파일 읽기/쓰기/편집, 코드 검색, 셸 명령 실행, 격리된 Git 워크트리, `AGENTS.md`/`CLAUDE.md` 준수, 로컬 스킬 탐색 등. Node 22.19+ 환경에서 `npm install -g @waishnav/devspace` 후 `devspace init` / `devspace serve`로 실행. MIT 라이선스.

## Pages Created from This Source

- [[DevSpace]] — concept page (자체 호스팅 MCP 서버 패턴)

## Key Findings

1. 로컬 파일을 원격 LLM 클라이언트에 노출하되 **업로드 없이** 터널 기반으로 연결하는 패턴
2. 연결 승인은 사용자만 아는 비밀번호로 게이팅 (`devspace init` 출력 → `~/.devspace/auth.json`)
3. Claude Code처럼 `CLAUDE.md`/`AGENTS.md` 프로젝트 지침을 그대로 따름 — MCP 클라이언트 생태계 간 컨벤션 수렴 사례
4. 보안 모델은 "신뢰하는 코딩 파트너처럼 취급"을 전제로 함 — 셸 실행 권한까지 위임되는 구조라 루트 폴더 선택이 유일한 통제 지점

## Raw File

`.raw/pytorch-devspace-mcp.md` — 원문 전체 내용
