from functools import cached_property
from os.path import join
from tempfile import gettempdir
from time import time

from ocrd import Processor, Resolver, Workspace
from ocrd.workspace_bagger import WorkspaceBagger

from .client import OlaHdClient


class OlaHdClientProcessor(Processor):

    @cached_property
    def executable(self):
        return 'ocrd-olahd-client'

    def process_workspace(self, workspace: Workspace) -> None:
        assert self.parameter
        self.logger.info('Posting workspace to %s' % self.parameter['endpoint'])
        client = OlaHdClient(self.parameter['endpoint'], self.parameter['username'],
                             self.parameter['password'])
        bagger = WorkspaceBagger(Resolver(), strict=True)
        # TODO
        dest = join(gettempdir(), 'bag-%d.ocrd.zip' % int(round((time() * 1000))))
        # TODO
        ocrd_identifier = workspace.mets.unique_identifier
        self.logger.debug('Bagging workspace')
        bagger.bag(workspace, ocrd_identifier, dest=dest)
        self.logger.debug('Logging in')
        client.login()
        self.logger.debug('POST bag')
        prev_pid = self.parameter.get('pid_previous_version', None)
        pid = client.post(dest, prev_pid=prev_pid)
        self.logger.info(f"finished POST bag. Received PID: {pid}")
        # TODO: what's the purpose of this?
        if "password" in self.parameter:
            self.parameter["password"] = "*****"
        if pid:
            self.parameter["pid_previous_version"] = pid
