# Builder -------------------------------------------------------------------- #
FROM ubuntu:24.04 AS builder

ENV SRC_URL=https://public.startown.ai/packages/hepmc-2.06.09.tar.gz 

RUN apt-get update && \
    apt-get install -y curl cmake ninja-build g++ libvdt-dev libtbb-dev libpcre3

WORKDIR /src
RUN curl -L ${SRC_URL} | tar -xz --strip=1
RUN cmake -GNinja -B /build \
    -DCMAKE_INSTALL_PREFIX=/opt/hepmc \
    -DCMAKE_BUILD_TYPE=Release \
    -Dmomentum=GEV \
    -Dlength=MM && \
    cmake --build /build --target install

# Runner --------------------------------------------------------------------- #
FROM ubuntu:24.04 AS runner

COPY --from=builder /opt/hepmc /opt/hepmc
CMD ["bash"]