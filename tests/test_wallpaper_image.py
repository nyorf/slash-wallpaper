import base64

import cv2
import numpy as np
import pytest

from conftest import REPO_ROOT

WALLPAPER = REPO_ROOT / "data" / "wallpaper.jpg"
SHAPE = (720, 1280, 3)

# data/wallpaper.jpg as cv2.imread decodes it; replacing the file means measuring these again
REFERENCE_MEAN_BGR = (103.4546, 95.5153, 108.7457)
REFERENCE_PIXELS_BGR = {
    (0, 0): (75, 61, 55),
    (100, 200): (41, 50, 59),
    (360, 640): (113, 122, 166),
    (500, 1000): (30, 32, 40),
    (719, 1279): (92, 95, 100),
}

# the json route re-encodes at the encoder's default quality, so its pixels differ from the file's by jpeg loss
MIN_REENCODE_PSNR_DB = 45.0


def psnr(a, b):
    mse = np.mean((a.astype(np.float64) - b.astype(np.float64)) ** 2)
    return float("inf") if mse == 0 else 10 * np.log10(255.0**2 / mse)


def mean_bgr(image):
    return image.reshape(-1, 3).mean(axis=0)


@pytest.fixture
def wallpaper_json_jpeg(client):
    response = client.get("/wallpaper")
    assert response.status_code == 200
    body = response.json()
    assert set(body) == {"image"}
    return base64.b64decode(body["image"], validate=True)


def test_imread_decodes_the_wallpaper_to_reference_pixels():
    image = cv2.imread(str(WALLPAPER))
    assert isinstance(image, np.ndarray)
    assert image.shape == SHAPE
    assert image.dtype == np.uint8
    np.testing.assert_allclose(mean_bgr(image), REFERENCE_MEAN_BGR, atol=0.05)
    for (y, x), expected in REFERENCE_PIXELS_BGR.items():
        np.testing.assert_allclose(image[y, x].astype(int), expected, atol=2, err_msg=f"pixel ({y}, {x})")


def test_wallpaper_json_carries_a_complete_jpeg(wallpaper_json_jpeg):
    assert wallpaper_json_jpeg[:3] == b"\xff\xd8\xff"
    assert wallpaper_json_jpeg[-2:] == b"\xff\xd9"


def test_wallpaper_json_decodes_to_a_720p_three_channel_uint8_image(wallpaper_json_jpeg):
    decoded = cv2.imdecode(np.frombuffer(wallpaper_json_jpeg, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    assert decoded is not None
    assert decoded.shape == SHAPE
    assert decoded.dtype == np.uint8


def test_wallpaper_json_matches_the_file_within_jpeg_loss(wallpaper_json_jpeg):
    decoded = cv2.imdecode(np.frombuffer(wallpaper_json_jpeg, dtype=np.uint8), cv2.IMREAD_COLOR)
    original = cv2.imread(str(WALLPAPER))
    assert psnr(decoded, original) >= MIN_REENCODE_PSNR_DB
    np.testing.assert_allclose(mean_bgr(decoded), REFERENCE_MEAN_BGR, atol=0.1)
    for (y, x), expected in REFERENCE_PIXELS_BGR.items():
        np.testing.assert_allclose(decoded[y, x].astype(int), expected, atol=10, err_msg=f"pixel ({y}, {x})")
