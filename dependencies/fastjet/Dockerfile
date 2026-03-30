FROM ubuntu:24.04 AS builder

ENV SRC_URL=https://public.startown.ai/packages/fastjet-3.5.1.tar.gz \
    SRC_DIR=/opt/src \
    BUILD_DIR=/opt/build \
    INSTALL_DIR=/opt/fastjet \
    CONTRIB_SRC_URL=https://public.startown.ai/packages/fjcontrib-1.101.tar.gz \
    CONTRIB_SRC_DIR=/opt/fjcontrib

RUN apt-get update && \
    apt-get install -y curl cmake ninja-build g++ swig python3-dev

RUN mkdir -p ${SRC_DIR} ${BUILD_DIR} ${INSTALL_DIR} ${CONTRIB_SRC_DIR} && \
    curl -L ${SRC_URL} | tar -xz --strip=1 --directory=${SRC_DIR} && \
    curl -L ${CONTRIB_SRC_URL} | tar -xz --strip=1 --directory=${CONTRIB_SRC_DIR}

RUN cmake \
    -GNinja \
    -S ${SRC_DIR} \
    -B ${BUILD_DIR} \
    -DCMAKE_INSTALL_PREFIX=${INSTALL_DIR} \
    -DCMAKE_BUILD_TYPE=Release \
    -DFASTJET_BUILD_EXAMPLES=OFF \
    -DFASTJET_ENABLE_PYTHON=ON && \
    cmake --build ${BUILD_DIR} && \
    cmake --install ${BUILD_DIR}

RUN cd ${CONTRIB_SRC_DIR} && \
    ./configure --fastjet-config=${INSTALL_DIR}/bin/fastjet-config && \
    make -j $(nproc) && \
    make install

FROM ubuntu:24.04 AS runner

ENV DEBIAN_FRONTEND=noninteractive \
    FASTJET_DIR=/opt/fastjet 

ENV CPATH=${FASTJET_DIR}/include \
    LIBRARY_PATH=${FASTJET_DIR}/lib \
    LD_LIBRARY_PATH=${FASTJET_DIR}/lib \
    PYTHONPATH=${FASTJET_DIR}/lib/python3.12/dist-packages \
    PATH=${FASTJET_DIR}/bin:${PATH}

COPY --from=builder ${FASTJET_DIR} ${FASTJET_DIR}

CMD ["bash"]