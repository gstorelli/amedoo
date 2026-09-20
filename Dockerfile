FROM nginx:1.27-alpine

LABEL org.opencontainers.image.title="AMEDOO — sito ufficiale"
LABEL org.opencontainers.image.description="Sito statico associazioneamedoo.it"
LABEL org.opencontainers.image.source="https://github.com/gstorelli/amedoo"

COPY deploy/default.conf /etc/nginx/conf.d/default.conf
COPY . /usr/share/nginx/html/

EXPOSE 80
