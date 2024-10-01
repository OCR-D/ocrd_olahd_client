ARG DOCKER_BASE_IMAGE
FROM $DOCKER_BASE_IMAGE
ARG VCS_REF
ARG BUILD_DATE
LABEL \
    maintainer="https://ocr-d.de/kontakt" \
    org.label-schema.vcs-ref=$VCS_REF \
    org.label-schema.vcs-url="https://github.com/OCR-D/ocrd_olahd_client" \
    org.label-schema.build-date=$BUILD_DATE

WORKDIR /build/ocrd_olahd_client
COPY setup.py .
COPY ocrd_olahd_client/ocrd-tool.json .
COPY ocrd_olahd_client ./ocrd_olahd_client
COPY requirements.txt .
COPY README.md .
COPY Makefile .
RUN make install
RUN rm -rf /build/ocrd_olahd_client

WORKDIR /data
VOLUME ["/data"]
