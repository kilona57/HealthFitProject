FROM python:3.12-slim

WORKDIR /app
COPY . /app/

# Обновите pip до последней версии
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
