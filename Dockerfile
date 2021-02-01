FROM python:3.9-slim-buster

LABEL maintainer="h.lavicka@email.cz"

RUN apt-get update && apt-get install -y -qq git build-essential dash bash csh apt-utils iproute2

RUN pip install --upgrade pip

RUN mkdir -p /workdir
WORKDIR /workdir

# python environment
COPY poetry.lock /workdir/
COPY pyproject.toml /workdir/

# support scripts
COPY install.sh /workdir/
COPY run.sh /workdir/

RUN bash install.sh

# application
COPY server.py /workdir/
COPY powerplant_payload.py /workdir/

EXPOSE 8888

CMD ["bash", "/workdir/run.sh"]
