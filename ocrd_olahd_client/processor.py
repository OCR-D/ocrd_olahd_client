import json
from os.path import join
from tempfile import gettempdir
from time import time

from pkg_resources import resource_string

from ocrd import Processor, Resolver
from ocrd.workspace_bagger import WorkspaceBagger

from .client import OlaHdClient

OCRD_TOOL = json.loads(resource_string(__name__, 'ocrd-tool.json').decode('utf8'))
TOOL = 'ocrd-olahd-client'

class OlaHdClientProcessor(Processor):

    def __init__(self, *args, **kwargs):
        kwargs['ocrd_tool'] = OCRD_TOOL['tools'][TOOL]
        kwargs['version'] = OCRD_TOOL['version']
        super().__init__(*args, **kwargs)

    def process(self):
        client = OlaHdClient(self.parameter['endpoint'], self.parameter['username'], self.parameter['password'])
        bagger = WorkspaceBagger(Resolver(), strict=True)
        # TODO
        dest = join(gettempdir(), 'bag-%d.zip' % int(round((time() * 1000))))
        # TODO
        ocrd_identifier = self.workspace.mets.unique_identifier
        bagger.bag(self.workspace, ocrd_identifier, dest=dest)
        client.login()
        client.post_bag(dest, prev_pid=ocrd_identifier)
