FROM python:3.13-slim-trixie

ARG DATA_DIR=/var/lib/backend
ARG LOG_DIR=/var/log/backend

RUN useradd --system --user-group --no-create-home app \
    && mkdir -p "${DATA_DIR}" "${LOG_DIR}" \
    && chown app:app "${DATA_DIR}" "${LOG_DIR}"

WORKDIR /usr/src/app

COPY pyproject.toml ./

RUN python -m pip install --no-cache-dir --root-user-action=ignore . \
    && rm -rf build backend.egg-info

COPY app ./app
COPY migrations ./migrations

USER app

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
