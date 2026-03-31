# Builder -------------------------------------------------------------------- #
FROM ubuntu:24.04 AS builder

ENV SRC_URL=https://public.startown.ai/packages/pythia-8.316.tar.gz 

COPY --from=startown/hepmc:2.06.09 /opt/hepmc /opt/hepmc
COPY --from=startown/zlib:1.3.1 /opt/zlib /opt/zlib
RUN apt-get update && \
    apt-get install -y curl g++ make rsync

WORKDIR /src
RUN curl -L ${SRC_URL} | tar -xz --strip=1
RUN ./configure --prefix=/opt/pythia \
    --with-hepmc2=/opt/hepmc \
    --with-gzip=/opt/zlib && \
    make -j $(nproc) && \
    make install

# Runner --------------------------------------------------------------------- #
FROM ubuntu:24.04 AS runner

COPY --from=builder /opt/pythia /opt/pythia
CMD ["bash"]
