FROM ubuntu:24.04 AS builder

ENV SRC_URL=https://public.startown.ai/packages/root-6.34.10.tar.gz \
    SRC_DIR=/opt/src \
    BUILD_DIR=/opt/build \
    INSTALL_DIR=/opt/root

RUN apt-get update && \
    apt-get install -y curl ninja-build && \
    apt-get install -y binutils cmake dpkg-dev g++ gcc libssl-dev git libx11-dev \
    libxext-dev libxft-dev libxpm-dev python3 libtbb-dev libvdt-dev libgif-dev && \
    apt-get install -y gfortran libpcre3-dev \
    libglu1-mesa-dev libglew-dev libftgl-dev \
    libfftw3-dev libcfitsio-dev libgraphviz-dev \
    libavahi-compat-libdnssd-dev libldap2-dev \
    python3-dev python3-numpy libxml2-dev libkrb5-dev \
    libgsl-dev qtwebengine5-dev nlohmann-json3-dev libmysqlclient-dev \
    libgl2ps-dev \
    liblzma-dev libxxhash-dev liblz4-dev libzstd-dev

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
    ROOT_DIR=/opt/root 

ENV CPATH=${ROOT_DIR}/include \
    LIBRARY_PATH=${ROOT_DIR}/lib \
    LD_LIBRARY_PATH=${ROOT_DIR}/lib \
    PYTHONPATH=${ROOT_DIR}/lib \
    PATH=${ROOT_DIR}/bin:${PATH}

COPY --from=builder ${ROOT_DIR} ${ROOT_DIR}

CMD ["bash"]