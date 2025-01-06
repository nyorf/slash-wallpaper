from fastapi import FastAPI
from fastapi.responses import StreamingResponse, JSONResponse
import io
import base64
import cv2


app = FastAPI()


@app.get(path="/wallpaper")
async def getWallpaper(
    img: bool = False,
    image: bool = False):
    if not img and not image:
        img = cv2.imread('data/wallpaper.jpg')
        jpg_img = cv2.imencode('.jpg', img)
        b64_string = base64.b64encode(jpg_img[1]).decode('utf-8')
        img_json = {'image': b64_string}
        return img_json
    else:
        image_stream = io.FileIO('data/wallpaper.jpg', mode='r')
        return StreamingResponse(content=image_stream, media_type="image/jpg")


@app.get(path="/robots.txt")
@app.get(path="/robots")
async def robots():
    robots_file = io.FileIO('data/robots.txt', mode='r')
    return StreamingResponse(content=robots_file, media_type="text/plain")


@app.route("/{full_path:path}")
async def catch_all(full_path: str):  # catch-all route
    response = {
        "error": "This route is not available.",
        "status_code": 404
    }
    return JSONResponse(
        content=response,
        status_code=404)
