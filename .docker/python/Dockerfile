ARG PY_VERSION
FROM python:${PY_VERSION:-3.9-alpine3.21}

LABEL maintainer="Osiozekhai Aliu"

RUN apk update && apk upgrade && \
    apk add git build-base bash nano