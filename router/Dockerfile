FROM ubuntu:xenial

# define interface names (should be the same as in VNFD)
# r-eth0 --> lan link
# r-eth1 --> wan link 
ENV IFIN r-eth1
ENV IFOUT r-eth0 

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
    snort

ADD snort.conf /etc/snort/snort.conf
ADD entry.sh entry.sh
ADD restart_snort.sh restart_snort.sh
