#!/usr/bin/env python

"""Tests for `cli` package."""

import os

from click.testing import CliRunner

from questions import cli


def test_command_list_resources():
    runner = CliRunner()
    result = runner.invoke(cli.list_resources, ["jquery", "default"])
    assert result.exit_code == 0
    assert "Required Javascript resources" in result.output
    assert "Required CSS resources" in result.output


def test_command_list_resources_include_widgets():
    runner = CliRunner()
    result = runner.invoke(
        cli.list_resources, ["jquery", "default", "--include-widgets"]
    )
    assert result.exit_code == 0
    assert "Required Javascript resources" in result.output
    assert "Required CSS resources" in result.output
    assert "Widget specific Javascript resources" in result.output
    assert "Widget specific CSS resources" in result.output


def test_command_download_surveyjs():
    runner = CliRunner()
    with runner.isolated_filesystem():
        os.mkdir("_tmp_")
        result = runner.invoke(cli.download_surveyjs, ["_tmp_", "jquery", "default"])
        assert result.exit_code == 0
        assert "Downloaded " in result.output
