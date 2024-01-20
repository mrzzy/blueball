#
# blueball
# Server
# Dockerfile
#

FROM python:3.10.2-slim 

WORKDIR /app
# install pip module requirements
COPY server/requirements.txt .
RUN pip install -r requirements.txt
# add simulation logic
COPY simulation /tmp/simulation
RUN pip install /tmp/simulation
# copy source code
COPY server/ .

CMD ["python", "server.py"]
