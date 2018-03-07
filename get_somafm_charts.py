from lxml import html
import requests

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


for station in station_url_names:
    page = requests.get('http://somafm.com/charts/{}/{}-03Mar18.html'.format(station, station))
    tree = html.fromstring(page.content)
    
    data = tree.xpath('//div[@id="content"]/pre/text()')
    a = str(data[0])
    b = a.splitlines()
    c = list(filter(None, b))
    print(station, len(c))