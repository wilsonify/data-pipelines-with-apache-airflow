airflow db init && \
airflow users create \
--username admin \
--password admin \
--firstname Anonymous \
--lastname Admin \
--role Admin \
--email admin@example.org && \
airflow connections add \
--conn-type postgres \
--conn-host localhost \
--conn-login postgres \
--conn-password mysecretpassword \
my_postgres
