from lxml import html
import requests
from datetime import date, timedelta
import pandas as pd
import os

output_dir = 'C:\\tmp\\somafm\\'
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

station_url_names = ['bagel',
                     'beatblender',
                     'bootliquor',
                     'brfm',
                     'christmas',
                     'cliqhop',
                     'covers',
                     'deepspaceone',
                     'defcon',
                     'digitalis',
                     'doomed',
                     'dronezone',
                     'dubstep',
                     'earwaves',
                     'fluid',
                     'folkfwd',
                     'groovesalad',
                     'illstreet',
                     'indiepop',
                     'jollysoul',
                     'lush',
                     'metal',
                     'missioncontrol',
                     'poptron',
                     'secretagent',
                     'seventies',
                     'sf1033',
                     'sonicuniverse',
                     'spacestation',
                     'suburbsofgoa',
                     'thetrip',
                     'thistle',
                     'u80s',
                     'xmasinfrisko',
                     'xmasrocks']

# Get list of week start dates in two formats
num_weeks = int(round(52*30))  # (Weeks in years)*(Years)
chart_weeks = {'url': [],
               'csv': []}
#week = date(2017, 12, 30)  # (YYYY, MM, DD) 

# Round today's date to the most recent Saturday (when charts are published)
today = date.today()
today_index = (today.weekday() + 1) % 7
week = today - timedelta(today_index + 1)

for i in range(num_weeks):
    chart_weeks['url'] += [week.strftime('%d%b%y')]  # DDMMMYY (ex. 30Dec17)
    chart_weeks['csv'] += [week.isoformat()]         # YYYY-MM-DD
    week = week - timedelta(days=7)                  # Previous week

# FIXME development code to shorten runs
#station_url_names = ['groovesalad']
#chart_weeks['url'] = chart_weeks['url'][0:3]
#chart_weeks['csv'] = chart_weeks['csv'][0:3]

data = {'week': [],
        'rank': [],
        'artist': [],
        'media': [],
        'media_type': [],
        'score_type': [],
        'score': [],
        'station': [],
        'url': []}

for i, station in enumerate(station_url_names):
    try:
        for j, week in enumerate(chart_weeks['url']):
            print('{} ({:02}/{:02}) | {} ({:04}/{:04})'.format(station, i+1, len(station_url_names), week, j+1, len(chart_weeks['url'])))
            # Parse raw data from website
            page_url = 'http://somafm.com/charts/{}/{}-{}.html'.format(station, station, week)
            page = requests.get(page_url)
            tree = html.fromstring(page.content)
            text = tree.xpath('//div[@id="content"]/pre/text()')
            a = str(text[0])
            b = a.splitlines()
            c = list(filter(None, b))
            for line in c:
                # If end of charts, go to next week
                if 'adds' in line.lower():
                    break
                # If chart header, then split according to whitespace
                if line[0:7] == 'Top 30 ':
                    line_split = line.split()
                    media_type = line_split[2].lower()
                    score_type = line_split[4].lower()
                else:
                    # Look in line for period and parenthesis, indicitave of chart record
                    dot = [ix for ix in range(len(line)) if line[ix:ix+2]=='. ']
                    paren = [ix for ix in range(len(line)) if line[ix:ix+1]=='(']
                    if dot and paren:
                        dot = dot[0]
                        paren = paren[-1]
                        # If ' - '  exists then it's an album or a track
                        dash = [ix for ix in range(len(line)) if line[ix:ix+3]==' - ']
                        if dash:
                            dash = dash[0]
                            data['artist'] += [line[dot+1:dash].strip()]
                            data['media'] += [line[dash+2:paren].strip()]
                        # If ' - ' doesn't exist then it's an artist
                        else:
                            data['artist'] += [line[dot+1:paren].strip()]
                            data['media'] += ['']
                        data['week'] += [chart_weeks['csv'][j]]
                        data['rank'] += [line[0:dot]]
                        data['media_type'] += [media_type]
                        data['score_type'] += [score_type]
                        data['score'] += [line[paren+1:-1]]
                        data['station'] += [station]
                        data['url'] += [page_url]
    except:
        continue
        
        
# Create dataframe out of dict
df = pd.DataFrame(data, columns=data.keys())
df.index.name = 'index'

# Create csv out of dataframe
df_out = df.astype(str)
df_out.to_csv(output_dir + 'somafm_charts.csv')
