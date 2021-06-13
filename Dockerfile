FROM python:3.8

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get -y install libpq-dev
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

ADD easycar /opt/easycar
COPY entrypoint.sh /opt/easycar/entrypoint.sh
WORKDIR /opt/easycar

RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 8000

ENTRYPOINT [ "/bin/bash", "/opt/easycar/entrypoint.sh" ]