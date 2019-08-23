from modules import nmap

# import lancerargs
import os
import tempfile
import pytest
import io
import sys

# TODO: Figure out a way to do Nmap tests reliably on Travis
"""def test_nmap():
    lancerargs.parse_arguments(['-T', 'scanme.nmap.org'])
    nmap.nmap_scan(False)


def test_nmap_quiet():
    lancerargs.parse_arguments(['-T', 'scanme.nmap.org'])
    nmap.nmap_scan(True)"""


def test_parse_down_nmap_scan():
    xml_output = '<hosts up="0" down="1" total="1"/>'
    file_descriptor, file_path = tempfile.mkstemp(suffix='.tmp')

    open_file = os.fdopen(file_descriptor, 'w')
    open_file.write(xml_output)
    open_file.close()

    captured_output = io.StringIO()
    sys.stdout = captured_output

    with pytest.raises(SystemExit):
        nmap.parse_nmap_scan(file_path)

    sys.stdout = sys.__stdout__
    os.unlink(file_path)
    assert "unreachable" in captured_output.getvalue()
