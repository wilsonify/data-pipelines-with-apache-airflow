
docker-build:
	docker build --progress=plain -t events-api:latest -f Dockerfile .

docker-stop:
	docker stop events-api || true

docker-run: docker-stop
	docker run --rm --name events-api -p 32768:5000 events-api:latest

docker-test:
	curl -o tests/output/output.json "http://localhost:32768/events?start_date=2019-01-01&end_date=2019-01-03"

