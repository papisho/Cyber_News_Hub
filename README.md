# Cyber_News_Hub
A place where you can find most of your cyber news in one place. 
<p>The main reason for making this to to practice my python and JS skill and how to work with API's</p>

<h1>Video Walkthrough</h1>
<p>This video will be updated whenever a new feature is added.</p>

Here's a walkthrough of implemented features:

<img src='/public/assets/cyber_anim.gif' title='Video Walkthrough' width='' alt='Video Walkthrough' />

GIF created with 
[ScreenToGif](https://www.screentogif.com/) 

## Prerequisites

* Python 3.11 or higher
* `pip` for installing dependencies

## Installation

Install the python dependencies with:
```bash
pip install -r requirements.txt
```

## Running the app

### Development

Use development mode to enable hot reloading and debug output:

```bash
export FLASK_ENV=development
python app.py
```

### Production

Run without setting `FLASK_ENV` (or set it to any value other than
`development`) to start the server without debug mode:

```bash
python app.py
```

## Available Routes

| Route | Description |
|-------|-------------|
| `/` | Serves the web UI (static files from `public/`). |
| `/api/articles` | Returns a JSON list of news articles. Supports `limit`, `feed`, `start`, `end` and `refresh` query parameters. |

## Using the UI

Open your browser to `http://localhost:5000` after starting the app. Use the dropdowns at the top to choose how many stories to show, select a feed source, and set optional start/end dates. Click **Scrape** to load articles or **Refresh** to shuffle the results while keeping your filters.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.