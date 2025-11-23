# 한국투자증권 REST API MCP Server (Custom)

[](https://www.python.org/downloads/)
[](https://opensource.org/licenses/MIT)

한국투자증권(KIS)의 REST API를 사용하여 주식 시세 및 계좌 정보를 조회하는 MCP(Model Context Protocol) 서버입니다.
이 프로젝트는 기존 `kis-mcp-server`를 커스터마이징하여 **조회 기능(시세, 잔고, 주문내역)에 특화**되었으며, `uv` 패키지 매니저를 기반으로 관리됩니다.

## ✨ 주요 기능

  - 🇰🇷 **국내 주식 조회**

      - 실시간 현재가 및 호가 조회
      - 계좌 잔고 조회
      - 일별 주문 체결 내역 조회
      - 주문 상세 내역 조회
      - 기간별 주가 및 차트 데이터 조회

  - 🌏 **해외 주식 조회**

      - 미국(나스닥/뉴욕/아멕스), 일본, 중국, 홍콩, 베트남 등
      - 실시간 현재가 조회

  - ⚡ **특징**

      - **안전한 조회 전용 모드** (주문/매수 기능 제외)
      - `uv` 기반의 빠른 환경 설정
      - 통합 테스트(`pytest`) 환경 구축
      - 비동기 처리로 빠른 응답

## ⚠️ 주의사항

이 프로젝트는 개발 중인 프로젝트입니다.

  * 본 프로젝트를 사용하여 발생하는 모든 데이터 사용 및 책임은 사용자에게 있습니다.
  * API 사용 시 한국투자증권의 이용약관 및 API 호출 제한 정책을 준수해야 합니다.
  * **민감한 정보(APP KEY, SECRET, 계좌번호)가 유출되지 않도록 `.env` 파일 관리에 주의하세요.**

## Requirements

  * Python \>= 3.13
  * [uv](https://github.com/astral-sh/uv) (Python packaging tool)

## Installation & Setup

이 프로젝트는 `uv`를 사용하여 의존성과 가상환경을 관리합니다.

### 1\. `uv` 설치 (없는 경우)

```bash
pip install uv
```

### 2\. 프로젝트 의존성 설치

프로젝트 루트 경로에서 다음 명령어를 실행하여 가상환경 생성 및 패키지를 설치합니다.

```bash
uv sync
```

### 3\. 환경 변수 설정 (`.env`)

프로젝트 루트 디렉토리에 `.env` 파일을 생성하고, 한국투자증권에서 발급받은 API 정보를 입력하세요.

**`.env` 파일 예시:**

```ini
# 한국투자증권 API 설정
KIS_APP_KEY="여기에_앱키를_입력하세요"
KIS_APP_SECRET="여기에_시크릿키를_입력하세요"

# 계좌 타입 (REAL: 실전투자, VIRTUAL: 모의투자)
KIS_ACCOUNT_TYPE="VIRTUAL"

# 종합계좌번호 (8자리)
KIS_CANO="12345678"
```

## Testing

서버가 정상적으로 작동하는지 확인하기 위해 통합 테스트를 실행할 수 있습니다.
테스트는 자동으로 로컬 서버를 실행하여 API 응답을 검증합니다.

```bash
# 전체 테스트 실행
uv run pytest

# 상세 로그와 함께 테스트 실행 (추천)
uv run pytest -v -s
```

## Execution

설정과 테스트가 완료되면 서버를 실행합니다.

```bash
# MCP 서버 실행
uv run run-server
```

실행 시 `kis_mcp_server.main:main` 엔트리포인트를 통해 서버가 시작됩니다.

## Functions Description

이 서버는 **조회 기능**만을 제공합니다.

### 🇰🇷 Domestic Stock (국내 주식)

  * **inquery\_stock\_price** - 주식 현재가 조회

      * `symbol`: 종목코드 (예: "005930")
      * Returns: 현재가, 전일대비, 거래량 등

  * **inquery\_balance** - 계좌 잔고 조회

      * Returns: 보유 종목 리스트, 평가 손익, 수익률 등

  * **inquery\_order\_list** - 일별 주문 체결 내역 조회

      * `start_date`: 조회 시작일 (YYYYMMDD)
      * `end_date`: 조회 종료일 (YYYYMMDD)

  * **inquery\_order\_detail** - 주문 상세 내역 조회

      * `order_no`: 주문번호 (선택사항)
      * `order_date`: 주문일자 (YYYYMMDD)

  * **inquery\_stock\_ask** - 호가 정보 조회

      * `symbol`: 종목코드
      * Returns: 1\~10단계 매도/매수 호가 및 잔량

### 🌏 Overseas Stock (해외 주식)

  * **inquery\_overseas\_stock\_price** - 해외 주식 현재가 조회
      * `symbol`: 종목코드 (예: "AAPL")
      * `market`: 시장코드 ("NASD", "NYSE", "AMEX", "JP", "HK", "CN" 등)

## License

MIT License