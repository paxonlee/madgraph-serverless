# Builder -------------------------------------------------------------------- #
FROM ubuntu:24.04 AS builder

ENV SRC_URL=https://public.startown.ai/packages/delphes-3.5.0.tar.gz 

COPY --from=startown/root:6.34.10 /opt/root /opt/root
ENV PATH=/opt/root/bin:${PATH}
RUN apt-get update && \
    apt-get install -y curl cmake ninja-build g++ libvdt-dev libtbb-dev libpcre3

WORKDIR /src
RUN curl -L ${SRC_URL} | tar -xz --strip=1
RUN cmake -GNinja -B /build \
    -DCMAKE_INSTALL_PREFIX=/opt/delphes \
    -DCMAKE_BUILD_TYPE=Release && \
    cmake --build /build && \
    cmake --install /build

# Runner --------------------------------------------------------------------- #
FROM ubuntu:24.04 AS runner

COPY --from=builder /opt/delphes /opt/delphes
CMD ["bash"]
