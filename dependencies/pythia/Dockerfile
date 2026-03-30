FROM ubuntu:24.04 AS builder

ENV SRC_URL=https://public.startown.ai/packages/pythia-8.316.tar.gz \
    SRC_DIR=/opt/src \
    BUILD_DIR=/opt/build \
    INSTALL_DIR=/opt/pythia

RUN apt-get update && \
    apt-get install -y curl g++ make rsync

COPY --from=startown/hepmc:2.06.09 /opt/hepmc /opt/hepmc
COPY --from=startown/zlib:1.3.1 /opt/zlib /opt/zlib

RUN mkdir -p ${SRC_DIR} ${BUILD_DIR} ${INSTALL_DIR} && \
    curl -L ${SRC_URL} | tar -xz --strip=1 --directory=${SRC_DIR}

RUN cd ${SRC_DIR} && \
    ./configure \
    --prefix=${INSTALL_DIR} \
    --with-hepmc2=/opt/hepmc \
    --with-gzip=/opt/zlib && \
    make -j $(nproc) && \
    make install

FROM ubuntu:24.04 AS runner

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHIA_DIR=/opt/pythia 

ENV CPATH=${PYTHIA_DIR}/include \
    LIBRARY_PATH=${PYTHIA_DIR}/lib \
    LD_LIBRARY_PATH=${PYTHIA_DIR}/lib \
    PATH=${PYTHIA_DIR}/bin:${PATH}

COPY --from=builder ${PYTHIA_DIR} ${PYTHIA_DIR}

CMD ["bash"]