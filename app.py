
# app.py
from flask import Flask, jsonify
import feedparser
from cachetools import TTLCache

# Serve files out of your `public/` directory:
app = Flask(__name__, static_folder='public', static_url_path='')

# Simple in-memory cache (5 min TTL)
cache = TTLCache(maxsize=1, ttl=300)

# RSS feeds to pull from
FEEDS = [
    'https://feeds.feedburner.com/TheHackersNews',
    'https://krebsonsecurity.com/feed/',
    'https://www.wired.com/feed/category/security/latest/rss',
    'https://techcrunch.com/tag/security/feed/'
]

@app.route('/')
def index():
    # serves public/index.html
    return app.send_static_file('index.html')

@app.route('/api/articles')
def articles():
    # return cached if fresh
    if 'articles' in cache:
        return jsonify(cache['articles'])

    all_entries = []
    for url in FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            teaser = entry.get('summary', '')[:197].rsplit(' ',1)[0] + '…'
            all_entries.append({
                'title': entry.title,
                'link': entry.link,
                'pubDate': entry.get('published', ''),
                'teaser': teaser
            })
    # newest first, top 20
    all_entries.sort(key=lambda e: e['pubDate'], reverse=True)
    top20 = all_entries[:20]
    cache['articles'] = top20
    return jsonify(top20)

if __name__ == '__main__':
    # match your front-end fetch on port 3000
    app.run(port=5000, debug=True)
