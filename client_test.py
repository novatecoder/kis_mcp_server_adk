import asyncio
import json
from fastmcp import Client  # FastMCP 클라이언트를 임포트합니다.

# 1. 서버 주소 설정 (server.py가 실행 중인 주소)
SERVER_URL = "http://127.0.0.1:8080/mcp/"

async def main():
    """클라이언트를 실행하여 서버의 도구를 테스트합니다."""
    
    print(f"{SERVER_URL} 서버에 연결 중...")
    # 클라이언트 객체 생성 (기본적으로 /mcp/ 경로로 접속합니다)
    client = Client(SERVER_URL)

    # async with 문으로 서버에 연결합니다.
    async with client:
        print("연결 성공. 'inquery-stock-price' 툴 호출 (symbol: 005930)...")
        
        try:
            # 2. 툴 호출
            # client.call_tool("툴이름", { "파라미터명": "값" })
            result = await client.call_tool(
                "inquery-stock-price", 
                {"symbol": "005930"}
            )
            
            # 3. 결과 출력 (수정된 부분)
            print("\n[성공] KIS API 응답 결과:")

            # result 객체(상자)의 content 리스트([0])에서 text(내용물)를 꺼냅니다.
            # 이 내용물은 JSON "문자열" 형태입니다.
            json_data_string = result.content[0].text

            # JSON 문자열을 파이썬 딕셔너리로 다시 변환합니다.
            final_data_dict = json.loads(json_data_string)

            # 이제 파이썬 딕셔너리를 예쁘게 출력합니다.
            print(json.dumps(final_data_dict, indent=2, ensure_ascii=False))

        except Exception as e:
            print(f"\n[실패] 툴 호출 중 에러 발생: {e}")

# 4. 비동기 메인 함수 실행
if __name__ == "__main__":
    asyncio.run(main())