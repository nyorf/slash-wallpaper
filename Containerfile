FROM python:3.13.1-slim

LABEL maintainer="me@nyorf.com"

COPY requirements.txt requirements.txt

COPY data/wallpaper.jpg data/wallpaper.jpg

RUN pip3 install -r requirements.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

COPY main.py main.py

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
