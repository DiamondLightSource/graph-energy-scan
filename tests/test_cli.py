import subprocess
import sys

from graph_energy_scan import __version__


def test_cli_version():
    cmd = [sys.executable, "-m", "graph_energy_scan", "--version"]
    assert subprocess.check_output(cmd).decode().strip() == __version__
