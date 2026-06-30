# hash:sha256:3acfa51f7ad1723d1d2b2c3ddf6a0bd8990ab47fd23241c82ff52fdda8eb9754
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/ubuntu-desktop-igv-fiji-mambaforge:23.1.0-4-python3.10.12-fiji20231107-1617-firefox120.0-igv2.16.1-guacamole1.5.2-ubuntu22.04

ARG DEBIAN_FRONTEND=noninteractive
ARG AWS_ACCESS_KEY_ID
ARG AWS_DEFAULT_REGION
ARG AWS_SECRET_ACCESS_KEY

# (Removed COPY git-askpass / + GIT_* ARGs: the only git pip-install below is the
#  public aind-exaspim-dataset-utils repo, so no build-time git auth is needed.
#  git-askpass was a CO-only build artifact, absent from this GitHub-sourced capsule.)

ENV JAVA_HOME=/code/zulu8.80.0.17-ca-fx-jdk8.0.422-linux_x64/jre
ENV PATH=/code/zulu8.80.0.17-ca-fx-jdk8.0.422-linux_x64:$PATH
ENV AWS_REGION=us-west-2
ENV JAVA_OPTS=$JAVA_OPTS -Djava.awt.headless=true

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libblosc-dev \
        maven \
        jq \
    && rm -rf /var/lib/apt/lists/*


RUN conda install -y \
        ca-certificates==2024.7.4 \
        certifi==2024.7.4 \
        openjdk==8.0.382 \
        openssl==3.3.1 \
    && conda clean -ya

ADD "https://github.com/coder/code-server/releases/download/v4.9.0/code-server-4.9.0-linux-amd64.tar.gz" /.code-server/code-server.tar.gz
	
RUN cd /.code-server \
	&& tar -xvf code-server.tar.gz \
	&& rm code-server.tar.gz \
	&& ln -s /.code-server/code-server-4.9.0-linux-amd64/bin/code-server  /usr/bin/code-server

RUN pip install -U --no-cache-dir \
    awscli==1.33.30 \
    xmltodict==0.13.0 \
    aind-exaspim-dataset-utils@git+https://github.com/AllenNeuralDynamics/aind-exaspim-dataset-utils.git@main \

