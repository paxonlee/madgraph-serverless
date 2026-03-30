FROM ubuntu:24.04 AS builder

ENV SRC_URL=https://public.startown.ai/packages/hepmc-2.06.09.tar.gz \
    SRC_DIR=/opt/src \
    BUILD_DIR=/opt/build \
    INSTALL_DIR=/opt/hepmc

RUN apt-get update && \
    apt-get install -y curl cmake ninja-build g++ libvdt-dev libtbb-dev libpcre3

RUN mkdir -p ${SRC_DIR} ${BUILD_DIR} ${INSTALL_DIR} && \
    curl -L ${SRC_URL} | tar -xz --strip=1 --directory=${SRC_DIR}

RUN cmake \
    -GNinja \
    -S ${SRC_DIR} \
    -B ${BUILD_DIR} \
    -DCMAKE_INSTALL_PREFIX=${INSTALL_DIR} \
    -DCMAKE_BUILD_TYPE=Release \
    -Dmomentum=GEV \
    -Dlength=MM && \
    cmake --build ${BUILD_DIR} && \
    cmake --install ${BUILD_DIR}

FROM ubuntu:24.04 AS runner

ENV DEBIAN_FRONTEND=noninteractive \
    HEPMCDIR=/opt/hepmc 

ENV CPATH=${HEPMCDIR}/include \
    LIBRARY_PATH=${HEPMCDIR}/lib \
    LD_LIBRARY_PATH=${HEPMCDIR}/lib

COPY --from=builder ${HEPMCDIR} ${HEPMCDIR}

CMD ["bash"]