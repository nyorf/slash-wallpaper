FROM quay.io/fedora/python-311

LABEL maintainer="me@nyorf.com"

COPY requirements.txt requirements.txt

COPY data/wallpaper.jpg data/wallpaper.jpg

RUN pip3 install -r requirements.txt

COPY main.py main.py

CMD ["uvicorn", "main:app"]
