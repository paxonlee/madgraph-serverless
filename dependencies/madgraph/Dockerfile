FROM ubuntu:24.04 AS builder

ARG SRC_URL=https://public.startown.ai/packages/madgraph-3.6.6.tar.gz \
    ARG INSTALL_DIR=/opt/madgraph

RUN apt-get update && \
    apt-get install -y curl wget python3 python3-six gnuplot make g++

RUN mkdir -p ${SRC_DIR} ${BUILD_DIR} ${INSTALL_DIR} && \
    curl -L ${SRC_URL} | tar -xz --strip=1 --directory=${SRC_DIR}

COPY --from=startown/delphes:3.5.0 /opt/delphes /opt/delphes
COPY --from=startown/emela:1.0.1 /opt/emela /opt/emela
COPY --from=startown/fastjet:3.5.1 /opt/fastjet /opt/fastjet
COPY --from=startown/hepmc:2.06.09 /opt/hepmc /opt/hepmc
COPY --from=startown/lhapdf:6.5.5 /opt/lhapdf /opt/lhapdf
COPY --from=startown/pythia:8.316 /opt/pythia /opt/pythia
COPY --from=startown/root:6.34.10 /opt/root /opt/root
COPY --from=startown/zlib:1.3.1 /opt/zlib /opt/zlib

RUN sed -i 's|# pythia8_path = .*|pythia8_path = /opt/pythia|' \
    ${INSTALL_DIR}/input/mg5_configuration.txt && \
    sed -i 's|# delphes_path = .*|delphes_path = /opt/delphes/bin|' \
    ${INSTALL_DIR}/input/mg5_configuration.txt && \
    sed -i 's|# fastjet = .*|fastjet = /opt/fastjet/bin/fastjet-config|' \
    ${INSTALL_DIR}/input/mg5_configuration.txt && \
    sed -i 's|# eMELA = .*|eMELA = /opt/emela/bin/eMELA-config|' \
    ${INSTALL_DIR}/input/mg5_configuration.txt && \
    sed -i '/^# lhapdf_py3 = /a lhapdf = /opt/lhapdf/bin/lhapdf-config' \
    ${INSTALL_DIR}/input/mg5_configuration.txt && \
    sed -i 's|# text_editor = .*|text_editor = vim|' \
    ${INSTALL_DIR}/input/mg5_configuration.txt && \
    sed -i 's|# auto_update = .*|auto_update = 0|' \
    ${INSTALL_DIR}/input/mg5_configuration.txt

RUN echo "install mg5amc_py8_interface" | ${INSTALL_DIR}/bin/mg5_aMC 

FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
    python3 python3-pip python3-six python-is-python3 \
    gfortran g++ make perl gnuplot vim wget ghostscript imagemagick \
    libvdt-dev libtbb-dev libpcre3
RUN pip3 install --upgrade setuptools --break-system-packages

COPY --from=builder /opt/zlib /opt/zlib
COPY --from=builder /opt/hepmc /opt/hepmc
COPY --from=builder /opt/lhapdf /opt/lhapdf
COPY --from=builder /opt/fastjet /opt/fastjet
COPY --from=builder /opt/emela /opt/emela
COPY --from=builder /opt/root /opt/root
COPY --from=builder /opt/pythia /opt/pythia
COPY --from=builder /opt/delphes /opt/delphes

ENV MG5_DIR=/opt/madgraph
COPY --from=builder ${MG5_DIR} ${MG5_DIR}

ENV PATH=${MG5_DIR}/bin:${PATH}
ENV LD_LIBRARY_PATH=/opt/lhapdf/lib

RUN echo '#!/bin/bash\n\
    cleanup() {\n\
    rm -f py.py\n\
    }\n\
    trap cleanup EXIT INT TERM\n\
    mg5_aMC "$@"' > /start.sh && \
    chmod +x /start.sh

ENTRYPOINT ["/start.sh"]
