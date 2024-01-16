FROM python:latest

WORKDIR /src

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt && pip install .

ENV TOKEN="abc"
ENV PORT=8020

WORKDIR /src/hydrus_viewer
ENTRYPOINT hydrus_viewer --port=${PORT} ${TOKEN}

