FROM startown/madgraph:3.5.13

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN pip3 install --break-system-packages runpod pexpect s3fs

WORKDIR /work
COPY handler.py handler.py
ENTRYPOINT []
CMD ["python3", "-u", "handler.py"]