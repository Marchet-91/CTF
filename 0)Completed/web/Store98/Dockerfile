FROM rust:1.71-bullseye as builder

ARG TARGETPLATFORM

WORKDIR /root
RUN cargo install cargo-strip

COPY store98/Cargo.* ./
COPY store98/src ./src
COPY store98/migrations ./migrations

RUN cargo build --release && \
    cargo strip && \
    mv /root/target/release/store98 /root



FROM debian:bullseye-slim

RUN apt update && apt install -y mariadb-client
COPY --from=builder /root/store98 /
COPY store98/www /www

EXPOSE 5000

CMD ["./store98"]