# -*- coding: utf-8 -*-

"""Console script for crawler."""
import sys
import json

import click

from crawler.crawler import Crawler


@click.command()
@click.argument('base_url')
@click.option('-c', '--config', help='JSON config file')
@click.option('-o', '--output', help='Data output file')
def main(base_url, config, output):
    click.echo(click.style('[+] Getting data from %s' % base_url, fg='white', bold=True))

    with open(config, 'r') as f:
        json_data = f.read()

    c = Crawler(base_url, json_data=json_data)
    data = json.dumps(c.find_from_json(), indent=4)

    with open(output, 'w') as f:
        f.write(data)

    click.echo(click.style('[+] Finished!', fg='white', bold=True))



if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
