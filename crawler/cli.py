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
@click.option('-r', '--raw', is_flag=True, default=True, help='Output raw data')
def main(base_url, config, output, raw):
    click.echo(click.style('\n[+] Getting data from %s\n' % base_url, fg='white', bold=True))

    with open(config, 'r') as f:
        json_data = f.read()

    c = Crawler(base_url, json_data=json_data, format_out=raw)
    data = json.dumps(c.find_from_json(), indent=4)

    with open(output, 'w') as f:
        f.write(data)

    click.echo(click.style('\n[+] Finished!\n\n', fg='white', bold=True))



if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
