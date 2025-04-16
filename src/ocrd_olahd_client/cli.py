import click
from ocrd.decorators import ocrd_cli_options, ocrd_cli_wrap_processor

from .processor import OlaHdClientProcessor

@click.command()
@ocrd_cli_options
def cli(*args, **kwargs):
    # OCR-D CLI spec requires input, which the processor wrapper enforces (not empty, not None)
    # but we can pass an empty string as Processor.verify will not check its existence
    kwargs['input_file_grp'] = ''
    return ocrd_cli_wrap_processor(OlaHdClientProcessor, *args, **kwargs)
