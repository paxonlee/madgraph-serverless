FROM ubuntu:24.04 AS builder

ENV SRC_URL=https://public.startown.ai/packages/lhapdf-6.5.5.tar.gz \
    SRC_DIR=/opt/src \
    BUILD_DIR=/opt/build \
    INSTALL_DIR=/opt/lhapdf

RUN apt-get update && \
    apt-get install -y curl g++ make python3-dev

RUN mkdir -p ${SRC_DIR} ${BUILD_DIR} ${INSTALL_DIR} && \
    curl -L ${SRC_URL} | tar -xz --strip=1 --directory=${SRC_DIR}

RUN cd ${SRC_DIR} && \
    PYTHON=python3 ./configure --prefix=${INSTALL_DIR} && \
    make -j$(nproc) && \
    make install

FROM ubuntu:24.04 AS runner

ENV DEBIAN_FRONTEND=noninteractive \
    LHAPDF_DIR=/opt/lhapdf 

ENV CPATH=${LHAPDF_DIR}/include \
    LIBRARY_PATH=${LHAPDF_DIR}/lib \
    LD_LIBRARY_PATH=${LHAPDF_DIR}/lib \
    PYTHONPATH=${LHAPDF_DIR}/lib/python3.12/dist-packages \
    PATH=${LHAPDF_DIR}/bin:${PATH}

COPY --from=builder ${LHAPDF_DIR} ${LHAPDF_DIR}

CMD ["bash"]