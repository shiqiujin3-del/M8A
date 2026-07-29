FROM alpine:3.20

RUN apk add --no-cache openssh-client

COPY docker-entrypoint.sh /usr/local/bin/m8a-contact-bridge-tunnel
RUN chmod +x /usr/local/bin/m8a-contact-bridge-tunnel

ENTRYPOINT ["/usr/local/bin/m8a-contact-bridge-tunnel"]
