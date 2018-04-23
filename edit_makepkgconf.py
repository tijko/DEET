#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import shutil
from subprocess import Popen, PIPE


def edit_makepkg_conf(makepkg_conf):
    current_dir = os.getcwd()
    makepkg_tmp = os.path.join(current_dir, 'makepkg.conf.tmp')
    with open(makepkg_tmp, 'a+') as tmp_fh:
        with open(makepkg_conf) as conf_fh:
            for line in conf_fh.readlines():
                if line.startswith('OPTIONS='):
                    line = line.replace('strip', '!strip')
                tmp_fh.write(line)
    shutil.copyfile(makepkg_conf, 'makepkg.conf.backup')
    shutil.copyfile(makepkg_tmp, makepkg_conf)

def run_cmd(cmd):
    shell_proc = Popen(cmd.split(), stdout=PIPE, universal_newlines=True)
    output, errno = shell_proc.communicate()
    return output

def find_stripped_pkgs(pac_db):
    stripped_pkgs = []
    for pkg in filter(None, pac_db.split('\n')):
        chk_bin_file = run_cmd('file -L /usr/bin/{}'.format(pkg))
        if ('cannot open' in chk_bin_file or 
            'not stripped' in chk_bin_file or
            'text executable' in chk_bin_file):
            continue
        stripped_pkgs.append(pkg)
    return stripped_pkgs

def write_disk_usage(pkgs, filename):
    pkg_paths = ['/usr/bin/{}'.format(pkg) for pkg in pkgs]
    disk_usage = run_cmd('du -Lcbs {}'.format(' '.join(pkg_paths)))
    with open(filename, 'w+') as fh:
        fh.write(disk_usage)

def update_pacman_keys():
    packey = 'pacman-key --{}'
    packey_cmds = ['init', 'populate', 'refresh-keys']
    for cmd in packey_cmds:
        run_cmd(packey.format(cmd))

if __name__ == '__main__':
    makepkg_conf = '/etc/makepkg.conf'
    edit_makepkg_conf(makepkg_conf)
