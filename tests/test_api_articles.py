
import datetime
import types

import pytest

import app

@pytest.fixture

def client(monkeypatch):
    # Prepare fake feed entries for each feed
    base_date = datetime.datetime(2022, 1, 1, 12, 0, 0)
    entries_map = {}
    for idx, url in enumerate(app.FEEDS):
        entries = []
        for day in range(3):
            dt = base_date + datetime.timedelta(days=day)
            entries.append({
                'title': f'title-{idx}-{day}',
                'link': f'https://example.com/{idx}/{day}',
                'summary': 'summary text',
                'published': dt.isoformat(),
                'published_parsed': dt.timetuple(),
            })
        entries_map[url] = types.SimpleNamespace(entries=entries)

    call_count = {'count': 0}

    def fake_parse(url):
        call_count['count'] += 1
        return entries_map[url]

    monkeypatch.setattr(app.feedparser, 'parse', fake_parse)
    app.cache.clear()
    app.app.config['TESTING'] = True
    with app.app.test_client() as client:
        yield client, call_count


def test_cache_usage(client):
    client, call_count = client

    # First request populates the cache
    resp = client.get('/api/articles')
    assert resp.status_code == 200
    first_count = call_count['count']
    assert first_count == len(app.FEEDS)

    # Second request should hit cache and not call feedparser.parse again
    resp = client.get('/api/articles')
    assert resp.status_code == 200
    assert call_count['count'] == first_count


def test_feed_filter(client):
    client, call_count = client
    feed_url = app.FEEDS[0]

    resp = client.get('/api/articles', query_string={'feed': feed_url})
    assert resp.status_code == 200
    data = resp.get_json()

    # Expect only entries from the specified feed (3 fake entries)
    assert len(data) == 3


def test_date_filters(client):
    client, _ = client

    # Only entries on 2022-01-02
    resp = client.get('/api/articles', query_string={'start': '2022-01-02', 'end': '2022-01-02'})
    assert resp.status_code == 200
    data = resp.get_json()

    # 4 feeds * 1 entry each on that date
    assert len(data) == len(app.FEEDS)