FROM startown/madgraph:3.5.13

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /work
COPY handler.py handler.py
COPY pyproject.toml pyproject.toml
RUN pip3 install --break-system-packages uv && \
    uv pip install --system --break-system-packages .

ENTRYPOINT []
CMD ["python3", "-u", "handler.py"]
