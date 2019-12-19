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
    curl \
    ssldump \
    w3m \
    tshark

ADD client.sh client.sh
ADD loadgen.sh loadgen.sh
