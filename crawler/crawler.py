# -*- coding: utf-8 -*-

import os
import json
import re

from click import echo, style
from requests_html import HTMLSession
from requests_html import HTML

from crawler.async_links import get_all_links

"""Main module."""

class Crawler():
    session = None
    html = None
    json_data = None
    links = None

    def __init__(self, base_url, json_data=None, render=False, refresh=False, format_out=True):
        self.session = HTMLSession()
        self.json_data = self._parse(json_data) if json_data else None
        self.links = self._get_links(base_url, refresh=refresh)
        self.format_out = format_out
        self.render = render


    def _get_links(self, base_url, refresh=False):
        cache_file = os.path.join(os.getcwd(), '.link_cache')
        if os.path.isfile(cache_file) and not refresh:
            with open(cache_file, 'r') as f:
                return json.load(f)
        else:
            links = get_all_links(base_url)
            with open(cache_file, 'w') as f:
                f.write(json.dumps(links))
            return links


    def _parse(self, json_data):
        return json.loads(json_data)

    def _get(self, url):
        r = self.session.get(url)
        if self.render:
            r.html.render()
        return r.html

    def find_from_json(self, json_data=None):
        def transform_lists_and_nested(value):
            if isinstance(value, list) and len(value) == 1:
                return value[0]

            if isinstance(value, list) \
                and len(value) > 1 \
                and not isinstance(value, str):
                return [transform_lists_and_nested(i) for i in value]

            if isinstance(value, dict):
                if value.get('children', False):
                    return transform_lists_and_nested(value['children'])

            return value

        def text_content_for_key(html, value):
            if not isinstance(value, dict):
                return [
                    {
                        "text": i.text,
                        "html": i.html
                    } for i in html.find(value)
                ] if not self.format_out else [
                    i.text for i in html.find(value)
                ]
            else:
                children = value['children']
                selector = value['selector']
                return [
                    {
                        "text": i.text,
                        "html": i.html,
                        "children": {
                            key: text_content_for_key(i, value)
                            for key, value in children.items()
                        }
                    } for i in html.find(selector)
                ] if not self.format_out else [
                    {
                        "children": {
                            key: text_content_for_key(i, value)
                            for key, value in children.items()
                        }
                    } for i in html.find(selector)
                ]

        data = self.json_data if self.json_data else self._parse(json_data)
        out = {}

        for k, v in data.items():
            # Match all elements from self.links with regex in k
            reg = re.compile('%s' % k)
            key_list = [i for i in filter(reg.match, self.links)]

            if len(key_list) > 0:
                for item in key_list:
                    try:
                        echo(style("[-] Crawling %s", bold=False) % item)
                        html = self._get(item)
                        out[item] = {
                            key: text_content_for_key(html, value)
                            for key, value in v.items()
                        }
                        if not self.format_out:
                            out[item]['_source'] = html.html
                            out[item]['_meta'] = [i.html for i in html.find('meta')]
                    except:
                        pass
            echo(style("* * *", fg='white', bold=True))
        return {
            k: {
                key: transform_lists_and_nested(value)
                for key, value in v.items()
            } for k, v in out.items()
        } if self.format_out else out
