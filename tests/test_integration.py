import pytest
import json
import asyncio
from datetime import datetime, timedelta
from fastmcp import Client

# ----------------------------------------------------------------
# 유틸리티 함수 (client_test.py의 파싱 로직 반영)
# ----------------------------------------------------------------
def parse_result(result):
    """
    MCP 툴 실행 결과(JSON 문자열)를 파싱하여 파이썬 딕셔너리로 반환합니다.
    """
    try:
        # [수정 포인트] result가 리스트인지 객체인지 확인하여 처리
        content = None
        
        if isinstance(result, list):
            # result가 바로 리스트인 경우 (현재 발생하는 상황)
            if not result:
                return None
            content = result
        elif hasattr(result, 'content'):
            # result가 .content 속성을 가진 객체인 경우 (구버전 호환)
            if not result.content:
                return None
            content = result.content
        else:
            print(f"[ERROR] 알 수 없는 결과 타입입니다: {type(result)}")
            return None

        # 리스트의 첫 번째 요소에서 텍스트 추출
        first_item = content[0]
        
        # TextContent 객체라면 .text 속성을 사용
        if hasattr(first_item, "text"):
            json_data_string = first_item.text
        else:
            # 문자열이거나 다른 형태일 경우
            json_data_string = str(first_item)

        return json.loads(json_data_string)

    except Exception as e:
        print(f"[ERROR] 결과 파싱 실패: {e} (Result Type: {type(result)})")
        return None

# ----------------------------------------------------------------
# 통합 테스트 케이스
# ----------------------------------------------------------------

@pytest.mark.asyncio
async def test_01_server_connection_and_stock_price(run_test_server):
    """
    [기본 연결 테스트] client_test.py의 내용을 반영했습니다.
    서버에 접속하고 삼성전자(005930) 현재가를 조회합니다.
    """
    server_url = run_test_server
    print(f"\n[Test] {server_url} 서버에 연결 중...")
    
    async with Client(server_url) as client:
        # 1. 툴 목록 확인 (연결 확인용)
        tools = await client.list_tools()
        tool_names = [t.name for t in tools]
        print(f"[Info] 사용 가능한 툴 목록: {tool_names}")
        assert "inquery-stock-price" in tool_names

        # 2. 주식 현재가 조회 (client_test.py 로직)
        symbol = "005930"
        print(f"[Action] 'inquery-stock-price' 툴 호출 (symbol: {symbol})...")
        
        result = await client.call_tool("inquery-stock-price", {"symbol": symbol})
        data = parse_result(result)

        # 3. 결과 검증
        assert data is not None
        assert "stck_prpr" in data, "현재가 정보(stck_prpr)가 누락되었습니다."
        
        print("\n[성공] KIS API 응답 결과:")
        print(f" - 종목명: {symbol} (삼성전자)")
        print(f" - 현재가: {data['stck_prpr']}")
        print(f" - 전일대비: {data['prdy_vrss']} ({data['prdy_ctrt']}%)")
        print(f" - 누적거래량: {data['acml_vol']}")


@pytest.mark.asyncio
async def test_02_balance_inquiry(run_test_server):
    """
    [잔고 조회] example.py의 test_balance 기능
    """
    server_url = run_test_server
    
    async with Client(server_url) as client:
        print("\n[Action] 'inquery-balance' 툴 호출...")
        result = await client.call_tool("inquery-balance", {})
        data = parse_result(result)
        
        assert data is not None
        # API 응답 구조에 따라 output1(종목별상세), output2(계좌종합) 등이 존재하는지 확인
        # (실제 응답 키는 API 명세에 따름, 여기서는 데이터 수신 여부만 체크)
        print("[성공] 계좌 잔고 데이터 수신 완료")
        # print(json.dumps(data, indent=2, ensure_ascii=False)) # 상세 데이터 확인 시 주석 해제


@pytest.mark.asyncio
async def test_03_order_list_inquiry(run_test_server):
    """
    [주문 체결 내역] example.py의 test_order_list 기능
    """
    server_url = run_test_server
    today = datetime.now().strftime("%Y%m%d")
    
    async with Client(server_url) as client:
        print(f"\n[Action] 'inquery-order-list' 툴 호출 (Date: {today})...")
        
        result = await client.call_tool("inquery-order-list", {
            "start_date": today,
            "end_date": today
        })
        data = parse_result(result)
        
        assert data is not None
        print("[성공] 일별 주문 체결 내역 조회 완료")

@pytest.mark.asyncio
async def test_04_stock_info_daily(run_test_server):
    """
    [일별 주가 조회] example.py의 test_stock_info 기능
    """
    server_url = run_test_server
    end_date = datetime.now().strftime("%Y%m%d")
    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y%m%d")
    symbol = "005930"
    
    async with Client(server_url) as client:
        print(f"\n[Action] 'inquery-stock-info' 툴 호출 ({start_date} ~ {end_date})...")
        
        result = await client.call_tool("inquery-stock-info", {
            "symbol": symbol,
            "start_date": start_date,
            "end_date": end_date
        })
        data = parse_result(result)
        
        assert data is not None
        # output 리스트 확인
        if "output2" in data and isinstance(data["output2"], list):
            print(f"[성공] {len(data['output2'])}일 간의 주가 데이터를 가져왔습니다.")
        else:
            print("[성공] 주가 데이터 수신 완료 (데이터 없음)")


@pytest.mark.asyncio
async def test_05_stock_history_chart(run_test_server):
    """
    [차트용 주가 조회] example.py의 test_stock_history 기능
    """
    server_url = run_test_server
    end_date = datetime.now().strftime("%Y%m%d")
    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y%m%d")
    symbol = "005930"
    
    async with Client(server_url) as client:
        print(f"\n[Action] 'inquery-stock-history' 툴 호출...")
        
        result = await client.call_tool("inquery-stock-history", {
            "symbol": symbol,
            "start_date": start_date,
            "end_date": end_date
        })
        data = parse_result(result)
        
        assert data is not None
        print("[성공] 차트용 주가 히스토리 조회 완료")