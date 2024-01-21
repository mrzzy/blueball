#
# blueball
# Server
# Dockerfile
#

FROM python:3.10.2-slim 

WORKDIR /app
# generate self signed tls certificate for server
RUN openssl req -x509 -newkey rsa:4096 -sha256 -days 3650 \
  -nodes -keyout tls.key -out tls.crt -subj "/CN=example.com" \
  -addext "subjectAltName=DNS:example.com,DNS:*.example.com,IP:127.0.0.1"
# install pip module requirements
COPY server/requirements.txt .
RUN pip install -r requirements.txt
# add simulation logic
COPY simulation /tmp/simulation
RUN pip install /tmp/simulation
# copy source code
COPY server/ .


CMD ["python", "server.py", "--certificate", "tls.crt", "--private-key", "tls.key"]
