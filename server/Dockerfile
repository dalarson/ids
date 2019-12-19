FROM ubuntu:xenial

RUN export DEBIAN_FRONTEND=noninteractive && apt-get update && apt-get install -y -q \
    net-tools \
    iproute \
    tcpdump \
    inetutils-ping \
    iptables \
    arptables \
    ebtables \
    bridge-utils \
    ethtool \
    vim \
    python3 \
    python3-pip \
    libpq-dev \
    python3-dev \
    curl \
    ssldump \
    tshark

COPY server/requirements.txt /usr/local/server/

WORKDIR /usr/local/server

RUN python3 -m pip install -r requirements.txt

COPY server /usr/local/server

ADD exfil.py exfil.py
ADD exfil.sh exfil.sh

EXPOSE 5000

ENTRYPOINT ["python3", "server.py"]
