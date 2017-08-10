# Encyclopedia generator

Generates a website taking markdown source texts and generating html pages for them linked by an index.

Here's an [example](https://patrnk.github.io/devman_encyclopedia_copycat/index.html) of generated website.

# Installation
Requires Python 3.
```
pip install -r requirements.txt
python manage.py reset
python manage.py runserver
```

# Usage
Be sure to run `python manage.py reset` every time one of the `.py` files changes.

The generated website will be placed in the `live_website` folder.

After `python manage.py runserver` command, the index is available at `http://127.0.0.1:5500/index.html`.

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
