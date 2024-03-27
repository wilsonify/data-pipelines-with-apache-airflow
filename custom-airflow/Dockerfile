FROM apache/airflow:2.0.0-python3.8
COPY requirements.txt /opt/airflow/requirements.txt
USER root
RUN apt-get update && apt-get upgrade -y && apt-get install -y gcc && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*
RUN pip install -r /opt/airflow/requirements.txt
USER airflow
