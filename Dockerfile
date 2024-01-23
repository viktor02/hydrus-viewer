FROM python:latest

WORKDIR /src

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt && pip install .

ENV TOKEN="abc"
ENV PORT=8020
ENV BIND=127.0.0.1
ENV API_URL="http://0.0.0.0:45869/"

WORKDIR /src/hydrus_viewer
ENTRYPOINT hydrus_viewer --port=${PORT} --api_url=${API_URL} --bind ${BIND} ${TOKEN}
