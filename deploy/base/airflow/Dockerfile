FROM apache/airflow:slim-2.9.3-python3.10
USER 0
COPY requirements.txt requirements.txt
RUN apt update \
    && apt install -y \
    cron \
    vim \
    && pip3 install -r requirements.txt