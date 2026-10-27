import subprocess
import sys

import pytest
from fastapi import FastAPI

from conftest import REPO_ROOT


def test_main_imports_with_an_empty_environment():
    result = subprocess.run(
        [sys.executable, "-c", "import main; print(type(main.app).__name__)"],
        cwd=REPO_ROOT,
        env={},
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "FastAPI"


def test_app_registers_the_wallpaper_robots_and_catch_all_routes():
    import main

    assert isinstance(main.app, FastAPI)
    paths = {route.path for route in main.app.routes}
    assert {"/wallpaper", "/robots.txt", "/robots", "/{full_path:path}"} <= paths


@pytest.mark.parametrize("path", ["/robots.txt", "/robots"])
def test_app_starts_and_serves_the_robots_file(client, robots_bytes, path):
    response = client.get(path)
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")
    assert response.content == robots_bytes


@pytest.mark.parametrize("flag", ["img", "image"])
def test_wallpaper_flag_streams_the_file_byte_for_byte(client, wallpaper_bytes, flag):
    response = client.get("/wallpaper", params={flag: "true"})
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpg"
    assert response.content == wallpaper_bytes


@pytest.mark.parametrize("path", ["/", "/no/such/page", "/wallpaper/x"])
def test_any_other_path_answers_404_json(client, path):
    response = client.get(path)
    assert response.status_code == 404
    assert response.json() == {"error": "This route is not available.", "status_code": 404}


def test_catch_all_answers_head_and_refuses_other_methods(client):
    assert client.head("/no/such/page").status_code == 404
    assert client.post("/no/such/page").status_code == 405
