#!/usr/bin/env python

import click
import time
import os
import subprocess

CTX = dict(help_option_names=['-h', '--help'])

def get_script_dir():
    return os.path.dirname(os.path.realpath(__file__))

def create_dir(path):
    if not is.path.exists(path):
        os.mkdir(path)
        print("Directory {0} has been created.".format(path))

def load_yaml(config):
    cfg = {}
    cfg["CONFIG_DIR"] = os.path.dirname(os.path.realpath(config))
    cfg["YAML_FILE_NAME"] = os.path.basename(config)
    cfg["YAML_PATH"] = os.path.join(cfg["CONFIG_DIR"], cfg["YAML_NAME"])
    cfg["CONFIG_NAME"] = os.path.splitext(cfg["YAML_NAME"])[0]
    cfg["PY_CONFIG_NAME"] = cfg["CONFIG_NAME"] + '.py'
    #with open(ddconfig, 'r') as fyaml:
    yaml_cfg = yaml.safe_load(config)
    cfg["DATASET_DIR"] = yaml_cfg["train_path"]
    v = yaml_cfg["test_path"]
    if v is None:
        cfg["VALIDATION_DIR"] = cfg["DATASER_DIR"]
    else:
        cfg["VALIDATION_DIR"] = v

    cfg["DATASET_ABS_DIR"] = os.path.realpath(cfg["DATASET_DIR"])
    cfg["VALIDATION_ABS_DIR"] = os.path.realpath(cfg["VALIDATION_PATH"])

    if ((not os.path.exists(cfg["DATASET_ABS_DIR"]) or
        (not os.path.exists(cfg["VALIDATION_ABS_DIR"])):
        print("Error: dataset directory invalid.")
        exit(1)

    if (cfg["DATASET_DIR"] == cfg["DATASET_ABS_DIR"] and
        cfg["VALIDATION_DIR"] == cfg["VALIDATION_ABS_DIR"]):
        cfg["GUEST_DATA_DIR"] = '/'
    elif (cfg["DATASET_DIR"] != cfg["DATASET_ABS_DIR"] and
        cfg["VALIDATION_DIR"] != cfg["VALIDATION_ABS_DIR"]):
        cfg["GUEST_DATA_DIR"] = os.getcwd()
    else:
        print("Error: Traning and validation paths are different types. (One is an absolute path and one is a relative path.)")
        exit(1)


    return cfg

@click.group(context_settings=CTX)
def cli():
    pass

@cli.command()
def init():
    """
    Initialization procedure. Interactively generates a YAML configguration file.
    """
    conf_path = os.path.join(get_script_dir(), "config")

    print("#### Generating configuration ####")

    cmd = "docker run"
          + docker_options
          + "-v {0}:/home/blueoil/config".format(conf_path)
          + " {0}".format(docker_img)
          + "/bin/bash -c"
          + "python blueoil/blueoil_init.py && mv *.yml /home/blueoil/config"

    res = subprocess.call(cmd, shell=True)

    print("A YAML config file has been generated. Please check {0}.")


@cli.command()
@click.argument(
        'config-file',
        type=click.File('rb')
)
@click.option(
        'output-directory',
        '-o',
        default='./saved',
        help='......'
)
@click.option(
        '--experiment-id',
        '--id',
        default=None,
        help='ID to associate this project with.'
)
def train(config_file, output_dir, experiment_id):
    """
    Trains a neural network based on a given configuration file.
    """
    cfg = load_yaml(config_file)
    output_dir = os.path.realpath(output_dir)

    if experiment_id is None:
        experiment_id = time.time() # Note: change this to a proper thing.

    print("#### Running training (Id: {0}) ####".format(experiment_id))

    cmd = "docker run {0} {1}".format(docker_options, docker_img)
          + "python blueoil/blueoil_train.pt"
          + " -c /home/blueoil/config/{0} -i {1}".format(output_dir, cfg["YML_FILE_NAME"])
    subrpocess.call(cmd, shell=True)

    experiment_dir = os.path.join(output_dir, experiment_id)

    if not os.path.exists(experiment_dir):
        print("Error: checkpoint have not been properly generated.")
        exit(1)

    print("Checkpoints have been created in {0}.".format(experiment_dir))


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

    ### Run docker need to tidy-up restore uptions
    pass

@cli.command()
@click.argument(
        'config-file',
        type=click.File()
)
@click.option(
        '--input-dir',
        '-i',
        type=click.Path(exists=True),
        required=True,
        help='Input directory.'
)
@click.option(
        '--output-dir',
        '-o',
        type=click.Path(),
        required=True
)
@click.option(
        '--experiment-dir',
        '-e',
        type=click.Path(),
        required=True
)
@click.option(
        '--checkpoint',
        '-c',
        type=int,
        help='Checkpoint number to be used.'
)
def predict(config_file, input_dir, output_dir, experiment_dir, checkpoint):
    """
    Runs inference.
    """
    pass

@cli.command()
@click.option(
        '--experiment-dir',
        '-e',
        type=click.Path(exists=True),
        required=True
)
@click.option(
        '--port',
        '-p',
        type=int,
        default=6006,
        help='Port to host the visualization on.'
)
def tensorboard(experiment_dir, port):
    """
    Visualizes training progress via Tensorboard.
    """
    experiment_dir = os.path.realpath(experiment_dir)
    output_dir = os.path.dirname(experiment_dir)
    experiment_id = os.path.basename(experiment_dir)
    cuda = 0
    if "CUDA_VISIBLE_DEVICES" in os.environ:
        cuda = os.environ["CUDA_VISIBLE_DEVICES"]

    docker_options = common_docker_options
                     + " --runetime=nvidia"
                     + "-v {0}:/home/blueoil/saved".format(output_dir)
                     + "-e CUDA_VISIBLE_DEVICES={0}".format(cuda)

    tens_dir = "/home/blueoil/saved/{0}".format(experiment_id)

    cmd = "docker run " + docker_options + " -i" + "-p {0}:{0}".format(port) + img
          + "tensorboard --logdir {0} --host 0.0.0.0".format(tens_dir)
          + " --port {0}".format(poart)

    subprocess.call(cmd, shell=True)



if __name__ == '__main__':
    cli()
