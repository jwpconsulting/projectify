FROM docker.io/nixos/nix:2.22.3 as builder

COPY backend /tmp/build
WORKDIR /tmp/build

# https://marcopolo.io/code/nix-and-small-containers/
# https://mitchellh.com/writing/nix-with-dockerfiles
RUN echo "experimental-features = nix-command flakes" > /etc/nix/nix.conf \
    && nix build .#projectify-bundle

# projectify-backend
# ==================
FROM builder as build-backend
RUN nix build .#projectify-backend \
    && mkdir -p /tmp/nix-store-closure \
    && nix-store -qR result > /tmp/nix-store-closure-files \
    && xargs -a /tmp/nix-store-closure-files -I {} cp -a {} /tmp/nix-store-closure/
FROM scratch as projectify-backend
WORKDIR /app
COPY --from=build-backend /tmp/nix-store-closure /nix/store
COPY --from=build-backend /tmp/build/result /app
ENTRYPOINT ["/app/bin/projectify-backend"]

# projectify-celery
# =================
FROM builder as build-celery
RUN nix build .#projectify-celery \
    && mkdir -p /tmp/nix-store-closure \
    && nix-store -qR result > /tmp/nix-store-closure-files \
    && xargs -a /tmp/nix-store-closure-files -I {} cp -a {} /tmp/nix-store-closure/
FROM scratch as projectify-celery
WORKDIR /app
COPY --from=build-celery /tmp/nix-store-closure /nix/store
COPY --from=build-celery /tmp/build/result /app
ENTRYPOINT ["/app/bin/projectify-celery"]

# projectify-manage
# =================
FROM builder as build-manage
RUN nix build .#projectify-manage \
    && mkdir -p /tmp/nix-store-closure \
    && nix-store -qR result > /tmp/nix-store-closure-files \
    && xargs -a /tmp/nix-store-closure-files -I {} cp -a {} /tmp/nix-store-closure/
FROM scratch as projectify-manage
WORKDIR /app
COPY --from=build-manage /tmp/nix-store-closure /nix/store
COPY --from=build-manage /tmp/build/result /app
ENTRYPOINT ["/app/bin/projectify-manage"]
