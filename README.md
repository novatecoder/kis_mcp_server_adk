# 한국투자증권 REST API MCP Server (ADK Custom)

[](https://www.python.org/downloads/)
[](https://opensource.org/licenses/MIT)

한국투자증권(KIS)의 REST API를 사용하여 주식 시세 및 계좌 정보를 조회하는 MCP(Model Context Protocol) 서버입니다.
이 프로젝트는 **안전한 조회 전용(Read-Only)** 기능에 최적화되어 있으며, `uv` 패키지 매니저를 통해 의존성을 관리합니다.

## ✨ 주요 기능

이 서버는 다음 5가지 핵심 조회 기능을 제공합니다.

1.  **주식 현재가 조회**: 실시간 주가, 전일 대비 등락, 거래량 조회
2.  **계좌 잔고 조회**: 현재 보유 중인 종목과 평가 금액 조회
3.  **주문 체결 내역**: 일별 주문 및 체결 내역 조회 (주문 목록)
4.  **기간별 주가 조회**: 특정 기간(일별)의 종목 주가 데이터 조회
5.  **차트용 히스토리**: 차트 분석을 위한 과거 주가 히스토리 조회

> 🔒 **참고:** 매수/매도와 같은 주문 기능은 포함되어 있지 않아 실수로 인한 거래를 방지합니다.

## 🛠️ 요구 사항 (Requirements)

  * Python \>= 3.13
  * [uv](https://github.com/astral-sh/uv) (최신 파이썬 패키지 매니저)

## 🚀 설치 및 설정 (Setup)

### 1\. `uv` 설치

```bash
pip install uv
```

### 2\. 프로젝트 의존성 동기화

프로젝트 루트 폴더에서 다음 명령어를 실행하여 가상환경을 생성하고 필요한 라이브러리를 설치합니다.

```bash
uv sync
```

### 3\. 환경 변수 설정 (`.env`)

프로젝트 루트에 `.env` 파일을 생성하고, 한국투자증권 API 키와 계좌 정보를 입력하세요.

**`.env` 파일 형식:**

```ini
# [필수] 한국투자증권 API 인증 정보
KIS_APP_KEY="여기에_발급받은_APP_KEY"
KIS_APP_SECRET="여기에_발급받은_APP_SECRET"

# [필수] 계좌 설정 (REAL: 실전투자 / VIRTUAL: 모의투자)
KIS_ACCOUNT_TYPE="VIRTUAL"

# [필수] 종합계좌번호 (8자리 숫자)
KIS_CANO="12345678"
```

## ✅ 테스트 실행 (Testing)

서버가 정상적으로 작동하는지 확인하기 위해 통합 테스트를 실행합니다.
별도로 서버를 켤 필요 없이, 아래 명령어 하나로 \*\*[서버 실행 -\> 테스트 수행 -\> 서버 종료]\*\*가 자동으로 진행됩니다.

```bash
# 상세 로그와 함께 테스트 실행
uv run pytest -v -s
```

## 🏃 서버 실행 (Execution)

테스트가 완료되었다면, 실제 MCP 서버를 실행하여 Claude Desktop이나 다른 MCP 클라이언트와 연결할 수 있습니다.

```bash
uv run run-server
```

## 📚 사용 가능한 도구 (Available Tools)

MCP 클라이언트에서 호출할 수 있는 도구 목록입니다.

### 1\. `inquery-stock-price` (현재가)

  * **설명:** 특정 종목의 실시간 현재가 정보를 조회합니다.
  * **파라미터:**
      * `symbol` (str): 종목코드 (예: "005930")

### 2\. `inquery-balance` (계좌 잔고)

  * **설명:** 현재 계좌의 보유 종목 및 평가 금액을 조회합니다.
  * **파라미터:** 없음

### 3\. `inquery-order-list` (주문 내역)

  * **설명:** 특정 날짜의 주문 및 체결 내역 리스트를 조회합니다.
  * **파라미터:**
      * `start_date` (str): 조회 시작일 (YYYYMMDD)
      * `end_date` (str): 조회 종료일 (YYYYMMDD)

### 4\. `inquery-stock-info` (일별 주가)

  * **설명:** 특정 기간 동안의 일별 주가 데이터를 조회합니다.
  * **파라미터:**
      * `symbol` (str): 종목코드
      * `start_date` (str): 시작일 (YYYYMMDD)
      * `end_date` (str): 종료일 (YYYYMMDD)

### 5\. `inquery-stock-history` (차트 데이터)

  * **설명:** 차트 분석 등에 활용할 수 있는 과거 주가 히스토리 데이터를 조회합니다.
  * **파라미터:**
      * `symbol` (str): 종목코드
      * `start_date` (str): 시작일 (YYYYMMDD)
      * `end_date` (str): 종료일 (YYYYMMDD)

## License

MIT License