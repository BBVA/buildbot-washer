FROM python:3.6 as builder
RUN mkdir -p /src/washer
WORKDIR /src/washer

# Install dependencies.
COPY washer/worker/docker/requirements.txt ./
RUN pip install -r requirements.txt

# Copy and install package code
COPY washer ./washer
COPY setup.py ./
RUN pip install .

# Compile worker startup script with Nuitka.
RUN python -m nuitka --standalone -j5 --python-flag=-S washer/worker/__main__.py

# Prepare the distribution directory.
RUN mv worker.dist /washer
RUN cp /washer/worker.exe /washer/launch-worker
RUN ldd /washer/buildbot-worker | awk '/=>/ && !/\/washer/ {print $3}' | xargs -I{} cp -nv {} /washer/

# Copy entrypoint and set permissions.
COPY entrypoint.sh /washer
RUN chmod a+x /washer/entrypoint.sh

FROM alpine:latest
COPY --from=builder /washer /washer
CMD ["/washer/entrypoint.sh"]
