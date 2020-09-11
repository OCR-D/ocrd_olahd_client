from json import loads
from os import unlink
from os.path import join
from time import time
from tempfile import gettempdir, NamedTemporaryFile

from pytest import main, fixture, skip
from ocrd import Resolver
from ocrd.workspace_bagger import WorkspaceBagger
from ocrd_olahd_client import OlaHdClient

from tests.assets import assets

DEBUG_HTTP = 1
if DEBUG_HTTP:
    from http.client import HTTPConnection
    import logging
    HTTPConnection.debuglevel = 1
    logging.basicConfig() # you need to initialize logging, otherwise you will not see anything from requests
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

@fixture
def params():
    return loads(open('params.json').read())

@fixture
def client(params):
    return OlaHdClient(**params)

@fixture
def ocrd_identifier():
    return 'urn:test:import:kant'

@fixture
def kant_ocrdzip(ocrd_identifier):
    resolver = Resolver()
    bagger = WorkspaceBagger(resolver, strict=True)
    dest = join(gettempdir(), 'olahd-test-bag-%d.ocrd.zip' % int(round((time() * 1000))))
    ws = resolver.workspace_from_url(assets.path_to('kant_aufklaerung_1784/data/mets.xml'))
    bagger.bag(ws, ocrd_identifier, dest=dest)
    yield dest
    unlink(dest)

def test_login(client):
    skip("temporary")
    assert client.token is None
    client.login()
    assert client.token

def test_post(client, kant_ocrdzip, ocrd_identifier):
    client.login()
    # client.post('bar', ocrd_identifier)
    print(client.post(kant_ocrdzip))
    assert 0

if __name__ == '__main__':
    main([__file__])
