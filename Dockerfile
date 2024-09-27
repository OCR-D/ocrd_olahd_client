FROM ocrd/core:v2.68.0 AS base
ARG VCS_REF
ARG BUILD_DATE
LABEL \
    maintainer="https://github.com/OCR-D/ocrd_olahd_client/issues" \
    org.label-schema.vcs-ref=$VCS_REF \
    org.label-schema.vcs-url="https://github.com/OCR-D/ocrd_olahd_client" \
    org.label-schema.build-date=$BUILD_DATE

WORKDIR /build/ocrd_olahd_client
COPY setup.py .
COPY ocrd_olahd_client/ocrd-tool.json .
COPY ocrd_olahd_client ./ocrd_olahd_client
COPY requirements.txt .
COPY README.md .
RUN pip install .
RUN rm -rf /build/ocrd_olahd_client

WORKDIR /data
VOLUME ["/data"]
