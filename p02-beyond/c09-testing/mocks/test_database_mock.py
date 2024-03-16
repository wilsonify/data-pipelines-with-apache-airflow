from os.path import dirname

from pytest_docker_tools import container, build

postgres_image = build(path=f"{dirname(__file__)}/../database-mock")
postgres_container = container(image='{postgres_image.id}', ports={"5432/tcp": None}, )


def test_pgc(postgres_container):
    n = postgres_container.name
    p = postgres_container.ports['5432/tcp'][0]
    msg = f"Running Postgres container named {n} on port {p}."
    print(msg)
