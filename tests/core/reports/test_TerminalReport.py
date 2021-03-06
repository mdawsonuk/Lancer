# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from core.reports.TerminalReport import TerminalReport

import pytest
import io
import sys


@pytest.mark.core
def test_create_instance():
    report = TerminalReport()
    assert report is not None


@pytest.mark.core
def test_generate_report():
    report = TerminalReport()

    ftp_service = {"options": ["GET", "POST", "OPTIONS"], "FTP Banner": "FileZilla Server 0.9.60 beta\nwritten by"
                                                                        " Tim Kosse (tim.kosse@filezilla-project.org)"
                                                                        "\nPlease visit https://filezilla-project.org/"}

    hostname = {"Hostname": "TEST-HOSTNAME", "Aliases": []}

    sub_dict = {"Subsubdict": {}, "Lots of depth": {"More depth": "Ok, that's enough"}, "Empty Str": "", "Non-Str": 0,
                "ListOfDicts": [{"Key1": "Value1"}, {"Key2": "Value2"}]}

    geo_service = {"host": "example.com", "ip": "127.0.0.1", "SubDict": sub_dict}

    gobuster = []
    result = {"Path": "http://127.0.0.1/index.html", "Code": "200", "Code Value": "OK"}
    gobuster.append(result)
    empty_list = []
    result = {}
    empty_list.append(result)
    ports = {"21": ftp_service, "80": {"Gobuster": gobuster, "Empty": empty_list}, "geo": geo_service,
             "hostname": hostname}

    root = {"example.com": ports}

    captured_output = io.StringIO()
    sys.stdout = captured_output
    report.generate_report(root)
    sys.stdout = sys.__stdout__

    out = captured_output.getvalue()

    assert "Target: example.com" in out
    assert "Port: 21" in out
    assert " geo" in out
    assert " options:" in out
    assert "- GET" in out
    assert "host: example.com" in out
    assert "ip: 127.0.0.1" in out
    assert "http://127.0.0.1/index.html" in out
