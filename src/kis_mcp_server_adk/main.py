# src/kis_mcp_server/main.py
import logging
from .server import mcp

def main():
    """서버를 실행하는 엔트리포인트"""
    # 로그 레벨 등을 여기서 추가 설정할 수 있습니다.
    mcp.run(transport="streamable-http")

if __name__ == "__main__":
    main()