# base
FROM python:3.10-slim
LABEL maintainer="Mike Polinowski"

# arguments
ARG AIRFLOW_VERSION=2.5.1
ARG AIRFLOW_HOME=/opt/airflow
ARG PY_VER=3.10

# airflow install dir
ENV AIRFLOW_HOME=${AIRFLOW_HOME}
ENV CONSTRAINTS_URL=https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PY_VER}.txt

# install dependencies
RUN apt-get update -yqq && \
    apt-get upgrade -yqq && \
    apt-get install -yqq --no-install-recommends \ 
    wget \
    libczmq-dev \
    curl \
    libssl-dev \
    git \
    inetutils-telnet \
    bind9utils freetds-dev \
    libkrb5-dev \
    libsasl2-dev \
    libffi-dev libpq-dev \
    freetds-bin build-essential \
    default-libmysqlclient-dev \
    apt-utils \
    rsync \
    zip \
    unzip \
    gcc \
    vim \
    locales \
    && apt-get clean

# upgrade pip
# create airflow user 
# install apache airflow with subpackages
RUN pip install --upgrade pip && \
    useradd -ms /bin/bash -d ${AIRFLOW_HOME} airflow && \
    pip install apache-airflow[postgres]==${AIRFLOW_VERSION} --constraint ${CONSTRAINTS_URL}
    # pip install "apache-airflow[crypto,celery,postgres,cncf.kubernetes,docker]"==${AIRFLOW_VERSION} --constraint $(CONSTRAINTS_URL)
    
# copy start script to AIRFLOW_HOME
COPY ./entrypoint.sh ./entrypoint.sh

# make executable
RUN chmod +x ./entrypoint.sh

# give AIRFLOW_HOME to airflow user
RUN chown -R airflow: ${AIRFLOW_HOME}

# switch to airflow user
USER airflow

# go to AIRFLOW_HOME
WORKDIR ${AIRFLOW_HOME}

# create for DAGs
RUN mkdir dags

# expose webui port
EXPOSE 8080

# execute entrypoint.sh on container launch
ENTRYPOINT [ "/entrypoint.sh" ]