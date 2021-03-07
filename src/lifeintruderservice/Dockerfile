FROM docker.io/amd64/python:3.6-slim

LABEL MAINTAINER="Florian JUDITH <florian.judith.b@gmail.com>"

FROM docker.io/amd64/python:3-alpine

LABEL maintainer="Florian JUDITH <florian.judith.b@gmail.com" \
      org.label-schema.url="https://github.com/fjudith/open-policy-agent-exercices/blob/master/README.md" \
      org.label-schema.build-date="${BUILD_DATE}" \
      org.label-schema.version="${ANSIBLE_VERSION}" \
      org.label-schema.vcs-url="https://github.com/fjudith/open-policy-agent-exercices.git" \
      org.label-schema.vcs-ref="${VCS_REF}" \
      org.label-schema.docker.dockerfile="api/rethinkdb_flask_restful_api/Dockerfile" \
      org.label-schema.description="Rethinkdb and Flask based basic RESTFul API" \
      org.label-schema.schema-version="1.0" 

ENV LANG="C.UTF-8" \
    USER="apiserver" \
    USERID="10001" \
    GROUP="apiserver" \
    GROUPID="10001"
    
ENV CARS_INVENTORY_FILE="/home/${USER}/inventory.json" \
    CARS_STATUS_FILE="/home/${USER}/status.json" \
    OPA_URL="http://localhost:8181"

COPY ./requirements.txt /tmp/requirements.txt

RUN addgroup -S ${GROUP} && adduser -S ${USER} -G ${GROUP} --uid ${USERID} && \
    apk add --update --no-cache \
    ca-certificates \
    build-base && \
    ln -s /usr/include/locale.h /usr/include/xlocale.h && \
    pip3 install --upgrade -r /tmp/requirements.txt && \
    apk del \
        build-base && \
    rm -rf /var/cache/apk/*

WORKDIR /home/${USER}

COPY ./ ./


USER ${USER}

EXPOSE 8080
CMD ["python", "./server.py"]