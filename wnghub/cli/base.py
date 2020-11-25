import click
from wnghub.config import Config


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    ctx.config = Config.read()
    if ctx.invoked_subcommand is None:
        print('no sub')
    

@click.command('set-auth')
@click.option('-T', '--token', default=False, show_default=True, is_flag=True)
@click.argument('username', nargs=1)
@click.argument('password', nargs=1, required=False)
@click.pass_context
def auth(ctx, token, username, password):
    if token:
        if password is not None:
            raise click.ClickException(
                'Too many args passed for setting access token. '
                'Only pass one arg for access token.'
            )
        ctx.config.set_auth(auth_token=username)
    else:
        if password is None:
            raise click.ClickException(
                'Must pass password with username.'
            )
        ctx.config.set_auth(username=username, password=password)

cli.add_command(auth)

if __name__ == "__main__":
    cli()
