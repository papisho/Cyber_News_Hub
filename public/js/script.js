
// public/js/script.js

document.addEventListener('DOMContentLoaded', async () => {
    const container = document.getElementById('articles');
  
    try {
      const response = await fetch('/api/articles');
      if (!response.ok) throw new Error('Network response was not ok');
      const articles = await response.json();
  
      articles.forEach(article => {
        const card = document.createElement('div');
        card.className = 'article-card';
  
        const title = document.createElement('h2');
        title.textContent = article.title;
  
        const teaser = document.createElement('p');
        teaser.textContent = article.teaser;
  
        const link = document.createElement('a');
        link.href = article.link;
        link.target = '_blank';
        link.className = 'read-more';
        link.textContent = 'Read more →';
  
        card.append(title, teaser, link);
        container.appendChild(card);
      });
    } catch (err) {
      container.textContent = 'Sorry, unable to load articles right now.';
      console.error(err);
    }
  });
  