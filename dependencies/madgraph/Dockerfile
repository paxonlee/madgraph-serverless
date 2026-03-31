# Builder -------------------------------------------------------------------- #
FROM ubuntu:24.04 AS builder

ENV SRC_URL=https://public.startown.ai/packages/madgraph-3.5.13.tar.gz 

COPY --from=startown/delphes:3.5.0 /opt/delphes /opt/delphes
COPY --from=startown/emela:1.0.1 /opt/emela /opt/emela
COPY --from=startown/fastjet:3.5.1 /opt/fastjet /opt/fastjet
COPY --from=startown/hepmc:2.06.09 /opt/hepmc /opt/hepmc
COPY --from=startown/lhapdf:6.5.5 /opt/lhapdf /opt/lhapdf
COPY --from=startown/pythia:8.316 /opt/pythia /opt/pythia
COPY --from=startown/root:6.34.10 /opt/root /opt/root
COPY --from=startown/zlib:1.3.1 /opt/zlib /opt/zlib
RUN apt-get update && \
    apt-get install -y curl wget python3 python3-six gnuplot make g++

WORKDIR /opt/madgraph
RUN curl -L ${SRC_URL} | tar -xz --strip=1
RUN sed -i 's|# pythia8_path = .*|pythia8_path = /opt/pythia|' \
    /opt/madgraph/input/mg5_configuration.txt && \
    sed -i 's|# delphes_path = .*|delphes_path = /opt/delphes/bin|' \
    /opt/madgraph/input/mg5_configuration.txt && \
    sed -i 's|# fastjet = .*|fastjet = /opt/fastjet/bin/fastjet-config|' \
    /opt/madgraph/input/mg5_configuration.txt && \
    sed -i 's|# eMELA = .*|eMELA = /opt/emela/bin/eMELA-config|' \
    /opt/madgraph/input/mg5_configuration.txt && \
    sed -i '/^# lhapdf_py3 = /a lhapdf = /opt/lhapdf/bin/lhapdf-config' \
    /opt/madgraph/input/mg5_configuration.txt && \
    sed -i 's|# text_editor = .*|text_editor = vim|' \
    /opt/madgraph/input/mg5_configuration.txt && \
    sed -i 's|# auto_update = .*|auto_update = 0|' \
    /opt/madgraph/input/mg5_configuration.txt
RUN echo "install mg5amc_py8_interface" | /opt/madgraph/bin/mg5_aMC 

# Runner --------------------------------------------------------------------- #
FROM ubuntu:24.04

COPY --from=builder /opt/delphes /opt/delphes
COPY --from=builder /opt/emela /opt/emela
COPY --from=builder /opt/fastjet /opt/fastjet
COPY --from=builder /opt/hepmc /opt/hepmc
COPY --from=builder /opt/lhapdf /opt/lhapdf
COPY --from=builder /opt/madgraph /opt/madgraph
COPY --from=builder /opt/pythia /opt/pythia
COPY --from=builder /opt/root /opt/root
COPY --from=builder /opt/zlib /opt/zlib
RUN apt-get update && \
    apt-get install -y \
    python3 python3-pip python3-six \
    gfortran g++ make perl gnuplot vim wget ghostscript imagemagick \
    libvdt-dev libtbb-dev libpcre3

ENV PATH=/opt/madgraph/bin:${PATH} \
    LD_LIBRARY_PATH=/opt/lhapdf/lib

ENTRYPOINT ["mg5_aMC"]
