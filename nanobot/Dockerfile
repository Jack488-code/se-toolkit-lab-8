ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}astral/uv:python3.14-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1
WORKDIR /app
RUN uv pip install --system "nanobot-ai @ https://github.com/HKUDS/nanobot/archive/e7d371ec1e6531b28898ec2c869ef338e8dd46ec.zip"
COPY entrypoint.py /app/nanobot/entrypoint.py
COPY config.json /app/nanobot/config.json
COPY workspace/ /app/nanobot/workspace/
FROM ${REGISTRY_PREFIX_DOCKER_HUB}python:3.14.2-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8
RUN apt-get update && apt-get install -y --no-install-recommends gosu && rm -rf /var/lib/apt/lists/*
RUN groupadd --system --gid 999 nonroot && useradd --system --gid 999 --uid 999 --create-home nonroot
COPY --from=builder --chown=nonroot:nonroot /usr/local /usr/local
COPY --from=builder --chown=nonroot:nonroot /app/nanobot /app/nanobot
ENV PATH="/usr/local/bin:$PATH"
RUN mkdir -p /app/nanobot/workspace/cron /app/nanobot/workspace/memory && chmod -R 777 /app/nanobot/workspace
WORKDIR /app/nanobot
CMD ["python", "/app/nanobot/entrypoint.py"]
