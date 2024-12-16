# Stage 1: Build stage
FROM python:3.12.7-slim-bookworm AS build
LABEL authors="Teknicallity"

ENV PYTHONUNBUFFERED=1

RUN apt-get -y update && apt-get -y install build-essential

WORKDIR /build
COPY requirements.txt requirements.txt

RUN python -m venv --copies /build/.venv && \
    /build/.venv/bin/pip install --upgrade pip wheel --no-cache-dir && \
    /build/.venv/bin/pip install --no-cache-dir -r requirements.txt && \
    /build/.venv/bin/pip install --no-cache-dir 'uWSGI>=2.0.28'

COPY . .
RUN mkdir -p /build/config
RUN /build/.venv/bin/python manage.py migrate
RUN /build/.venv/bin/python manage.py collectstatic --noinput

# Stage 2: Runtime stage
FROM python:3.12.7-slim-bookworm AS runtime
LABEL authors="Teknicallity"

ENV PYTHONUNBUFFERED=1

WORKDIR /etc/tubarr
VOLUME /etc/tubarr/config
VOLUME /etc/tubarr/media

COPY --from=build /build/.venv /etc/tubarr/.venv
COPY --from=build /build/static /etc/tubarr/static

COPY . .

ENV VIRTUAL_ENV=/etc/tubarr/.venv
ENV PATH=/etc/tubarr/.venv/bin:$PATH

RUN mkdir -p /etc/tubarr/config && \
    chown www-data:www-data /etc/tubarr/config && \
    chmod g+w /etc/tubarr && \
    chmod +x /etc/tubarr/start.sh

EXPOSE 3020

CMD ["/etc/tubarr/start.sh"]