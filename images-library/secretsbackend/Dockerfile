ARG AIRFLOW_BASE_IMAGE="apache/airflow:2.0.0-python3.8"
FROM ${AIRFLOW_BASE_IMAGE}

RUN pip install --user --no-cache-dir \
    hvac~=0.10 \
    apache-airflow-insideairbnb-c14-project-providers-http~=1.0.0
