FROM debian:buster-slim

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt install -qy \
    wget

# Install R.
#RUN apt install -qy r-base

# Install SSH.
RUN apt install -qy openssh-server

# Install Python through miniconda.
RUN wget -qO miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    /bin/bash miniconda.sh -b -p /usr/lib/miniconda3 && \
    rm -f miniconda.sh && \
    ln -s /usr/lib/miniconda3/bin/conda /usr/bin/conda && \
    conda update -n base -c defaults conda

# PyAgrum dependencies.
RUN apt install -qy graphviz

# Clean up.
RUN apt-get remove -y \
    wget \
    && apt-get clean

# Keep container up.
CMD ["tail", "-f", "/dev/null"]

