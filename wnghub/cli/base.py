import click
from wnghub.config.config import Config
from wnghub.client.github import GithubApiClient
from wnghub.controller.config import ConfigController
from wnghub.controller.github import GithubController
from wnghub.controller.view import NotificationViewController


@click.group(invoke_without_command=True)
@click.option("-A/--only-unread", default=False)
@click.pass_context
def cli(ctx, a):
    ctx.obj = Config.read()
    if ctx.invoked_subcommand is None:
        config = ctx.obj
        auth_token = config.auth_token
        client = GithubApiClient(auth_token)
        controller = GithubController(client, config)
        results = controller.get_notifications(all=a)
        view_controller = NotificationViewController(config)
        view_controller.display(results)


@click.command("set-auth", help="Sets auth token for Github.")
@click.argument("auth_token", nargs=1)
@click.pass_context
def auth(ctx, auth_token):
    controller = ConfigController(ctx.obj)
    controller.set_auth(auth_token)


@click.command(
    "get-config",
    help="Gets value from config. Possible values: {}".format(
        ConfigController._valid_config_fields
    ),
)
@click.argument("field_name", nargs=1)
@click.pass_context
def get_config(ctx, field_name):
    controller = ConfigController(ctx.obj)
    value = controller.get(field_name)
    click.echo(value)


@click.command("set-config", help="Sets value in config file")
@click.argument("field_name", nargs=1)
@click.argument("value", nargs=1)
@click.pass_context
def set_config(ctx, field_name, value):
    controller = ConfigController(ctx.obj)
    controller.set(field_name, value)


@click.command("reset-config", help="Sets value in config file")
@click.argument("field_name", nargs=1)
@click.pass_context
def reset_config(ctx, field_name):
    controller = ConfigController(ctx.obj)
    controller.reset(field_name)


cli.add_command(auth)
cli.add_command(get_config)
cli.add_command(set_config)
cli.add_command(reset_config)

if __name__ == "__main__":
    cli()
