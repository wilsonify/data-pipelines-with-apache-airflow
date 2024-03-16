import json

from os.path import dirname
from http.client import HTTPConnection

import pytest
from pytest_docker_tools import build, container

fakedns_image = build(path=f"{dirname(__file__)}/../resolver-service-dns")
fakedns = container(image='{fakedns_image.id}', environment={'DNS_EXAMPLE_COM__A': '127.0.0.1', })
apiserver_image = build(path=f"{dirname(__file__)}/../resolver-service-api", )
apiserver = container(image='{apiserver_image.id}', ports={'8080/tcp': None, }, dns=['{fakedns.ips.primary}'])

@pytest.fixture(name="apiclient")
def apiclient_fixture(apiserver):
    port = apiserver.ports['8080/tcp'][0]
    return HTTPConnection(f'localhost:{port}')


def test_api_server(apiclient):
    apiclient.request('GET', '/')
    response = apiclient.getresponse()
    assert response.status == 200
    assert json.loads(response.read()) == {'result': '127.0.0.1'}
