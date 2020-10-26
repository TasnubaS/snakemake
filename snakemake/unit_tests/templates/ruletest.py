import os
import sys

import subprocess as sp
from tempfile import TemporaryDirectory
import shutil
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

import common


def test_{{ ruletest.name }}():

    with TemporaryDirectory() as tmpdir:
        workdir = Path(tmpdir) / "workdir"
        data_path = "{{ ruletest.data_path }}"
        expected_path = "{{ ruletest.expected_path }}"

        # copy data to the temporary workdir
        shutil.copytree(data_path, workdir)

        # run the test job
        sp.check_output([
            "snakemake", 
            "{{ ruletest.target }}", 
            "-F", 
            "-j1",
            {% if "conda" in deploy %}
            "--use-conda",
            {% endif %}
            {% if "singularity" in deploy %}
            "--use-singularity",
            {% endif %}
            "--directory",
            workdir,
        ])

        # check the output
        common.OutputChecker(data_path, expected_path, workdir).check()