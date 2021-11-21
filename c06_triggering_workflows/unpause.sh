docker exec \
c06_triggering_workflows_postgres_1 \
psql -U airflow -c \
"
UPDATE dag
SET is_paused = false;
"
