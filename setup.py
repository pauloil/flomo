# -*- coding:utf-8 -*-
import setuptools
import ast
from pathlib import Path
from typing import List

FILE_DIR = Path(__file__).parent.resolve()

REQUIREMENTS_SPEC = 'requirements.txt'
PACKAGE_ENTRY = 'flomo'
VERSION_FLAG = '__version__'

with open("README.md", "r") as fh:
    long_description = fh.read()


def read_requirements() -> List[str]:
    p = FILE_DIR / REQUIREMENTS_SPEC
    with open(str(p), 'r', encoding='utf-8') as f:
        rows = f.readlines()

    requirements = list()
    for r in rows:
        r = r.strip()
        if not r:
            continue

        if r.startswith('#'):
            continue

        requirements.append(r)

    return requirements


def get_version() -> str:
    p = FILE_DIR / PACKAGE_ENTRY / '__init__.py'

    version_row = None
    with open(str(p), 'r', encoding='utf-8') as f:
        r = f.readline()
        while (r):
            if r.startswith(VERSION_FLAG):
                version_row = r
                break

            r = f.readline()

    _, version = version_row.split('=')
    version = version.strip()
    version = ast.literal_eval(version)
    return version


setuptools.setup(
    name="flo-cli",
    version=get_version(),
    author="pauloil",
    author_email="pauloil29@yahoo.co.jp",
    description="Flomo unofficial API with full CRUD support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pauloil/flomo",
    packages=setuptools.find_packages(),
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': [
            'flo=flomo.cli:main',
            'flo-mcp=flomo.mcp_server:main',
        ],
    },
    classifiers=(
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    python_requires='>=3.7',
)
'''
pip uninstall flomo -y
rm -rf ./dist
rm -rf ./build
python setup.py sdist bdist_wheel
pip install -U dist/flomo-0.0.4a0-py3-none-any.whl
twine upload dist/*
'''
