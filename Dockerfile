### MYHOUSE ###

### define base image
ARG SDK_VERSION
ARG ARCHITECTURE
FROM myhouseproject/myhouse-sdk-raspbian:${ARCHITECTURE}-${SDK_VERSION}

### copy files into the image
COPY . $WORKDIR
