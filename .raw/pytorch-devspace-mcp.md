---
source_url: https://discuss.pytorch.kr/t/devspace-chatgpt-mcp/10994
retrieved: 2026-07-02
author: 9bow (박정환)
published: 2026-07-01
---

# DevSpace: ChatGPT를 내 컴퓨터의 로컬 코드에 연결하는 자체 호스팅 MCP 서버

## DevSpace 소개

ChatGPT에게 코드를 다루게 하려면 보통 파일을 복사해 붙여넣거나 별도 서비스에 업로드해야 합니다. DevSpace는 이 과정을 뒤집어, ChatGPT가 내 컴퓨터의 실제 프로젝트를 직접 읽고 수정하고 실행하도록 안전하게 연결하는 자체 호스팅(self-hosted) MCP 서버입니다. 프로젝트 이름 그대로 "Codex 스타일의 코딩 워크플로를 ChatGPT로 가져오는 것"을 목표로 합니다.

핵심은 "아무것도 제3자에게 업로드하지 않는다"는 점입니다. DevSpace는 사용자의 머신에서 직접 실행되고, 사용자가 직접 통제하는 터널(tunnel)을 통해 노출되며, 사용자만 알고 있는 비밀번호로 연결을 승인합니다.

DevSpace는 MCP를 지원하는 호스트라면 ChatGPT뿐 아니라 Claude 같은 클라이언트와도 동작합니다.

## 동작 방식

DevSpace는 ChatGPT(원격)와 내 컴퓨터(로컬) 사이를 보안 터널과 비밀번호 승인으로 잇습니다. `devspace serve`로 로컬 MCP 서버를 띄우면 기본 엔드포인트는 `http://127.0.0.1:7676/mcp`. 대부분 Cloudflare Tunnel, ngrok, Pinggy, Tailscale Funnel 같은 공개 HTTPS 터널로 노출하고, MCP 클라이언트는 그 공개 `/mcp` URL로 접속.

클라이언트가 연결을 시도하면 DevSpace는 소유자(Owner) 비밀번호 승인 페이지를 띄움. 비밀번호는 `devspace init` 시점에 출력되며 `~/.devspace/auth.json`에 저장. 사용자가 명시적으로 승인한 연결만 동작.

## 제공 도구

- 열린 작업 공간 안에서 파일을 읽고, 쓰고, 편집
- 코드 검색 및 디렉토리 구조 탐색
- 테스트·빌드·Git·패키지 스크립트 같은 셸 명령 실행
- 병렬 코딩 세션을 위한 격리된 Git 워크트리
- `AGENTS.md`/`CLAUDE.md` 프로젝트 지침 준수
- 사용자 스킬 폴더에서 로컬 에이전트 스킬 탐색

## 설치 및 사용법

Node `>=22.19 <27` 필요.

```bash
npm install -g @waishnav/devspace
devspace init
devspace serve
```

전역 설치 없이 `npx @waishnav/devspace init` / `npx @waishnav/devspace serve`도 가능. 설정 중 로컬 프로젝트 폴더, 로컬 포트(기본 7676), 공개 HTTPS 주소를 입력. Linux/macOS/Windows(Git Bash·WSL·MSYS2·Cygwin) 지원, PowerShell/cmd.exe 단독 환경은 미지원. 점검 명령: `devspace doctor`.

## 보안 모델

저자는 "선택한 로컬 폴더에 대한 원격 접근"이라고 명시. 루트 폴더 선택은 사용자가 결정하지만, 일단 작업 공간이 열리면 연결된 MCP 클라이언트는 셸 실행을 포함한 강력한 로컬 권한을 가짐. 연결된 클라이언트를 신뢰하는 코딩 파트너처럼 다루라고 권고.

## 라이선스

MIT 라이선스. 개인 및 상업적 목적 자유 사용 가능.

## 링크

- GitHub: https://github.com/Waishnav/devspace
- 설정 가이드: https://github.com/Waishnav/devspace/blob/main/docs/setup.md
