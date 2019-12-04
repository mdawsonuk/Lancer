# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""


from core import config, ArgHandler

import os
import pytest
import logging


@pytest.mark.core
def test_get_config_parser():
    cfg = config.get_config_parser()
    assert cfg is not None
    assert cfg['Main']['ShowHeader'] is 'yes'


@pytest.mark.core
def test_get_config_path():
    path = config.get_config_path()
    assert os.path.exists(os.path.dirname(path))
    from getpass import getuser
    assert getuser() in path


@pytest.mark.core
def test_save_config():
    config.save_config()
    assert os.path.exists(config.get_config_path())


@pytest.mark.core
def test_load_config():
    config.load_config()
    assert config.config is not None


@pytest.mark.core
def test_load_config_not_on_disk():
    os.remove(config.get_config_path())
    config.load_config()
    assert config.config is not None
    assert os.path.exists(config.get_config_path())


@pytest.mark.core
def test_get_module_value():
    config.config["nmap"] = {}
    config.config["nmap"]["enabled"] = "yes"

    assert config.get_module_value("nmap", "enabled")


@pytest.mark.core
def test_get_module_value_doesnt_exist():
    assert config.get_module_value("FakeModule", "FakeKey", "fakevalue") == "fakevalue"


@pytest.mark.core
def test_get_current_target_cache():
    path = config.get_current_target_cache("127.0.0.1")
    assert config.folder_name in path
    assert "127.0.0.1" in path


@pytest.mark.core
def test_get_module_cache():
    path = config.get_module_cache("Test", "127.0.0.1", "22")
    assert "Test" in path
    assert "22" in path


@pytest.mark.core
def test_get_module_cache_no_port():
    path = config.get_module_cache("Test", "127.0.0.1")
    assert "Test" in path
    assert path.endswith("Test")


@pytest.mark.core
def test_get_logger_very_verbose():
    ArgHandler.parse_arguments(["-T", "::1", "-vv"])
    logger = config.get_logger("TestVeryVerbose")
    assert logger.handlers[0].level is logging.DEBUG
