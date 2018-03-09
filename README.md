# Crawler

Crawls a site and saves text into structured JSON based on a provided config file. This utility is meant for relatively small websites: the first step in the process is to recursively crawl all public pages of a site and build a list of available pages... so you _wouldn't want to use it on Wikipedia_.

## Dependencies

* Python 3
* Pip

## Installation

You should use virtualenv:

```bash
# install virtualenv
pip install virtualenv

# create an environment
virtualenv -p python3 venv
source venv/bin/activate

# install crawler
pip install git+git://github.com/spbrien/crawler.git#egg=crawler
```

## Config

#### Simple

Create a JSON config file called `config.json`:

```JSON
{
    "^http://www.example.com/$": {
        "title": "body > div > h1",
        "text": "body > div > p:nth-child(2)"
    }
}
```

The top-level keys are regular expressions. The tool will pull a list of all pages available on the website, then crawl pages that match these regular expressions. For each expression, the crawler will extract text from the DOM according to the selectors in the provided schema.

Run the tool:

```bash
crawler http://example.com -c config.json -o data.json
```

The output from the above config should be:

```JSON
{
    "http://www.example.com/": {
        "title": "Example Domain",
        "text": "This domain is established to be used for illustrative examples in documents. You may use this domain in examples without prior coordination or asking for permission."
    }
}

```

#### Complex

You can have more complex configs, with nested data:

```JSON
{
    "^http://www.some-website.com/$": {
        "container": {
            "selector": "body > div",
            "children": {
                "child-title": "h1",
                "child-subtitle": "h3",
                "child-text": "p"
            }
        },
    }
}
```

Or you can extract data from multiple pages that use the same template/markup:

```JSON
{
    "^http://www.some-website.com/blog/page/\\d+$": {
        "container": {
            "selector": "body > div",
            "children": {
                "child-title": "h1",
                "child-subtitle": "h3",
                "child-text": "p"
            }
        },
    }
}
```

**Don't forget to escape your regex for JSON**
