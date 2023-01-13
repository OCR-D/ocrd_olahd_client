import json
from os.path import join
from tempfile import gettempdir
from time import time

from pkg_resources import resource_string

from ocrd import Processor, Resolver
from ocrd_utils import getLogger
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
        LOG = getLogger('processor.OlaHdClientProcessor')
        LOG.info('Posting workspace to %s' % self.parameter['endpoint'])
        client = OlaHdClient(self.parameter['endpoint'], self.parameter['username'],
                             self.parameter['password'])
        bagger = WorkspaceBagger(Resolver(), strict=True)
        # TODO
        dest = join(gettempdir(), 'bag-%d.ocrd.zip' % int(round((time() * 1000))))
        # TODO
        ocrd_identifier = self.workspace.mets.unique_identifier
        LOG.debug('Bagging workspace')
        bagger.bag(self.workspace, ocrd_identifier, dest=dest)
        LOG.debug('Logging in')
        client.login()
        LOG.debug('POST bag')
        prev_pid = self.parameter.get('pid_previous_version', None)
        pid = client.post(dest, prev_pid=prev_pid)
        LOG.info(f"finished POST bag. Received PID: {pid}")
        if "password" in self.parameter:
            self.parameter["password"] = "*****"
        if pid:
            self.parameter["pid_previous_version"] = pid
