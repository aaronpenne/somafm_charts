SomaFM "Top 30" Charts
======================

This simple scraper parses and compiles the "Top 30" charts at [SomaFM](http://somafm.com/).  SomaFM is "listener-supported, commercial-free, underground/alternative radio" based out of San Francisco. Their 30+ uniquely flavored channels are hand curated and cover everything from [downtempo beats](https://somafm.com/player/#/now-playing/groovesalad) to [indie pop rock](https://somafm.com/player/#/now-playing/indiepop) to [metal](https://somafm.com/player/#/now-playing/metal) to [classic soul](https://somafm.com/player/#/now-playing/7soul). 

Background
----------
Every week SomaFM publishes charts for each channel with the 30 most popular artists, albums, and tracks for the previous week. Each channel has a new page for the week's chart. [Here is an example chart page](http://somafm.com/charts/groovesalad/groovesalad-30Dec17.html). This tool scrapes the following charts:
- Top 30 Artists by Spins
- Top 30 Albums by Spins
- Top 30 Tracks by Spins
- Top 30 Artists by Listeners
- Top 30 Albums by Listeners
- Top 30 Tracks by Listeners

Definitions from the SomaFM website: 
> *Charts are listed by spin (the number of times we played the song that week) and by listeners, which is the sum of the number of people listening to a channel each time we played that song or artist.*

get_somafm_charts.py
--------------------
This tool goes through each channel's entire available chart history and *currently* creates a CSV for each channel. The end goal is to push this info to a database.

The chart data is reshaped so each record contains the following fields:
`week`, `rank`, `artist`, `media`, `media_type`, `score_type`, `score`, `station`, `url`

To get the full "Top 30" dataset the code has to run through roughly 10 years of weekly pages for each of the 35 channels. It takes a couple hours on my machine to finish.

Dependencies
------------
- [Python 3](https://www.python.org/)
- [lxml](https://github.com/lxml/lxml)
- [pandas](https://github.com/pandas-dev/pandas)
- [requests](https://github.com/requests/requests)

Developed with Python 3.6 on Windows 10. 

Todo List
---------
- Basics
    - [x] Pull data from all stations
    - [x] Pull data from all dates (programmatic 7 day delta)
    - [x] Parse chart into columns (csv style)
    - [x] Output CSV
    - [ ] Args for date range, stations (other filtering after data pull)
    - [x] Start date to 'last Saturday' (relative to today)
    - [ ] Modularize for CLI usage
- Reporting
    - [ ] Generate metrics (top artist on groovesalad in 2015, top song on xmas ever)
    - [ ] Generate visualization
    - [ ] Generate year-end ranking charts, etc.
- Databasing
    - [ ] Create database architecture
    - [ ] Save data in database
        
License
-------
[MIT License](https://github.com/aaronpenne/somafm_charts/blob/master/LICENSE) © Aaron Penne

Disclaimer: This project is not affiliated with SomaFM in any way.
