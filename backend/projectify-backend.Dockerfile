FROM docker.io/nixos/nix:2.22.3 as builder

COPY . /tmp/build
WORKDIR /tmp/build

# https://marcopolo.io/code/nix-and-small-containers/
# https://mitchellh.com/writing/nix-with-dockerfiles
RUN echo "experimental-features = nix-command flakes" > /etc/nix/nix.conf \
    && nix build .#projectify-backend .#projectify-backend.static \
    && cp -a "$(nix-store -qR result/)" /tmp/nix-store-closure

FROM scratch
WORKDIR /app
COPY --from=builder /tmp/nix-store-closure /nix/store
COPY --from=builder /tmp/build/result /app
COPY --from=builder /tmp/build/result-1-static /static
ENV STATIC_ROOT=/static

CMD ["gunicorn", "--config", "/app/etc/gunicorn.conf.py", "--log-config", "/app/etc/gunicorn-error.log"]
