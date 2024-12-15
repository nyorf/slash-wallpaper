import logging
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi import Body, Cookie, File, Form, Header, Path, Query
import io
import base64
import cv2

app = FastAPI()

@app.get(path="/wallpaper")
async def getWallpaper(img: bool = False):
    if not img:
        img = cv2.imread('data/wallpaper.jpg')
        jpg_img = cv2.imencode('.jpg', img)
        b64_string = base64.b64encode(jpg_img[1]).decode('utf-8')
        return b64_string
    else:
        image_stream = io.FileIO('data/wallpaper.jpg', mode='r')
        return StreamingResponse(content=image_stream, media_type="image/jpg")
