
from flask import Flask, jsonify, request
import feedparser
import datetime
import random
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
    return app.send_static_file('index.html')

@app.route('/api/articles')
def articles():
    # 1) Read query params
    limit      = request.args.get('limit',  default=20,  type=int)
    feed_param = request.args.get('feed')            # specific feed URL
    start      = request.args.get('start')           # YYYY-MM-DD
    end        = request.args.get('end')             # YYYY-MM-DD
    refresh    = request.args.get('refresh') == '1'  # True if wanting a “fresh” set

    # 2) Decide if we should use the cached “default” list
    use_cache = (
        limit == 20 and 
        not feed_param and 
        not start and 
        not end and 
        not refresh )
    
    if use_cache and 'articles' in cache:
        return jsonify(cache['articles'])

    # 3) Fetch & parse all feeds
    all_entries = []
    for url in FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            pub_dt = None
            if getattr(entry, 'published_parsed', None):
                pub_dt = datetime.datetime(*entry.published_parsed[:6])
                pub_date_str = entry.published
            else:
                pub_date_str = ''
            teaser = entry.get('summary', '')[:197].rsplit(' ',1)[0] + '…'
            all_entries.append({
                'title':   entry.title,
                'link':    entry.link,
                'pubDate': pub_date_str,
                'teaser':  teaser,
                'pub_dt':  pub_dt
            })

    # 4) Feed filter
    if feed_param:
        all_entries = [e for e in all_entries if e.get('feed') == feed_param]

    # 5) Date‐range filters
    if start:
        start_dt = datetime.datetime.fromisoformat(start)
        all_entries = [e for e in all_entries if e['pub_dt'] and e['pub_dt'] >= start_dt]
    if end:
        end_dt = datetime.datetime.fromisoformat(end) + datetime.timedelta(days=1)
        all_entries = [e for e in all_entries if e['pub_dt'] and e['pub_dt'] < end_dt]

    # 6) Either shuffle for “refresh” or sort newest first
    if refresh:
        random.shuffle(all_entries)
    else:
        all_entries.sort(key=lambda e: e['pub_dt'] or datetime.datetime.min, reverse=True)

    # 7) Take the requested number
    top_entries = all_entries[:limit]

    # 8) Cache the default set
    if use_cache:
        cache['articles'] = top_entries

    # 9) Strip internal fields
    for e in top_entries:
        e.pop('pub_dt', None)
        e.pop('feed',   None)

    return jsonify(top_entries)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
