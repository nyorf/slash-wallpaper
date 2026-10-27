import socket
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(autouse=True)
def repo_root_cwd(monkeypatch):
    # main.py opens data/ by relative path, as the image runs it from /app
    monkeypatch.chdir(REPO_ROOT)


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    def refuse(*args, **kwargs):
        raise AssertionError("tests must not open network connections")

    monkeypatch.setattr(socket.socket, "connect", refuse)
    monkeypatch.setattr(socket.socket, "connect_ex", refuse)


@pytest.fixture
def client():
    import main

    # the context manager runs the app's startup and shutdown, as uvicorn does
    with TestClient(main.app) as test_client:
        yield test_client


@pytest.fixture
def wallpaper_bytes():
    return (REPO_ROOT / "data" / "wallpaper.jpg").read_bytes()


@pytest.fixture
def robots_bytes():
    return (REPO_ROOT / "data" / "robots.txt").read_bytes()
