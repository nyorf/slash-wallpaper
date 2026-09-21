FROM python:3.13.7-slim@sha256:5f55cdf0c5d9dc1a415637a5ccc4a9e18663ad203673173b8cda8f8dcacef689

LABEL maintainer="me@nyorf.com"
LABEL org.opencontainers.image.title="hello-dexter"

WORKDIR /app

# shared libraries the opencv wheel loads at import
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg libsm6 libxext6 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY data/ ./data/
COPY main.py .

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# uid and gid fixed at 10001 and stated numerically in USER, so the identity holds wherever the image runs and needs
# no lookup in /etc/passwd; the pod spec asks for the same uid and gid
RUN groupadd -g 10001 app && useradd -u 10001 -g 10001 -M -s /usr/sbin/nologin app && chown -R 10001:10001 /app
USER 10001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
