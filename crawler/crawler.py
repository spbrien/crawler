# -*- coding: utf-8 -*-

import os
import json
import re

from requests_html import HTMLSession

from crawler.async_links import get_all_links


"""Main module."""

class Crawler():
    session = None
    html = None
    json_data = None
    links = None

    def __init__(self, base_url, json_data=None, refresh=False):
        self.session = HTMLSession()
        self.json_data = self._parse(json_data) if json_data else None
        self.links = self._get_links(base_url, refresh=refresh)


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
        r.html.render()
        return r.html

    def find_from_json(self, json_data=None):
        def text_content_for_key(value):
            if not isinstance(value, dict):
                return [
                    {
                        "text": i.text,
                        "html": i.html
                    } for i in html.find(value)
                ]
            else:
                pass

        data = self.json_data if self.json_data else self._parse(json_data)
        out = {}

        for k, v in data.items():
            # Match all elements from self.links with regex in k
            reg = re.compile('%s' % k)
            key_list = [i for i in filter(reg.match, self.links)]

            if len(key_list) > 0:
                for item in key_list:
                    try:
                        html = self._get(item)
                        out[item] = {
                            key: text_content_for_key(value)
                            for key, value in v.items()
                        }
                    except:
                        pass
        return out
