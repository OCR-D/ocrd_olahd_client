import click
from ocrd.decorators import ocrd_cli_options, ocrd_cli_wrap_processor

from .processor import OlaHdClientProcessor

@click.command()
@ocrd_cli_options
def cli(*args, **kwargs):
    # workaround for default input_input_file_grp: by default input_file_grp is set to 'INPUT' by
    # core because usually every processor has at least one input-file-grp. In case of this
    # processor this can cause an error so it is just removed for now
    if kwargs['input_file_grp'] == 'INPUT':
        kwargs['input_file_grp'] = ''
    return ocrd_cli_wrap_processor(OlaHdClientProcessor, *args, **kwargs)
