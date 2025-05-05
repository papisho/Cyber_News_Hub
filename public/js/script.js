

// public/js/script.js

document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('articles');
  const numStories = document.getElementById('num-stories');
  const feedFilter = document.getElementById('feed-filter');
  const startDate = document.getElementById('start-date');
  const endDate = document.getElementById('end-date');
  const scrapeBtn = document.getElementById('scrape-btn');
  const refreshBtn = document.getElementById('refresh-btn');
  const dropLinks = document.querySelectorAll('.dropdown-content a');
  const dropBtn = document.querySelector('.dropbtn');

  // Clear out existing articles
  function clearArticles() {
    container.innerHTML = '';
  }

  // Fetch & render articles based on filter controls
  async function loadArticles() {
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
        card.innerHTML = `
          <h2>${a.title}</h2>
          <p>${a.teaser}</p>
          <a href="${a.link}" target="_blank" class="read-more">Read more →</a>
        `;
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

  // “Refresh” button: reset filters, then fetch defaults
  refreshBtn.addEventListener('click', () => {
    numStories.value = '10';
    feedFilter.value = 'all';
    dropBtn.textContent = 'Categories ▾';
    startDate.value = '';
    endDate.value = '';
    loadArticles();
  });

  // Initial load
  loadArticles();
});
