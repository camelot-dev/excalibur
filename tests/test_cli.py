import pytest


def test_prog_name(cli_runner, cli, prog_name):
    assert cli_runner.get_default_prog_name(cli) == prog_name


@pytest.mark.xfail(reason="camelot overrides HelpFormatter.write_usage()")
def test_help_output(cli_help, prog_name):
    assert cli_help.output.startswith("Usage: %(prog_name)s [OPTIONS] COMMAND" % locals())

    options = "\n  ".join([
        "Options:",
        "--version  Show the version and exit.",
        "--help     Show this message and exit.",
    ])
    assert options in cli_help.output

    commands = "\n  ".join([
        "Commands:",
        "initdb", "resetdb", "run", "webserver", "worker",
    ])
    assert commands in cli_help.output


def test_version(cli_runner, cli, prog_name, current_version):
    result = cli_runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert result.output == "%(prog_name)s, version %(current_version)s\n" % locals()


def test_initdb_with_fake_initialize_database(cli_runner, cli, with_fake_called_once):
    result = cli_runner.invoke(cli, ["initdb"])
    assert not result.exception
    assert result.output == ""
    assert result.exit_code == 0
