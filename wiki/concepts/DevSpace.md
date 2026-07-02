---
type: concept
title: "DevSpace"
created: 2026-07-02
updated: 2026-07-02
tags:
  - concept
  - mcp
  - coding-agent
  - self-hosted
domain: ai-tooling
status: current
related:
  - "[[sources/DevSpace-ChatGPT-Local-MCP]]"
  - "[[concepts/_index]]"
---

# DevSpace

자체 호스팅(self-hosted) MCP 서버로, ChatGPT나 Claude 같은 MCP 클라이언트가 사용자 컴퓨터의 로컬 프로젝트 폴더를 직접 읽고 수정하고 실행할 수 있게 연결해준다. "Codex 스타일 코딩 워크플로를 ChatGPT로 가져오는 것"이 목표.

## 핵심 패턴

- **업로드 없음**: 파일을 서드파티에 전송하지 않고, 로컬에서 MCP 서버(`devspace serve`, 기본 `127.0.0.1:7676/mcp`)를 띄운 뒤 사용자가 통제하는 HTTPS 터널(Cloudflare Tunnel, ngrok, Pinggy, Tailscale Funnel)로만 노출
- **비밀번호 게이팅 승인**: `devspace init`이 출력하는 소유자 비밀번호(`~/.devspace/auth.json`)로만 연결 승인 — 클라이언트가 자동으로 들어오지 않고 명시적 승인 필요
- **범위가 한정된 워크스페이스**: 클라이언트는 승인된 프로젝트 폴더 하나만 작업 공간으로 열 수 있음
- **기존 에이전트 컨벤션 재사용**: `AGENTS.md`, `CLAUDE.md` 프로젝트 지침을 그대로 따르고, 사용자의 로컬 스킬 폴더를 탐색

## 제공 도구

파일 읽기/쓰기/편집, 코드 검색과 디렉토리 탐색, 셸 명령 실행(테스트/빌드/Git/패키지 스크립트), 병렬 세션을 위한 격리된 Git 워크트리.

## 왜 주목할 만한가

로컬 파일 시스템 접근을 원격 LLM 클라이언트에 위임하는 문제를, "업로드"가 아니라 "터널 + 비밀번호 승인"으로 푸는 접근이다. 다만 저자 스스로 "선택한 로컬 폴더에 대한 원격 접근"이며 셸 실행 권한까지 포함되므로 신뢰하는 코딩 파트너처럼 다뤄야 한다고 명시한다. 루트 폴더 선택이 유일한 사용자 통제 지점이라는 점이 보안 모델의 핵심 트레이드오프.

## 관련

- 라이선스: MIT
- GitHub: https://github.com/Waishnav/devspace
- Node `>=22.19 <27`, Linux/macOS/Windows(Git Bash·WSL) 지원

## 출처

[[sources/DevSpace-ChatGPT-Local-MCP]]
