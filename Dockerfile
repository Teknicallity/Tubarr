#FROM debian:bookworm-slim
FROM python:3.11.9-slim-bookworm AS python-base
LABEL authors="Teknicallity"

#ENTRYPOINT ["top", "-b"]

#RUN apt update && apt -y install python3.11
WORKDIR /etc/tubarr

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3020

RUN python3 manage.py djangohuey

RUN chmod +x /etc/tubarr/start.sh

CMD ["/etc/tubarr/start.sh"]
