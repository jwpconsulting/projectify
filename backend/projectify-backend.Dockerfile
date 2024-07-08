FROM docker.io/nixos/nix:2.22.3 as builder

COPY . /tmp/build
WORKDIR /tmp/build

# https://marcopolo.io/code/nix-and-small-containers/
# https://mitchellh.com/writing/nix-with-dockerfiles
RUN echo "experimental-features = nix-command flakes" > /etc/nix/nix.conf \
    && nix build .#projectify-backend .#projectify-backend.static \
    && mkdir -p /tmp/nix-store-closure \
    && nix-store -qR result > /tmp/nix-store-closure-files \
    && xargs -a /tmp/nix-store-closure-files -I {} cp -a {} /tmp/nix-store-closure/

FROM scratch as web
WORKDIR /app
COPY --from=builder /tmp/nix-store-closure /nix/store
COPY --from=builder /tmp/build/result /app
COPY --from=builder /tmp/build/result-1-static /static
ENV STATIC_ROOT=/static

CMD ["/app/bin/gunicorn", "--config", "/app/etc/gunicorn.conf.py", "--log-config", "/app/etc/gunicorn-error.log"]

FROM scratch as worker
WORKDIR /app
COPY --from=builder /tmp/nix-store-closure /nix/store
COPY --from=builder /tmp/build/result /app
# We might not need STATIC_ROOT for a worker
COPY --from=builder /tmp/build/result-1-static /static
ENV STATIC_ROOT=/static

CMD ["/app/bin/celery", "--app", "projectify", "worker", "--concurrency", "1"]
