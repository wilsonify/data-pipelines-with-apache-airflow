airflow db upgrade && \
sleep 5 && \
airflow users create \
--username admin \
--password admin \
--firstname Anonymous \
--lastname Admin \
--role Admin \
--email admin@example.org
