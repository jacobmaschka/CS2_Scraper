# CS2 Scraper (IP)
## Overview
- Given a teams HLTV.org match page link, this scraper will fetch all of their individual match links within the past 3 months (for now its set to 1 month to make testing easier). Using those match links, it then finds all map links, and then the players stats. 
## Getting Started
You will need to make sure the following are installed
- Node.js - https://nodejs.org/en/download <br>
- Playwright - `pip install pytest-playwright`, and then `playwright install` <br>
- BeautifulSoup - `pip install beautifulsoup4`

## Languages/Technologies
- Python
- BeautifulSoup
- Playwright

## Notes for further development
- Working in headful mode, but not working in headless mode. In headful mode it tests on fingerprint websites as a bot, so I believe headless mode is being blocked by the website.
- To solve this, I need to look into HTTP headers and how to bypass bot protections.
- Once headless mode is functional, I want to make it asynchronous so it runs faster. I will need to look into proxies to avoid being rate limited.
- Add a database to store player stats.
