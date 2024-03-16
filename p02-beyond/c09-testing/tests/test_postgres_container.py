import os

import pytest
from pytest_docker_tools import fetch, container


@pytest.fixture(name="postgres_container")
def postgres_fixture(postgres_credentials):
    postgres_image = fetch(repository="postgres:11.1-alpine")
    pgimage_str = str(postgres_image)
    pgenvironment = {
        "POSTGRES_USER": postgres_credentials.username,
        "POSTGRES_PASSWORD": postgres_credentials.password,
    }
    pgport = {"5432/tcp": None}
    pgvol = {
        os.path.join(os.path.dirname(__file__), "postgres-init.sql"): {
            "bind": "/docker-entrypoint-initdb.d/postgres-init.sql"
        }
    }
    pgc = container(
        image=pgimage_str,
        environment=pgenvironment,
        ports=pgport,
        volumes=pgvol,
    )

    return pgc



def test_call_fixture(postgres_container):
    postgres_container.start()
    n = postgres_container.name
    p = postgres_container.ports['5432/tcp'][0]
    msg = f"Running Postgres container named {n} on port {p}."
    print(msg)
    postgres_container.stop()
