import json
import os
import shutil

from slugify import slugify


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
    article_name = os.path.splitext(source_filename)[0]
    article_slug = slugify(article_name)
    return '.'.join((article_slug, 'html'))


def add_info_about_paths(topics, articles_folder):
    for slug, topic in topics.items():
        topic['path'] = os.path.join(articles_folder, slug)
        for article in topic['articles']:
            article_name = generate_article_filename(article['source'])
            article['path'] = os.path.join(topic['path'], article_name)
    return topics


def delete_contents_of_folder(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


def force_copy_folder(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    shutil.copytree(source, destination)
