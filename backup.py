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
    err = p.stderr.read().decode('u8')
    print(err)
    if wait:
        p.wait()


class GitlabBackup(object):

    def __init__(self, server, private_token, backup_path):
        self.server = server
        self.private_token = private_token
        self.backup_path = backup_path
        os.makedirs(backup_path, exist_ok=True)
        self.gl = Gitlab(server, api_version=4, private_token=private_token)

    def cloneProject(self, url, name):
        print(url)
        projFullPath = os.path.join(self.backup_path, name)
        print(projFullPath)
        if os.path.exists(projFullPath):
            print(f'Project {name} already cloned ')
        else:
            cmd = f"cd {self.backup_path} ; git clone {url} "
            print(cmd)
            execute_cmd(cmd)

    def backup(self):

        for proj in self.gl.projects.list(all=True, owned=True):
            name = proj.attributes['name']
            name_with_namespace = proj.attributes['name_with_namespace']
            ssh_url_to_repo = proj.attributes['ssh_url_to_repo']
            self.cloneProject(ssh_url_to_repo, name)


def driver(opts):
    data = load_yml(opts.config)
    gb = GitlabBackup(**data)
    gb.backup()



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', dest='config', type=str, required=False, help='e.g.: python backup.py -c me.config')

    if len(sys.argv) == 1:
        parser.print_help()
        exit()

    opts = parser.parse_args()
    driver(opts)


