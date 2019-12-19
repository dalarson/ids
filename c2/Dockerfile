FROM ubuntu:xenial

ADD openssl.patch openssl.patch

# ensure local openssl is preferred over distribution openssl
ENV PATH /usr/local/bin:$PATH

ENV GPG_KEY 8657ABB260F056B1E5190839D9C4D26D0E604491
ENV OPENSSL_VERSION 1.1.0d
ENV CURL_VERSION 7.50.1

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
    vim

RUN set -x \
    && buildDeps=' \
    ca-certificates \
    gcc \
    libc6-dev \
    make \
    perl \
    wget \
    patch \
    zlib1g-dev \
    ' \
    && apt-get update && apt-get install -y --no-install-recommends $buildDeps \
    && rm -rf /var/lib/apt/lists/* \
    \
    && wget -O openssl.tar.gz "https://www.openssl.org/source/openssl-$OPENSSL_VERSION.tar.gz" \
    && wget -O openssl.tar.gz.asc "https://www.openssl.org/source/openssl-$OPENSSL_VERSION.tar.gz.asc" \
    && export GNUPGHOME="$(mktemp -d)" \
    && gpg --keyserver keyserver.ubuntu.com --recv-keys "$GPG_KEY" \
    && gpg --batch --verify openssl.tar.gz.asc openssl.tar.gz \
    && rm -r "$GNUPGHOME" openssl.tar.gz.asc \
    && mkdir -p /usr/src/openssl \
    && tar -xzC /usr/src/openssl --strip-components=1 -f openssl.tar.gz \
    && rm openssl.tar.gz \
    # `make test` needs to be run as a non-root user so we create user & group 'openssl' to build with
    && groupadd -r openssl && useradd -r -m -g openssl openssl \
    && chown -R openssl:openssl /usr/src/openssl \
    \
    && cd /usr/src/openssl \
    && patch -p1 < /openssl.patch \
    && su openssl -c ' \
    perl ./Configure linux-x86_64 \
    enable-ec_nistp_64_gcc_128 \
    shared \
    && make -j8 \
    ' \
    # install openssl as root
    && cd /usr/src/openssl \
    && make install_sw install_ssldirs \
    && ldconfig \
    \
    # bootstrap with the system CA certificates, a la Homebrew
    && cp /etc/ssl/certs/*.pem /usr/local/ssl/certs/ \
    && c_rehash /usr/local/ssl/certs \
    \
    && apt-get purge -y --auto-remove $buildDeps \
    && userdel -r openssl

RUN export DEBIAN_FRONTEND=noninteractive && apt-get update && apt-get install -y -q wget bzip2 build-essential

RUN wget https://curl.haxx.se/download/curl-$CURL_VERSION.tar.bz2 && \
    tar xjvf curl-$CURL_VERSION.tar.bz2 && \
    rm curl-$CURL_VERSION.tar.bz2 && \
    cd curl-$CURL_VERSION && \
    ./configure \
    --with-ssl=/usr/local/ssl \
    --without-libidn \
    --disable-static \
    --disable-ldap \
    --with-pic && \
    make && \
    make install && \
    ldconfig && \
    cd /

ADD run_command.py run_command.py
ADD cookie.txt cookie.txt
ADD run_command.sh run_command.sh
ADD exfil.sh exfil.sh

