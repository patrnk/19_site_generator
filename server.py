import json
import os.path

import jinja2
from livereload import Server

ROOT = 'live_website/'
TEMPLATES = 'templates/'


def load_article_info_by_topic(path):
    with open(path) as json_file:
        article_info = json.load(json_file)
    topics = {}
    for topic in article_info['topics']:
        topics[topic['slug']] = {
            'title': topic['title'],
            'articles': []
        }
    for article in article_info['articles']:
        topic_slug = article['topic']
        topics[topic_slug]['articles'].append(
            {
                'title': article['title'],
                'source': article['source'],
            }
        )
    return topics


def dump_html_to_file(html, path):
    with open(path, 'w') as html_file:
        html_file.write(html)


def render_index(environment, topics):
    context = {
        'topics': topics
    }
    rendered_index = environment.get_template('index.html').render(context)
    index_path = os.path.join(ROOT, 'index.html')
    dump_html_to_file(rendered_index, index_path)


def render_articles(environment, topics):
    pass


def make_site():
    topics = load_article_info_by_topic('config.json')
    environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(TEMPLATES)
    )
    render_index(environment, topics)
    render_articles(environment, topics)


if __name__ == '__main__':
    make_site()
    server = Server()
    server.watch(TEMPLATES, make_site)
    server.serve(root=ROOT)
