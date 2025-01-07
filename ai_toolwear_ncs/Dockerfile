# Copyright Intel Corporation


ARG UBUNTU_IMAGE_VERSION
FROM openvino/ubuntu20_data_runtime:2021.4.2 as builder

ENV DEBIAN_FRONTEND=noninteractive
USER root
RUN apt update && apt install -y build-essential \
    cmake \
    wget

WORKDIR /app

# Install libzmq
RUN rm -rf deps && \
    mkdir -p deps && \
    cd deps && \
    wget -q --show-progress https://github.com/zeromq/libzmq/releases/download/v4.3.4/zeromq-4.3.4.tar.gz -O zeromq.tar.gz && \
    tar xf zeromq.tar.gz && \
    cd zeromq-4.3.4 && \
    ./configure --prefix=/usr && \
    make install

# Install cjson
RUN rm -rf deps && \
    mkdir -p deps && \
    cd deps && \
    wget -q --show-progress https://github.com/DaveGamble/cJSON/archive/v1.7.12.tar.gz -O cjson.tar.gz && \
    tar xf cjson.tar.gz && \
    cd cJSON-1.7.12 && \
    mkdir build && cd build && \
    cmake -DCMAKE_INSTALL_INCLUDEDIR=/usr/include -DCMAKE_INSTALL_PREFIX=/usr .. && \
    make install

FROM openvino/ubuntu20_data_runtime:2021.4.2 as runtime

ENV DEBIAN_FRONTEND=noninteractive
USER root


# 安裝 libusb
RUN apt-get update && apt-get install -y libusb-1.0-0-dev

# Setting python env
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-distutils python3-minimal \
                    python3-pip \
                    wget && \
    rm -rf /var/lib/apt/lists/*

# RUN apt-get install -y curl

WORKDIR /app

ARG PKG_SRC
ARG EII_VERSION
ARG CONFIGMGR_VERSION
ARG MSGBUS_LIB_VERSION
ARG UTILS_LIB_VERSION
RUN wget ${PKG_SRC}/eii-utils-${UTILS_LIB_VERSION}-Linux.deb && \
    wget ${PKG_SRC}/eii-messagebus-${MSGBUS_LIB_VERSION}-Linux.deb && \
    wget ${PKG_SRC}/eii-configmanager-${CONFIGMGR_VERSION}-Linux.deb

# Installation of utils, eiimessagebus and configmgr debian packages
RUN dpkg -i /app/eii-utils-${UTILS_LIB_VERSION}-Linux.deb && \
    dpkg -i /app/eii-messagebus-${MSGBUS_LIB_VERSION}-Linux.deb && \
    dpkg -i /app/eii-configmanager-${CONFIGMGR_VERSION}-Linux.deb

ENV PYTHONPATH $PYTHONPATH:/usr/local/lib/python${PYTHON_VERSION}/dist-packages:/app/.local/lib/python${PYTHON_VERSION}/site-packages:/app

ARG PYPI_SRC
ARG MSGBUS_WHL
ARG CFGMGR_WHL



# Installation of eiimessagebus and configmgr whl packages
COPY core_libs_requirements.txt /app/
RUN if [ -z $PYPI_SRC ] ; then \
        pip3 install --no-cache-dir -r core_libs_requirements.txt; \
    else \
        wget ${PYPI_SRC}/${MSGBUS_WHL} && \
        wget ${PYPI_SRC}/${CFGMGR_WHL} && \
        pip3 install --no-cache-dir ${MSGBUS_WHL} && \
        pip3 install --no-cache-dir ${CFGMGR_WHL} ; \
    fi

# Install necessary python packages other than the packages of EII
COPY requirements.txt /app/
RUN pip3 install -r requirements.txt

ARG EII_UID
ARG EII_USER_NAME
# The EII original DOckerfile to add user
# RUN groupadd $EII_USER_NAME -g $EII_UID && \
#     useradd -r -u $EII_UID -g $EII_USER_NAME $EII_USER_NAME

# Add a new user and create a home directory for development with vscode
RUN groupadd $EII_USER_NAME -g $EII_UID && \
    useradd -m -d /home/$EII_USER_NAME -u $EII_UID -g $EII_USER_NAME $EII_USER_NAME &&\
    ############

    apt update &&\
    apt install -y x11-apps &&\
    apt-get install -y libgtk2.0-0 libgtk-3-0 libx11-dev
    ############


USER $EII_USER_NAME

COPY --from=builder /app/ /app/
COPY --from=builder /usr/lib /usr/lib
COPY --from=builder /usr/include /usr/include
HEALTHCHECK NONE

# COPY entrypoint.sh /app/
ENTRYPOINT ["./entrypoint.sh"]
