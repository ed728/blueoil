#!/usr/bin/env python

import click
import time

CTX = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CTX)
def cli():
    pass

@cli.command()
@click.option(
        '-o',
        '--output',
        help='Directory to save generated config file.',
        default=None,
        required=False,
        type=click.Path(exists=True),
        dir_okay=True
)
def init(output):
    """
    Initialization procedure. Interactively generates a YAML configguration file.
    """
    bconf = ask_questions()
    conf_path = save_config(bconf, output)
    click.echo('A new config file has been created as %s.' % (conf_path))


@cli.command()
@click.argument(
        'config-file',
        type=click.File('rb')
)
@click.option(
        '--experiment-id',
        '--id',
        default=lambda: time.time(),
        help='ID to associate this project with.'
)
def train(config_file, output_dir, experiment_id):
    """
    Trains a neural network based on a given configuration file.
    """
    pass

@cli.command()
@click.argument(
        'config-file',
        type=click.File('rb')
)
@click.option(
        '--experiment-dir',
        '-e',
        type=click.Path(exists=True),
        required=True
)
@click.option(
        '--checkpoint',
        '-c',
        type=int
        help='Checkpoint number to be used.'
)
def convert(config_file, experiment_dir, checkpoint):
    """
    Converts a trained neural network into a deplyable runtime.
    """
    pass

@cli.command()
@click.argument('config-file', type=click.File())
@click.option('--input-dir', '-i', type=click.Path(exists=True), required=True, help='Input directory.')
@click.option('--output-dir', '-o', type=click.Path(), required=True)
@click.option('--experiment-dir', '-e', type=click.Path(), required=True)
@click.option('--checkpoint', '-c', type=int, help='Checkpoint number to be used.')
def predict(config_file, input_dir, output_dir, experiment_dir, checkpoint):
    """
    Runs inference.
    """
    pass

@cli.command()
@click.option('--experiment-dir', '-e', type=click.Path(exists=True), required=True)
@click.option('--port', '-p', type=int, help='Port to host the visualization on.')
def tensorboard(experiment_dir, port):
    """
    Visualizes training progress via Tensorboard.
    """
    pass



if __name__ == '__main__':
    cli()
