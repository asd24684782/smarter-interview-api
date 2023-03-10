FROM python:3.8-slim-buster
# use pip3 to install python modules

RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install iproute2 lshw libgeos-dev libpq-dev gcc -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY ./env/requirements.txt /root/

RUN pip3 install --upgrade pip

RUN pip3 install --upgrade -r /root/requirements.txt

COPY src/ /opt/smart/src

WORKDIR /opt/smart/src

CMD ["python3","run.py"]
