import os
import platform
import sys
from pathlib import Path

from loguru import logger

# 设置当前工作目录
os.chdir(Path(__file__).parent.parent.joinpath("backend"))

from core import settings

IS_WINDOWS = platform.system() == "Windows"  # Linux


def run():
    """pdm Launching uvicorn fastAPI run script"""
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )


def kill():
    """pdm Kill uvicorn fastAPI run script"""
    proc = kill_port(settings.port)
    if proc:
        logger.info(f"kill port {settings.port} process {proc.name()}")
    else:
        logger.info(f"port {settings.port} process not found")


# kill 指定端口进程
def kill_port(port):
    import psutil

    for proc in psutil.process_iter():
        if proc.name().find("python") == -1:
            continue
        for conns in proc.connections(kind="inet"):
            if conns.laddr.port == port:
                proc.kill()
                # logging 输出日志
                return proc
    return None
