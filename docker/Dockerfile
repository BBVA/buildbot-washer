FROM python:3.6 as builder
RUN mkdir -p /src/washer
WORKDIR /src/washer

# Install dependencies.
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Compile worker startup script with Nuitka.
COPY worker.py ./
RUN python -m nuitka --show-progress --recurse-all --remove-output --full-compat --standalone -j5 --python-flag=-S worker.py

# Prepare the distribution directory.
RUN mv worker.dist /washer
RUN mv /washer/worker.exe /washer/buildbot-worker
RUN ldd /washer/buildbot-worker | awk '/=>/ && !/\/washer/ {print $3}' | xargs -I{} cp -nv {} /washer/
RUN cp /lib64/ld-linux-x86-64.so.2 /washer/

# Copy entrypoint and set permissions.
COPY entrypoint.sh /washer
RUN chmod a+x /washer/entrypoint.sh

FROM alpine
COPY --from=builder /washer /washer
CMD ["/washer/entrypoint.sh"]
