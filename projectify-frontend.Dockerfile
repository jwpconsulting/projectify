FROM docker.io/nixos/nix:2.22.3 as builder

COPY frontend /tmp/build
WORKDIR /tmp/build

FROM builder as build-frontend
# https://marcopolo.io/code/nix-and-small-containers/
# https://mitchellh.com/writing/nix-with-dockerfiles
RUN echo "experimental-features = nix-command flakes" > /etc/nix/nix.conf \
    && nix build .#projectify-frontend-node \
    && mkdir -p /tmp/nix-store-closure \
    && nix-store -qR result > /tmp/nix-store-closure-files \
    && xargs -a /tmp/nix-store-closure-files -I {} cp -a {} /tmp/nix-store-closure/

FROM scratch as projectify-frontend
WORKDIR /app
COPY --from=build-frontend /tmp/nix-store-closure /nix/store
COPY --from=build-frontend /tmp/build/result /app
ENTRYPOINT ["/app/bin/projectify-frontend-node"]
