import json
import os

import markdown
import jinja2
from livereload import Server

ROOT = 'live_website/'
TEMPLATES = 'templates/'
SOURCES_ROOT = 'articles/'


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


def read_text_from_file(path):
    with open(path) as text_file:
        return text_file.read()


def dump_html_to_file(html, path):
    with open(path, 'w') as html_file:
        html_file.write(html)


def generate_article_filename(article_source):
    source_filename = os.path.basename(article_source)
    article_slug = os.path.splitext(source_filename)[0]
    return '.'.join((article_slug, 'html'))


def render_index(environment, topics):
    context = {
        'topics': topics
    }
    rendered_index = environment.get_template('index.html').render(context)
    index_path = os.path.join(ROOT, 'index.html')
    dump_html_to_file(rendered_index, index_path)


def render_articles(environment, topics):
    for slug, topic in topics.items():
        topic_path = os.path.join(ROOT, slug)
        os.makedirs(topic_path, exist_ok=True)
        for article in topic['articles']:
            md_article = read_text_from_file(os.path.join(SOURCES_ROOT, article['source']))
            html_article = markdown.markdown(md_article)
            context = {
                'title': article['title'],
                'text': html_article,
                'topic': topic['title'],
            }
            rendered_article = environment.get_template('article.html').render(context)
            article_name = generate_article_filename(article['source'])
            article_path = os.path.join(topic_path, article_name)
            dump_html_to_file(rendered_article, article_path)


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
