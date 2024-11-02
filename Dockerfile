FROM python:3.12.7-slim-bookworm AS tubarr
LABEL authors="Teknicallity"

ENV PYTHONUNBUFFERED=1

#ENTRYPOINT ["top", "-b"]

RUN apt-get -y update && apt-get -y install build-essential

WORKDIR /etc/tubarr

COPY requirements.txt requirements.txt

RUN mkdir /etc/tubarr/.venv && \
    python -m venv --upgrade-deps --copies /etc/tubarr/.venv && \
    /etc/tubarr/.venv/bin/pip install --upgrade pip wheel && \
    /etc/tubarr/.venv/bin/pip install -r requirements.txt && \
    /etc/tubarr/.venv/bin/pip install 'uWSGI>=2.0.28'

#RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

VOLUME /etc/tubarr/config
VOLUME /etc/tubarr/media

#RUN mkdir -p /etc/tubarr/config && chmod -R 777 /etc/tubarr/config

EXPOSE 3020

ENV VIRTUAL_ENV=/etc/tubarr/.venv
ENV PATH=/etc/tubarr/.venv/bin:$PATH

RUN mkdir -p /etc/tubarr/config && \
    chown www-data:www-data /etc/tubarr/config

RUN mkdir /etc/tubarr/static && \
    python manage.py collectstatic --noinput

RUN chmod g+w .

RUN chmod +x /etc/tubarr/start.sh

CMD ["/etc/tubarr/start.sh"]
