FROM apache/airflow:2.0.0-python3.8
COPY init.sh /opt/airflow/init.sh
ENV AIRFLOW__CORE__EXECUTOR=LocalExecutor
ENV AIRFLOW__CORE__LOAD_DEFAULT_CONNECTIONS=False
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False
ENV AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql://airflow:airflow@172.17.0.2:5432/airflow
ENV AIRFLOW__CORE__STORE_DAG_CODE=True
ENV AIRFLOW__CORE__STORE_SERIALIZED_DAGS=True
ENV AIRFLOW__WEBSERVER__EXPOSE_CONFIG=True
ENV AIRFLOW__WEBSERVER__RBAC=False
RUN airflow db upgrade
RUN airflow users create --username admin --password admin --firstname Anonymous --lastname Admin --role Admin --email admin@example.org
ENTRYPOINT ["airflow"]
CMD ["scheduler"]

