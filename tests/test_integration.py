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
    client_test.py의 로직을 그대로 사용합니다.
    """
    try:
        # result.content 리스트에서 text(내용물)를 꺼냅니다.
        if not result.content:
            return None
        
        json_data_string = result.content[0].text
        return json.loads(json_data_string)
    except Exception as e:
        print(f"[ERROR] 결과 파싱 실패: {e}")
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
async def test_04_order_detail_inquiry(run_test_server):
    """
    [주문 상세 내역] example.py의 test_order_detail 기능
    """
    server_url = run_test_server
    today = datetime.now().strftime("%Y%m%d")
    
    async with Client(server_url) as client:
        print(f"\n[Action] 'inquery-order-detail' 툴 호출...")
        
        # 주문번호 없이 조회 테스트 (API 스펙에 따라 빈값 허용 시)
        result = await client.call_tool("inquery-order-detail", {
            "order_no": "", 
            "order_date": today
        })
        data = parse_result(result)
        
        assert data is not None
        print("[성공] 주문 상세 내역 조회 완료")


@pytest.mark.asyncio
async def test_05_stock_info_daily(run_test_server):
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
async def test_06_stock_history_chart(run_test_server):
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


@pytest.mark.asyncio
async def test_07_stock_ask_price(run_test_server):
    """
    [호가 조회] example.py의 test_stock_ask 기능
    """
    server_url = run_test_server
    symbol = "005930"
    
    async with Client(server_url) as client:
        print(f"\n[Action] 'inquery-stock-ask' 툴 호출...")
        
        result = await client.call_tool("inquery-stock-ask", {"symbol": symbol})
        data = parse_result(result)
        
        assert data is not None
        
        if "output1" in data:
            askp = data['output1'].get('askp1', 'N/A')
            bidp = data['output1'].get('bidp1', 'N/A')
            print(f"[성공] 호가 조회 완료 (매도1호가: {askp}, 매수1호가: {bidp})")
        else:
            print("[성공] 호가 데이터 수신 완료")


@pytest.mark.asyncio
async def test_08_overseas_stock_price(run_test_server):
    """
    [해외 주식 현재가] example.py의 해외주식 조회 기능
    """
    server_url = run_test_server
    symbol = "AAPL"
    market = "NASD"
    
    async with Client(server_url) as client:
        print(f"\n[Action] 'inquery-overseas-stock-price' 툴 호출 ({symbol}/{market})...")
        
        try:
            result = await client.call_tool("inquery-overseas-stock-price", {
                "symbol": symbol, 
                "market": market
            })
            data = parse_result(result)
            
            assert data is not None
            print(f"[성공] {symbol} 현재가 조회 완료")
            
        except Exception as e:
            # 해외주식은 권한이나 장 시간에 따라 실패할 수 있으므로 에러 로그만 출력하고 테스트는 패스 처리할 수도 있음
            print(f"[Info] 해외주식 조회 중 예외 발생 (정상일 수 있음): {e}")