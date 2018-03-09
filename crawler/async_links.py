#!/usr/bin/env python

# python 3.5 async web crawler.
# https://github.com/mehmetkose/python3.5-async-crawler

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2016 Mehmet Kose mehmet@linux.com


import aiohttp
import asyncio
import async_timeout
from urllib.parse import urljoin, urldefrag


def get_all_links(root_url):
    crawled_urls, url_hub = [], [root_url, "%s/sitemap.xml" % (root_url), "%s/robots.txt" % (root_url)]
    headers = {'user-agent': 'Opera/9.80 (X11; Linux x86_64; U; en) Presto/2.2.15 Version/10.10'}

    async def get_body(url):
        async with aiohttp.ClientSession() as session:
            try:
                with async_timeout.timeout(10):
                    async with session.get(url, headers=headers) as response:
                        if response.status == 200:
                            html = await response.text()
                            return {'error': '', 'html': html}
                        else:
                            return {'error': response.status, 'html': ''}
            except Exception as err:
                return {'error': err, 'html': ''}

    async def handle_task(task_id, work_queue):
        while not work_queue.empty():
            queue_url = await work_queue.get()
            if not queue_url in crawled_urls:
                crawled_urls.append(queue_url)
                body = await get_body(queue_url)
                if not body['error']:
                    for new_url in get_urls(body['html']):
                        if root_url in new_url and not new_url in crawled_urls:
                            work_queue.put_nowait(new_url)
                else:
                    pass

    def remove_fragment(url):
        pure_url, frag = urldefrag(url)
        return pure_url

    def get_urls(html):
        new_urls = [url.split('"')[0] for url in str(html).replace("'",'"').split('href="')[1:]]
        return [urljoin(root_url, remove_fragment(new_url)) for new_url in new_urls]

    q = asyncio.Queue()
    [q.put_nowait(url) for url in url_hub]
    loop = asyncio.get_event_loop()
    tasks = [handle_task(task_id, q) for task_id in range(3)]
    loop.run_until_complete(asyncio.wait(tasks))
    return crawled_urls
