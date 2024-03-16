FROM postgres:12-alpine
COPY postgres-init.sql /docker-entrypoint-initdb.d/postgres-init.sql
EXPOSE 5432
ENV POSTGRES_USER=airflow
ENV POSTGRES_PASSWORD=airflow
ENV POSTGRES_DB=airflow
