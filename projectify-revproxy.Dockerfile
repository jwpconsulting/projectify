FROM docker.io/nixos/nix:2.22.3 as builder

COPY revproxy /tmp/build
WORKDIR /tmp/build

FROM builder as build-revproxy
# https://marcopolo.io/code/nix-and-small-containers/
# https://mitchellh.com/writing/nix-with-dockerfiles
RUN echo "experimental-features = nix-command flakes" > /etc/nix/nix.conf \
    && nix build .#projectify-revproxy \
    && mkdir -p /tmp/nix-store-closure \
    && nix-store -qR result > /tmp/nix-store-closure-files \
    && xargs -a /tmp/nix-store-closure-files -I {} cp -a {} /tmp/nix-store-closure/

FROM scratch as projectify-revproxy
WORKDIR /app
COPY --from=build-revproxy /tmp/nix-store-closure /nix/store
COPY --from=build-revproxy /tmp/build/result /app
ENTRYPOINT ["/app/bin/projectify-revproxy"]
