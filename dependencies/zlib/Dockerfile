# Builder -------------------------------------------------------------------- #
FROM ubuntu:24.04 AS builder

ENV SRC_URL=https://public.startown.ai/packages/zlib-1.3.1.tar.gz

RUN apt-get update && \
    apt-get install -y curl cmake ninja-build

WORKDIR /src
RUN curl -L ${SRC_URL} | tar -xz --strip=1
RUN cmake -GNinja -B /build \
    -DCMAKE_INSTALL_PREFIX=/opt/zlib \
    -DCMAKE_BUILD_TYPE=Release && \
    cmake --build /build && \
    cmake --install /build

# Runner --------------------------------------------------------------------- #
FROM ubuntu:24.04 AS runner

COPY --from=builder /opt/zlib /opt/zlib
CMD ["bash"]
