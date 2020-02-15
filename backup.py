# coding=u8
import os
import sys
import argparse
import subprocess
from subprocess import PIPE
from gitlab import Gitlab
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper




def load_yml(conf_path):
    with open(conf_path, 'r') as f:
        data = load(f, Loader=Loader)
        return data


def execute_cmd(cmd, wait=False):
    p = subprocess.Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    if wait:
        p.wait()


def cloneProject(url, dest_path):
    print(url)
    os.makedirs(dest_path, exist_ok=True)
    cmd = f"cd {dest_path} ; git clone {url} "
    print(cmd)
    execute_cmd(cmd)


def backup(opts):
    data = load_yml(opts.config)
    dest_path = data['dest_path']
    gl = Gitlab(data['server'], api_version=4, private_token=data['private_token'])

    os.makedirs(dest_path, exist_ok=True)

    for proj in gl.projects.list(owned=True):
        name_with_namespace = proj.attributes['name_with_namespace']
        ssh_url_to_repo = proj.attributes['ssh_url_to_repo']
        cloneProject(ssh_url_to_repo, dest_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', dest='config', type=str, required=False, help='e.g.: python backup.py -c me.config')

    if len(sys.argv) == 1:
        parser.print_help()
        exit()

    opts = parser.parse_args()
    load_yml(opts.config)
    backup(opts)


