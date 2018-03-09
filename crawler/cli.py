# -*- coding: utf-8 -*-

"""Console script for crawler."""
import sys
import os
import json

import click
from slugify import slugify

from crawler.crawler import Crawler


@click.command()
@click.argument('base_url')
@click.option('-c', '--config', help='JSON config file')
@click.option('-o', '--output', help='Data output file')
@click.option('-s', '--scripts', is_flag=True, default=False, help='Render javascript')
@click.option('-r', '--raw', is_flag=True, default=True, help='Output raw data')
@click.option('-x', '--clear', is_flag=True, default=False, help='Clears url cache')
@click.option('--splitting', is_flag=True, default=False, help='Splits results into separate files')
def main(
    base_url,
    config,
    output,
    scripts,
    raw,
    clear,
    splitting,
):
    click.echo(click.style('\n[+] Getting data from %s\n' % base_url, fg='white', bold=True))

    with open(config, 'r') as f:
        json_data = f.read()

    c = Crawler(
        base_url,
        refresh=clear,
        render=scripts,
        json_data=json_data,
        format_out=raw
    )

    data_dir = os.path.join(os.getcwd(), '%s-data' % slugify(base_url))
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    if output:
        outfile = os.path.join(data_dir, output)
    else:
        outfile = os.path.join(data_dir, 'data.json')

    if not splitting:
        data = json.dumps(c.find_from_json(), indent=4)
        with open(outfile, 'w') as f:
            f.write(data)
    else:
        data = c.find_from_json()
        for k, v in data.items():
            with open(os.path.join(data_dir, "%s.json" % slugify(k)), 'w') as f:
                f.write(json.dumps(v, indent=4))

    click.echo(click.style('\n[+] Finished!\n\n', fg='white', bold=True))



if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
