FROM docker.io/amd64/python:3-slim

LABEL maintainer="Florian JUDITH <florian.judith.b@gmail.com" \
      org.label-schema.url="https://github.com/fjudith/cloud-native-app-demo/blob/master/README.md" \
      org.label-schema.build-date="${BUILD_DATE}" \
      org.label-schema.version="${ANSIBLE_VERSION}" \
      org.label-schema.vcs-url="https://github.com/fjudith/cloud-native-app-demo.git" \
      org.label-schema.vcs-ref="${VCS_REF}" \
      org.label-schema.docker.dockerfile="src/lifeintruderservice/Dockerfile" \
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

RUN groupadd --gid ${GROUPID} ${GROUP} && useradd --uid ${USERID} --groups ${GROUP} --gid ${GROUPID} ${GROUP} && \
    echo "Acquire::Check-Valid-Until \"false\";\nAcquire::Check-Date \"false\";" | cat > /etc/apt/apt.conf.d/10no--check-valid-until && \
    apt-get update -y && apt-get install -y --no-install-recommends \
    ca-certificates \
    software-properties-common \
    build-essential && \
    pip3 install --upgrade pip && \
    pip3 install --upgrade -r /tmp/requirements.txt && \
    apt-get autoremove -yqq --purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# RUN addgroup -S ${GROUP} && adduser -S ${USER} -G ${GROUP} --uid ${USERID} && \
#     apk add --update --no-cache \
#     gcc \
#     linux-headers \
#     make \
#     musl-dev \
#     python3-dev \
#     g++ \
#     ca-certificates \
#     build-base && \
#     ln -s /usr/include/locale.h /usr/include/xlocale.h && \
#     pip3 install --upgrade pip && \
#     pip3 install --upgrade -r /tmp/requirements.txt && \
#     apk del \
#         build-base && \
#     rm -rf /var/cache/apk/*

WORKDIR /home/${USER}

COPY ./ ./


USER ${USER}

EXPOSE 8080
CMD ["python", "./server.py"]