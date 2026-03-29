FROM ubuntu:24.04 AS builder

ENV SRC_URL=https://public.startown.ai/packages/zlib-1.3.1.tar.gz \
    SRC_DIR=/opt/src \
    BUILD_DIR=/opt/build \
    INSTALL_DIR=/opt/zlib

RUN apt-get update && \
    apt-get install -y curl cmake ninja-build

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
    ZLIB_DIR=/opt/zlib 

ENV CPATH=${ZLIB_DIR}/include \
    LIBRARY_PATH=${ZLIB_DIR}/lib \
    LD_LIBRARY_PATH=${ZLIB_DIR}/lib

COPY --from=builder ${ZLIB_DIR} ${ZLIB_DIR}

CMD ["bash"]