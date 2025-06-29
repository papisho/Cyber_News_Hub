

// public/js/script.js

document.addEventListener('DOMContentLoaded', () => {
  const container    = document.getElementById('articles');
  const numStories   = document.getElementById('num-stories');
  const feedFilter   = document.getElementById('feed-filter');
  const startDate    = document.getElementById('start-date');
  const endDate      = document.getElementById('end-date');
  const scrapeBtn    = document.getElementById('scrape-btn');
  const refreshBtn   = document.getElementById('refresh-btn');
  const dropLinks    = document.querySelectorAll('.dropdown-content a');
  const dropBtn      = document.querySelector('.dropbtn');

  // Clear out existing articles
  function clearArticles() {
    container.innerHTML = '';
  }

  // Fetch & render articles based on filter controls (I updated this part)
  async function loadArticles(forceRefresh = false) {
    const params = new URLSearchParams();
    params.append('limit', numStories.value);
    if (feedFilter.value && feedFilter.value !== 'all') {
      params.append('feed', feedFilter.value);
    }
    if (startDate.value) {
      params.append('start', startDate.value);
    }
    if (endDate.value) {
      params.append('end', endDate.value);
    }
    if (forceRefresh) {
      params.append('refresh', '1');
    }

    clearArticles();

    try {
      const res = await fetch(`/api/articles?${params.toString()}`);
      if (!res.ok) throw new Error('Network response was not ok');
      const articles = await res.json();

      if (articles.length === 0) {
        container.textContent = 'No articles found for these filters.';
        return;
      }

      articles.forEach(a => {
        const card = document.createElement('div');
        card.className = 'article-card';
        
        const title = document.createElement('h2');
        title.textContent = a.title;

        const teaser = document.createElement('p');
        teaser.textContent = a.teaser;

        const link = document.createElement('a');
        link.href = a.link;
        link.target = '_blank';
        link.className = 'read-more';
        link.textContent = 'Read more →';

        card.appendChild(title);
        card.appendChild(teaser);
        card.appendChild(link);
        container.appendChild(card);
      });

    } catch (err) {
      container.textContent = 'Sorry, unable to load articles right now.';
      console.error(err);
    }
  }

  // When user picks a category from the dropdown...
  dropLinks.forEach(link => {
    link.addEventListener('click', e => {
      e.preventDefault();
      const feed = link.dataset.feed;
      feedFilter.value = feed;
      dropBtn.textContent = `${link.textContent} ▾`;
    });
  });

  // “Scrape” button: fetch with current filters
  scrapeBtn.addEventListener('click', () => {
    loadArticles();
  });

 // “Refresh” button: keep filters but force fresh fetch
 refreshBtn.addEventListener('click', () => {
  loadArticles(true);
});

  // Initial load
loadArticles();
});
