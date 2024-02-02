FROM python:3.10

# Set the proxy address
ENV PROXY_IP=192.168.10.216
ENV PROXY_PORT=17790

# Set proxy environment variables
ENV http_proxy=http://${PROXY_IP}:${PROXY_PORT}
ENV https_proxy=http://${PROXY_IP}:${PROXY_PORT}
ENV all_proxy=socks5://${PROXY_IP}:${PROXY_PORT}
ENV no_proxy=localhost,127.0.0.1,.localdomain.com,${PROXY_IP}


RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

RUN apt-get install libgl1  -y

ENV PYTHONUNBUFFERED=True \
    PORT=9090 \
    WORKERS=2 \
    THREADS=4

WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

# CMD exec gunicorn --preload --bind :$PORT --workers $WORKERS --threads $THREADS --timeout 0 _wsgi:app
CMD exec gunicorn --bind :$PORT --workers $WORKERS --threads $THREADS --timeout 0 _wsgi:app
