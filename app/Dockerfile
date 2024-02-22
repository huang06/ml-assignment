FROM docker.io/library/python:3.10.13-slim-bookworm
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*
ARG LOGLEVEL
ENV LOGLEVEL=${LOGLEVEL:-INFO}
WORKDIR /srv/ml-assignment
COPY requirements.txt requirements.txt
RUN python3 -m pip install --no-cache-dir -r requirements.txt
COPY . .
ENTRYPOINT ["/bin/bash", "-c"]
CMD ["uvicorn app.main:app --host 0.0.0.0 --port 9527"]
