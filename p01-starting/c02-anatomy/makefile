
docker-run:
	docker run -it \
	-p 8080:8080 \
	-v dags/download_rocket_launches.py:/opt/airflow/dags/download_rocket_launches.py \
	--name airflow \
	--entrypoint=/bin/bash apache/airflow:2.0.0-python3.8 \
	-c "$(cat init.sh)"