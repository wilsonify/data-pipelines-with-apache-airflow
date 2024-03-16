from os.path import dirname

from pytest_docker_tools import container, build

postgres_image = build(path=f"{dirname(__file__)}/../database-mock")
postgres_container = container(image='{postgres_image.id}')

airflow_image = build(path=f"{dirname(__file__)}/../airflow-mock")
airflow_container = container(image='{airflow_image.id}')


def test_pgc1(postgres_container):
    print(postgres_container.name)


def test_pgc2(postgres_container, airflow_container):
    print(f"postgres_container.name = {postgres_container.name}")
    print(f"airflow_container.name = {airflow_container.name}")
