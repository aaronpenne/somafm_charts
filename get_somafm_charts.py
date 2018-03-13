# -*- coding: utf-8 -*-
"""
Simple scraper to pull the 'Top 30' charts from SomaFM (somafm.com) and reformat them
for analysis.

Author: Aaron Penne
Created: 2018-03-07

Developed with:
    Python 3.6
    Windows 10
"""

from lxml import html
import requests
from datetime import date, timedelta
import pandas as pd
import os
from multiprocessing.dummy import Pool
import itertools

# Set output directory, make it if needed
output_dir = os.path.realpath(r'C:\tmp\somafm')  # Windows machine
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

# List of all channel names formatted as in chart urls
channel_url_names = ['bagel',
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

def last_saturday():
    """Round today's date to the most recent Saturday (when charts are published)"""
    
    today = date.today()
    today_index = (today.weekday() + 1) % 7
    week = today - timedelta(today_index + 1)
    return week

def get_chart_weeks(week):
    """Get list of week start dates in two formats"""
    
    chart_weeks = {'url': [],
                   'csv': []}
    while week != date(2000, 1, 1):
        chart_weeks['url'] += [week.strftime('%d%b%y')]  # DDMMMYY (ex. 30Dec17)
        chart_weeks['csv'] += [week.isoformat()]         # YYYY-MM-DD
        week = week - timedelta(days=7)                  # Previous week
    return chart_weeks

def get_channel_charts(args):
    """Gets a single week's charts for a particular channel and reshapes it into readable CSV"""
    
    # args are handled this way to get around single arg limitation of Pool.map
    channel = args[0]
    week_url = args[1]
    week_csv = args[2]
            
    # Clear data for next channel
    data = {'week': [],
            'rank': [],
            'artist': [],
            'media': [],
            'media_type': [],
            'score_type': [],
            'score': [],
            'channel': [],
            'url': []}

    # Search backwards through the weeks until an error occurs (likely end of recorded data) 
    try:
        # Parse raw data from website
        page_url = 'http://somafm.com/charts/{}/{}-{}.html'.format(channel, channel, week_url)
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
                dot = [ix for ix in range(len(line)) if line[ix:ix+2]=='. ']  # This method is used over regex for speed #FIXME check speed
                paren = [ix for ix in range(len(line)) if line[ix:ix+1]=='(']
                if dot and paren:
                    
                    # Ensure the indexes for the first '.' and last '(' are used
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
                        
                    # Fill in rest of data
                    data['week'] += [week_csv]
                    data['rank'] += [line[0:dot]]
                    data['media_type'] += [media_type]
                    data['score_type'] += [score_type]
                    data['score'] += [line[paren+1:-1]]
                    data['channel'] += [channel]
                    data['url'] += [page_url]
                    
    # If error occurs, just move past it
    except:
        pass
    
    # Create dataframe out of dict
    df = pd.DataFrame(data, columns=data.keys())
    df.index.name = 'index'
    return df

    
def main():
    pass  # Local variables aren't showing up in Variable Explorer in Spyder, skip for now
    
if __name__ == '__main__':
    week = last_saturday()
    chart_weeks = get_chart_weeks(week)

    # For each channel, grab weekly charts, aggregate, and create csv
    for channel in channel_url_names:
        print(channel)
        with Pool(10) as p:
            # Run a chunk of weeks in a particular chart in parallel
            data = p.map(get_channel_charts, zip(itertools.repeat(channel), chart_weeks['url'], chart_weeks['csv']))
            
        # Concatenate all dataframes from multithreaded output, resetting index to 0:n-1
        df = pd.concat(data, ignore_index=True)
        
        # Create csv out of dataframe
        df_out = df.astype(str)
        df_out.to_csv(os.path.join(output_dir, 'somafm_charts_' + channel + '.csv'))