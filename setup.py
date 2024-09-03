#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from setuptools.command.install import install
import glob
import logging
import os
import re
import shutil
import warnings
import platform

log = logging.getLogger(__name__)


def install_file(source_filename, dest_filename):
    # do not overwrite network configuration if it exists already
    # https://git.toshiki.dev/shikigotchi/shikigotchi/issues/483
    if dest_filename.startswith('/etc/network/interfaces.d/') and os.path.exists(dest_filename):
        log.info(f"{dest_filename} exists, skipping ...")
        return
    elif dest_filename.startswith('/root/') and os.path.exists(dest_filename):
        log.info(f"{dest_filename} exists, skipping ...")
        return

    log.info(f"installing {source_filename} to {dest_filename} ...")
    dest_folder = os.path.dirname(dest_filename)
    if not os.path.isdir(dest_folder):
        os.makedirs(dest_folder)

    shutil.copy2(source_filename, dest_filename)
    if dest_filename.startswith("/usr/bin/"):
        os.chmod(dest_filename, 0o755)


def install_system_files():
    data_path = None
    if os.stat("apt_packages.txt").st_size != 0:
        f = open("apt_packages.txt", "r")
        for x in f:
            os.system(f"apt-get install -y {x}")
        f.close()
    setup_path = os.path.dirname(__file__)
    if platform.machine().startswith('arm'):
        data_path = os.path.join(setup_path, "builder/data/32bit")
    elif platform.machine().startswith('aarch'):
        data_path = os.path.join(setup_path, "builder/data/64bit")

    for source_filename in glob.glob("%s/**" % data_path, recursive=True):
        if os.path.isfile(source_filename):
            dest_filename = source_filename.replace(data_path, '')
            install_file(source_filename, dest_filename)


def restart_services():
    # reload systemd units
    os.system("systemctl daemon-reload")

    # for people updating https://git.toshiki.dev/shikigotchi/shikigotchi/pull/551/files
    os.system("systemctl enable fstrim.timer")


class CustomInstall(install):
    def run(self):
        super().run()
        if os.geteuid() != 0:
            warnings.warn("Not running as root, can't install shikigotchi system files!")
            return
        install_system_files()
        restart_services()


def version(version_file):
    with open(version_file, 'rt') as vf:
        version_file_content = vf.read()

    version_match = re.search(r"__version__\s*=\s*[\"\']([^\"\']+)", version_file_content)
    if version_match:
        return version_match.groups()[0]

    return None


with open('requirements.txt') as fp:
    required = [
        line.strip()
        for line in fp
        if line.strip() and not line.startswith("--")
    ]

VERSION_FILE = 'shikigotchi/_version.py'
shikigotchi_version = version(VERSION_FILE)

setup(name='shikigotchi',
      version=shikigotchi_version,
      description='(⌐■_■) - Deep Reinforcement Learning instrumenting bettercap for WiFI shikiing.',
      author='andatoshiki && the dev team',
      author_email='hello@toshiki.dev',
      url='https://shikigotchi.toshiki.dev/',
      license='GPL',
      install_requires=[
          required,
      ],
      cmdclass={
          "install": CustomInstall,
      },
      scripts=['bin/shikigotchi'],
      package_data={'shikigotchi': ['defaults.toml', 'shikigotchi/defaults.toml', 'locale/*/LC_MESSAGES/*.mo']},
      include_package_data=True,
      packages=find_packages(),
      classifiers=[
          'Programming Language :: Python :: 3',
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Environment :: Console',
      ])
