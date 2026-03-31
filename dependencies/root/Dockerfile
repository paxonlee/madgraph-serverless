# Builder -------------------------------------------------------------------- #
FROM ubuntu:24.04 AS builder

ENV SRC_URL=https://public.startown.ai/packages/root-6.34.10.tar.gz 

RUN apt-get update && \
    apt-get install -y curl ninja-build \
    # Required
    binutils cmake dpkg-dev g++ gcc libssl-dev git libx11-dev \
    libxext-dev libxft-dev libxpm-dev python3 libtbb-dev libvdt-dev libgif-dev \
    # Most common optional
    gfortran libpcre3-dev \
    libglu1-mesa-dev libglew-dev libftgl-dev \
    libfftw3-dev libcfitsio-dev libgraphviz-dev \
    libavahi-compat-libdnssd-dev libldap2-dev \
    python3-dev python3-numpy libxml2-dev libkrb5-dev \
    libgsl-dev qtwebengine5-dev nlohmann-json3-dev libmysqlclient-dev \
    libgl2ps-dev \
    liblzma-dev libxxhash-dev liblz4-dev libzstd-dev

WORKDIR /src
RUN curl -L ${SRC_URL} | tar -xz --strip=1
RUN cmake -GNinja -B /build \
    -DCMAKE_INSTALL_PREFIX=/opt/root \
    -DCMAKE_BUILD_TYPE=Release && \
    cmake --build /build && \
    cmake --install /build

# Runner --------------------------------------------------------------------- #
FROM ubuntu:24.04 AS runner

COPY --from=builder /opt/root /opt/root
CMD ["bash"]
