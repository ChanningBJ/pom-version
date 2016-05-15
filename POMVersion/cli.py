import subprocess

import click
import sys

import Ops

@click.command()
@click.argument('path',  required=True)
@click.option('--tag-perfix',  required=False, type=click.STRING, default='api-') # TODO:是否有split的功能???


def main(path, tag_perfix):
    """My Tool does one thing, and one thing well."""
    Ops.init()
    version_tag = tag_perfix+Ops.pom_get_version()
    path_changed = Ops.git_path_changed(path, version_tag)
    if path_changed:
        print('Changes found on path '+path)
        new_version = Ops.change_pom_version()
        Ops.git_tag(tag_perfix+new_version)
    else:
        print('API version will not be changed')




