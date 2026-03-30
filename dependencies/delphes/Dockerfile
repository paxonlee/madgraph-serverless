FROM ubuntu:24.04 AS builder

ENV SRC_URL=https://public.startown.ai/packages/delphes-3.5.0.tar.gz \
    SRC_DIR=/opt/src \
    BUILD_DIR=/opt/build \
    INSTALL_DIR=/opt/delphes 

RUN apt-get update && \
    apt-get install -y curl cmake ninja-build g++ libvdt-dev libtbb-dev libpcre3

COPY --from=startown/root:6.34.10 /opt/root /opt/root
ENV PATH=/opt/root/bin:${PATH}

RUN mkdir -p ${SRC_DIR} ${BUILD_DIR} ${INSTALL_DIR} && \
    curl -L ${SRC_URL} | tar -xz --strip=1 --directory=${SRC_DIR}

RUN cmake \
    -GNinja \
    -S ${SRC_DIR} \
    -B ${BUILD_DIR} \
    -DCMAKE_INSTALL_PREFIX=${INSTALL_DIR} \
    -DCMAKE_BUILD_TYPE=Release && \
    cmake --build ${BUILD_DIR} && \
    cmake --install ${BUILD_DIR}

FROM ubuntu:24.04 AS runner

ENV DEBIAN_FRONTEND=noninteractive \
    DELPHES_DIR=/opt/delphes 

ENV CPATH=${DELPHES_DIR}/include \
    LIBRARY_PATH=${DELPHES_DIR}/lib \
    LD_LIBRARY_PATH=${DELPHES_DIR}/lib \
    PATH=${DELPHES_DIR}/bin:${PATH}

COPY --from=builder ${DELPHES_DIR} ${DELPHES_DIR}

CMD ["bash"]