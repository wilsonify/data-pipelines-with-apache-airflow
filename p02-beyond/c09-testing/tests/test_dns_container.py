import socket
from http.client import HTTPConnection

import pytest
from pytest_docker_tools import build, container

fakedns_image = build(path='examples/resolver-service/dns', )
fakedns = container(image='{fakedns_image.id}', environment={'DNS_EXAMPLE_COM__A': '127.0.0.1', })
apiserver_image = build(path='examples/resolver-service/api', )
apiserver = container(image='{apiserver_image.id}', ports={'8080/tcp': None, }, dns=['{fakedns.ips.primary}'])


@pytest.fixture(name="apiclient")
def apiclient_fixture(apiserver):
    port = apiserver.ports['8080/tcp'][0]
    return HTTPConnection(f'localhost:{port}')


def test_my_frobulator_works_after_restart(apiserver):
    apiserver.restart()
    sock = socket.socket()
    sock.connect(('127.0.0.1', apiserver.ports['8080/tcp'][0]))


def test_my_frobulator(apiclient):
    sock = socket.socket()
    sock.connect(('127.0.0.1', apiclient.ports['8080/tcp'][0]))
