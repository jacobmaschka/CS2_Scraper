from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re

def main():
    allPlayerStats = {}
    teamMatchPage = 'https://www.hltv.org/team/7020/spirit#tab-matchesBox'
    matchLinks = getMatchLinks(teamMatchPage)

    for link in matchLinks:
        mapLinks = getMapLinks(link)
        for link in mapLinks:
            playerStats = getPlayerStats(link)
            # Update the allPlayerStats dictionary with the playerStats from the current map
            for player, stats in playerStats.items():
                if player in allPlayerStats:
                    allPlayerStats[player].extend(stats)
                else:
                    allPlayerStats[player] = stats
    
    # Now print all players stats
    for player, stats in allPlayerStats.items():
        print(f"{player}: {stats}")      
            

def getPlayerStats(mapPage):
    with sync_playwright() as p:
        # Launch playwright in chrome, open a new page, and go to the passed in link
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        #stealth_sync(page)
        page.set_viewport_size({"width": 1920, "height": 1080})
        page.goto(mapPage)

        # Wait to make sure its loaded, then click to accept the cookies.
        try:
            page.wait_for_selector('#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll', timeout=5000)
            page.click('#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')
        # If the cookie dialog box isnt loaded within 5 seconds, keep going
        except TimeoutError:
            pass
        
        page.wait_for_selector('body > div.bgPadding > div.widthControl > div:nth-child(2) > div.contentCol > div.stats-section.stats-match')
        statHTML = page.inner_html('body > div.bgPadding > div.widthControl > div:nth-child(2) > div.contentCol > div.stats-section.stats-match')

        soup = BeautifulSoup(statHTML, 'html.parser')
        
        # Find all divs with class 'stats-content'
        stats_content_divs = soup.find_all('div', class_='stats-content')

        playerStats = {}

        # Need to pull this earlier and pass it into this function, used in the next loop
        hardcodedTeam = 'Spirit'

        # Iterate over the divs and extract player stats
        for stats_content in stats_content_divs:

            # Define a lambda function to check if the table has the class 'hidden'
            filterCondition = lambda table: 'hidden' not in table.get('class', [])
            # Find all tables within a stats-content div
            allTables = stats_content.find_all('table')
            # Use filter to select only the tables that meet the filter condition
            tables = filter(filterCondition, allTables)


            for table in tables:
                # Check if the table header contains the hardcoded team name
                header = table.find('th')
                if header and header.text.strip() == hardcodedTeam:
                    # Extract data from the table
                    rows = table.find_all('tr')
                    for row in rows[1:]:  # Skip the header row
                        columns = row.find_all('td')
                        # Assuming the columns are in a specific order, you can extract data like this
                        name = columns[0].get_text().strip()
                        killCol = columns[1].get_text().strip()
                        kills = int(re.findall(r'\d+', killCol)[0])
                        if name in playerStats:
                            playerStats[name].append(kills)
                        else:
                            playerStats[name] = [kills]

        browser.close()
        return playerStats


def getMapLinks(matchPage):
    with sync_playwright() as p:
        # Launch playwright in chrome, open a new page, and go to the passed in link
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        #stealth_sync(page)
        page.set_viewport_size({"width": 1920, "height": 1080})
        page.goto(matchPage)

        # Wait to make sure its loaded, then click to accept the cookies.
        try:
            page.wait_for_selector('#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll', timeout=5000)
            page.click('#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')
        # If the cookie dialog box isnt loaded within 5 seconds, keep going
        except TimeoutError:
            pass

        page.wait_for_selector('body > div.bgPadding > div.widthControl > div:nth-child(2) > div.contentCol > div.match-page > div.g-grid.maps > div.col-6.col-7-small > div.flexbox-column')
        resultsHTML = page.inner_html('body > div.bgPadding > div.widthControl > div:nth-child(2) > div.contentCol > div.match-page > div.g-grid.maps > div.col-6.col-7-small > div.flexbox-column')

        soup = BeautifulSoup(resultsHTML, 'html.parser')
        mapholders = soup.find_all('div', class_='mapholder')

        mapLinks = []

        # Iterate over each mapholder
        for mapholder in mapholders:
            # Find the results-center-stats div inside each mapholder
            results_center_stats = mapholder.find("div", class_="results-center-stats")
            if results_center_stats:
                # Find the a tag inside results-center-stats and print its href attribute
                a_tag = results_center_stats.find("a")
                if a_tag:
                    mapLinks.append('https://www.hltv.org' + a_tag["href"])
        
        browser.close()
        return mapLinks


def getMatchLinks(teamMatchPage):
    with sync_playwright() as p:
        # Launch playwright in chrome, open a new page, and go to the passed in link
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()
        #stealth_sync(page)
        page.set_viewport_size({"width": 1920, "height": 1080})
        page.goto(teamMatchPage)
        
        # Wait to make sure its loaded, then click to accept the cookies.
        try:
            page.wait_for_selector('#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll', timeout=5000)
            page.click('#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')
        # If the cookie dialog box isnt loaded within 5 seconds, keep going
        except TimeoutError:
            pass

        # Wait to make sure its loaded, then click to show all matches
        page.wait_for_selector('#matchesBox > a')
        page.click('#matchesBox > a')

        # Wait to make sure its loaded, then click to filter for last 3 months
        # page.wait_for_selector('body > div.bgPadding > div.widthControl > div:nth-child(2) > div.leftCol > div > div > div > div.sidebar-first-level > div > div > div:nth-child(4) > div > a:nth-child(3)')
        # page.click('body > div.bgPadding > div.widthControl > div:nth-child(2) > div.leftCol > div > div > div > div.sidebar-first-level > div > div > div:nth-child(4) > div > a:nth-child(3)')
        
        # Use last month for now to make testing easier
        page.wait_for_selector('body > div.bgPadding > div.widthControl > div:nth-child(2) > div.leftCol > div.results > div > div > div.sidebar-first-level > div > div > div:nth-child(4) > div > a:nth-child(2)')
        page.click('body > div.bgPadding > div.widthControl > div:nth-child(2) > div.leftCol > div.results > div > div > div.sidebar-first-level > div > div > div:nth-child(4) > div > a:nth-child(2)')
        
        # Wait to make sure its loaded, then get the HTML content for the results-all div
        page.wait_for_selector('body > div.bgPadding > div.widthControl > div:nth-child(2) > div.contentCol > div.results > div.results-holder.allres > div.results-all')
        resultsHtml = page.inner_html('body > div.bgPadding > div.widthControl > div:nth-child(2) > div.contentCol > div.results > div.results-holder.allres > div.results-all')

        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(resultsHtml, 'html.parser')

        # Initialize a list to store the match links
        matchLinks = []

        # Iterate over every result-con div within the results-all div
        for result in soup.find_all('div', class_='result-con'):
            # Find and store the match link
            link = result.find('a')['href']
            fullLink = 'https://www.hltv.org' + link
            matchLinks.append(fullLink)

        # Close the opened browser
        browser.close()

        return matchLinks
        

if __name__ == "__main__":
    main()