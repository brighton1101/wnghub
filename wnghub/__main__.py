#!/usr/bin/env python

from wnghub.cli.base import cli


def main():
    """
    This method is the entrypoint for the `wnghub` console script.
    """
    cli()


if __name__ == "__main__":
    """
    This should be here in case users do `python3 -m wnghub`
    Not sure who would do that, but...
    """
    main()
