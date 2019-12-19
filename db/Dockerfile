FROM postgres:11

COPY dump.sql /docker-entrypoint-initdb.d/

RUN export DEBIAN_FRONTEND=noninteractive && apt-get update && apt-get install -y -q \
    net-tools \
    iproute \
    inetutils-ping \
    iptables \
    arptables \
    ebtables \
    bridge-utils \
    ethtool \
    vim