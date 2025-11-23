# tests/conftest.py
import pytest
import subprocess
import time
import os
import signal
import sys

# 서버가 뜰 때까지 기다릴 최대 시간 (초)
TIMEOUT = 10 
SERVER_PORT = 8080
SERVER_URL = f"http://127.0.0.1:{SERVER_PORT}/mcp/"

@pytest.fixture(scope="session")
def run_test_server():
    """
    테스트 세션 시작 전 서버를 실행하고, 끝나면 종료하는 픽스처
    """
    # 1. 서버 실행 명령어 (src 모듈 실행)
    cmd = [sys.executable, "-m", "kis_mcp_server.main"]
    
    # 환경변수 복사 (필요시 수정)
    env = os.environ.copy()
    
    # 2. 서버 프로세스 시작
    print(f"\n[Test] Starting server on port {SERVER_PORT}...")
    proc = subprocess.Popen(
        cmd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # 3. 서버가 준비될 때까지 대기 (단순 대기)
    # 실제로는 health check endpoint를 찌르는 것이 더 좋지만, 여기선 시간으로 대기
    time.sleep(3) 

    # 4. 프로세스가 죽지 않았는지 확인
    if proc.poll() is not None:
        stdout, stderr = proc.communicate()
        raise RuntimeError(f"Server failed to start:\n{stderr.decode()}")

    yield SERVER_URL  # 테스트 함수들에게 서버 주소를 전달

    # 5. 테스트 종료 후 서버 종료
    print("\n[Test] Stopping server...")
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()