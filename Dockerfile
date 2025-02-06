FROM python:latest

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip wheel && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install .

ENV TOKEN="abc"
ENV PORT=8020
ENV BIND=127.0.0.1
ENV API_URL="http://0.0.0.0:45869/"

EXPOSE $PORT

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl -f http://localhost:${PORT}/ || exit 1

CMD hydrus_viewer --port $PORT --api_url $API_URL --bind $BIND $TOKEN
