{%- if cookiecutter.command_line_interface|lower == 'click' %}from click.testing import CliRunner

from {{ cookiecutter.project_slug }} import cli
{%- endif %}


def test_version():
    from {{cookiecutter.project_slug}} import __version__

    assert __version__ == '{{ cookiecutter.version }}'
{%- if cookiecutter.command_line_interface|lower == 'click' %}


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert '{{ cookiecutter.project_slug }}.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
{%- endif %}
