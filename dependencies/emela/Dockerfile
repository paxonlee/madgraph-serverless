# Builder -------------------------------------------------------------------- #
FROM ubuntu:24.04 AS builder

ENV SRC_URL=https://public.startown.ai/packages/emela-1.0.1.tar.gz 

RUN apt-get update && \
    apt-get install -y curl cmake ninja-build g++ gfortran

WORKDIR /src
RUN curl -L ${SRC_URL} | tar -xz --strip=1
RUN cmake -GNinja -B /build \
    -DCMAKE_INSTALL_PREFIX=/opt/emela \
    -DCMAKE_BUILD_TYPE=Release && \
    cmake --build /build && \
    cmake --install /build

# Runner --------------------------------------------------------------------- #
FROM ubuntu:24.04 AS runner

COPY --from=builder /opt/emela /opt/emela
CMD ["bash"]
