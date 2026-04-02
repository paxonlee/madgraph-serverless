# Builder -------------------------------------------------------------------- #
FROM ubuntu:24.04 AS builder

ENV SRC_URL=https://public.startown.ai/packages/lhapdf-6.5.5.tar.gz 

RUN apt-get update && \
    apt-get install -y curl g++ make python3-dev

WORKDIR /src
RUN curl -L ${SRC_URL} | tar -xz --strip=1
RUN PYTHON=python3 ./configure --prefix=/opt/lhapdf && \
    make -j$(nproc) && \
    make install

RUN ln -s /usr/bin/python3 /usr/local/bin/python && \
    PATH=/opt/lhapdf/bin:${PATH} \
    LD_LIBRARY_PATH=/opt/lhapdf/lib \
    PYTHONPATH=/opt/lhapdf/lib/python3.12/dist-packages \
    lhapdf install NNPDF23_lo_as_0130_qed

# Runner --------------------------------------------------------------------- #
FROM ubuntu:24.04 AS runner

COPY --from=builder /opt/lhapdf /opt/lhapdf
CMD ["bash"]
