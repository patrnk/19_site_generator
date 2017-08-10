import os
import sys
from argparse import ArgumentParser, RawTextHelpFormatter

import markdown
import jinja2
from livereload import Server

import file_utils

TEMPLATES = 'templates/'
ASSETS = 'assets/'
ARTICLE_SOURCES = 'articles/'
ARTICLE_INFO = 'config.json'
ROOT = 'live_website/'
ARTICLES_SUBDIRECTORY = 'encyclopedia/'


def render_index(environment, topics):
    context = {
        'topics': topics
    }
    rendered_index = environment.get_template('index.html').render(context)
    index_path = os.path.join(ROOT, 'index.html')
    file_utils.dump_html_to_file(rendered_index, index_path)


def render_articles(environment, topics):
    for slug, topic in topics.items():
        topic_path = os.path.join(ROOT, ARTICLES_SUBDIRECTORY, slug)
        os.makedirs(topic_path, exist_ok=True)
        for article in topic['articles']:
            md_article = file_utils.read_text_from_file(
                os.path.join(ARTICLE_SOURCES, article['source'])
            )
            html_article = markdown.markdown(md_article)
            context = {
                'title': article['title'],
                'text': html_article,
                'topic': topic['title'],
            }
            rendered_article = environment.get_template('article.html').render(context)
            article_name = file_utils.generate_article_filename(article['source'])
            article_path = os.path.join(topic_path, article_name)
            file_utils.dump_html_to_file(rendered_article, article_path)


def collect_assets():
    file_utils.force_copy_folder(ASSETS, os.path.join(ROOT, ASSETS))

def make_site():
    topics = file_utils.load_article_info_by_topic(ARTICLE_INFO)
    environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(TEMPLATES)
    )
    render_index(environment, topics)
    render_articles(environment, topics)


def parse_args(argv):
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        'action',
        choices=('runserver', 'reset'),
        help='runserver -- start livereload server\n'
             'reset -- remove all generated files and generate them again'
    )
    return parser.parse_args(argv)


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    if args.action == 'reset':
        file_utils.delete_contents_of_folder(ROOT)
        collect_assets()
        make_site()
    if args.action == 'runserver':
        server = Server()
        server.watch(TEMPLATES, make_site)
        server.watch(ASSETS, collect_assets)
        server.serve(root=ROOT)
