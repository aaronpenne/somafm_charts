somafm_charts
=============

Parses and compiles artist/album/track charts from [`somafm`](http://somafm.com/), the best internet radio around. The end goal is to have a database of all the top artists/albums/tracks played on the various stations.

From the SomaFM website:

> *over 30 unique channels of listener-supported, commercial-free, underground/alternative radio broadcasting to the world. All music hand-picked by SomaFM's award-winning DJs and music directors.*


FIXME
-----
- Basics
    - [x] Pull data from all stations
    - [x] Pull data from all dates (programmatic 7 day delta)
    - [x] Parse chart into columns (csv style)
    - [x] Output CSV
    - [ ] Args for date range, stations (other filtering after data pull)
    - [ ] Start date to 'last Saturday' (relative to today)
- Reporting
    - [ ] Generate metrics (top artist on groovesalad in 2015, top song on xmas ever)
    - [ ] Generate visualization
    - [ ] Generate year-end ranking charts, etc.
- Databasing
    - [ ] Create database architecture
    - [ ] Save data in database