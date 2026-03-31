# Builder -------------------------------------------------------------------- #
FROM ubuntu:24.04 AS builder

ENV SRC_URL=https://public.startown.ai/packages/fastjet-3.5.1.tar.gz \
    CONTRIB_SRC_URL=https://public.startown.ai/packages/fjcontrib-1.101.tar.gz

RUN apt-get update && \
    apt-get install -y curl cmake ninja-build g++ swig python3-dev

WORKDIR /src
RUN curl -L ${SRC_URL} | tar -xz --strip=1
RUN cmake -GNinja -B /build \
    -DCMAKE_INSTALL_PREFIX=/opt/fastjet \
    -DCMAKE_BUILD_TYPE=Release \
    -DFASTJET_ENABLE_PYTHON=ON && \
    cmake --build /build && \
    cmake --install /build
RUN curl -L ${CONTRIB_SRC_URL} | tar -xz --strip=1
RUN ./configure --fastjet-config=/opt/fastjet/bin/fastjet-config && \
    make -j $(nproc) && \
    make install

# Runner --------------------------------------------------------------------- #
FROM ubuntu:24.04 AS runner

COPY --from=builder /opt/fastjet /opt/fastjet
CMD ["bash"]
