import pytest
from click.testing import CliRunner

from excalibur.__version__ import __version__
from excalibur import cli as cli_module


@pytest.fixture
def current_version():
    """Returns the current release's version string."""

    return __version__


@pytest.fixture
def cli_runner():
    """Returns a `CliRunner` instance for testing CLI commands."""

    return CliRunner()


@pytest.fixture
def cli():
    """Returns the main CLI group command instance."""

    return cli_module.cli


@pytest.fixture
def cli_args(request):
    """Provides a way to parametrize `cli_invoke` fixture's arguments."""

    return request.param


@pytest.fixture
def cli_invoke(cli_runner, cli, cli_args):
    """Using a `CliRunner`, invokes the main CLI command group with the `cli_args` as
    arguments, and asserts `exit_code` is 0 before returning the `Result`.

    """

    result = cli_runner.invoke(cli, cli_args)
    assert result.exit_code == 0
    return result


@pytest.fixture(params=[pytest.param([], id="<no-arguments>"), pytest.param(["--help"], id="--help")])
def cli_help(request, cli_runner, cli):
    """Using a `CliRunner`, invokes the main CLI command group without arguments and with
    `--help`, asserting `exit_code` is 0 before returning the `Result`.

    """

    result = cli_runner.invoke(cli, request.param)
    assert result.exit_code == 0
    return result


@pytest.fixture
def prog_name(cli_runner, cli):
    """Returns the program name of the main CLI command group."""

    return cli_runner.get_default_prog_name(cli)


class NoArgsCallable:
    """Helper class to check a callable was called without arguments and track the number of
    invocations."""

    def __init__(self):
        self.num_calls = 0

    def __call__(self, *args, **kwargs):
        assert args == ()
        assert kwargs == {}
        self.num_calls += 1


@pytest.fixture
def with_fake_called_once(request, monkeypatch):
    fake = NoArgsCallable()
    with monkeypatch.context() as m:
        patched_callable = request.function.__name__.partition("_with_fake_")[-1]

        m.setattr(cli_module, patched_callable, fake)
        assert getattr(cli_module, patched_callable) is fake

        yield fake

        assert fake.num_calls == 1
