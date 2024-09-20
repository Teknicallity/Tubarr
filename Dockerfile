#FROM debian:bookworm-slim
FROM python:3.11.9-slim-bookworm AS tubarr
LABEL authors="Teknicallity"

#ENTRYPOINT ["top", "-b"]

#RUN apt update && apt -y install python3.11
WORKDIR /etc/tubarr

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /etc/tubarr/config && chmod -R 777 /etc/tubarr/config

EXPOSE 3020

ENV VIRTUAL_ENV=/opt/venv
ENV PATH=/opt/venv/bin:$PATH

RUN ["chmod", "g+w", "."]

RUN chmod +x /etc/tubarr/start.sh

CMD ["/etc/tubarr/start.sh"]
