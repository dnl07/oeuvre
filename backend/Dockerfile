FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8000

COPY ./entrypoint.sh /

ENTRYPOINT ["/entrypoint.sh"]