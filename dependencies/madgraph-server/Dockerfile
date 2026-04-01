# Build on top of the base madgraph image
FROM startown/madgraph:3.5.13

RUN pip3 install --break-system-packages fastapi uvicorn pexpect

WORKDIR /work
COPY app.py /app/app.py
EXPOSE 8000
ENTRYPOINT []
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "/app"]
