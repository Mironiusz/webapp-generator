FROM python:3.13-slim-trixie

WORKDIR /usr/src/app

COPY . .

RUN python3 -m pip install "."

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.main:app",  "--host", "0.0.0.0", "--port", "8000"]
