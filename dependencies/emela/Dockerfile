FROM ubuntu:24.04 AS builder

ENV SRC_URL=https://public.startown.ai/packages/emela-1.0.1.tar.gz \
    SRC_DIR=/opt/src \
    BUILD_DIR=/opt/build \
    INSTALL_DIR=/opt/emela

RUN apt-get update && \
    apt-get install -y curl cmake ninja-build g++ gfortran

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
    EMELA_DIR=/opt/emela 

ENV CPATH=${EMELA_DIR}/include \
    LIBRARY_PATH=${EMELA_DIR}/lib \
    LD_LIBRARY_PATH=${EMELA_DIR}/lib \
    PATH=${EMELA_DIR}/bin:${PATH}

COPY --from=builder ${EMELA_DIR} ${EMELA_DIR}

CMD ["bash"]