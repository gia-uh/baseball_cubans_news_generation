import json
from typing import Dict, List
import requests
from bs4 import Comment
from bs4 import BeautifulSoup
import datetime
from .base import Scrapper

PARSER = 'lxml'
try:
    import lxml
except ImportError:
    PARSER = 'html.parser'

nation = {
    'all': 0,
    'Aruba': 45,
    'Australia': 8,
    'Brasil': 47,
    'Canadá': 2,
    'Colombia': 14,
    'Cuba': 15,
    'Curacao': 16,
    'República Dominicana': 19,
    'Alemania': 23,
    'Honduras': 25,
    'Japón': 29,
    'Lituania': 117,
    'México': 30,
    'Holanda': 31,
    'Nicaragua': 32,
    'Panamá': 35,
    'Puerto Rico': 5,
    'Corea del Sur': 55,
    'Taiwán': 107,
    'Estados Unidos': 1,
    'Venezuela': 42
}

class Scrapper_for_country(Scrapper):
    __slots__ = ('_country', '_ss', '_base_url')
    def __init__(self, country = 'all'):
        super().__init__()
        self._country = country
        self._ss = requests.Session()
        self._ss.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Safari/537.36'
        self._ss.headers['Accept-Encoding'] = 'gzip, deflate'
        self._base_url = 'https://www.baseball-reference.com'

    @property
    def country(self):
        return self._country

    def _scrap(self):
        return self.get_players()

    def get_players(self):

        session = self._ss

        base_url = self._base_url

        year = datetime.date.today().year
        # TODO: cambiar esto para tener en cuanta el país selccionado
        r = session.get(base_url + '/bio/Cuba_born.shtml')
        bsObj = BeautifulSoup(r.text, PARSER)

        hitters = bsObj.find('table', {'id': 'bio_batting'}).tbody.find_all('tr')

        comments = bsObj.find_all(string=lambda text: isinstance(text, Comment))

        for i in comments:
            bs = BeautifulSoup(i, PARSER)
            p = bs.find('table', {'id': 'bio_pitching'})
            if p is not None:
                pitchers = p.tbody.findAll('tr')
                break

        players = []
        players_team = {}

        players_team['complete_list'] = []
        players_team['current_year_list'] = {}

        for h in hitters:
            if 'class' not in h:
                name = h.find('td', {'data-stat': 'player'}).a.get_text()
                link = h.find('td', {'data-stat': 'player'}).a['href']
                player_id = h.find('td', {'data-stat': 'player'})['data-append-csv']
                year_max = h.find('td', {'data-stat': 'year_max'}).get_text()
                year_max = int(year_max)
                players_team['complete_list'].append(player_id)
                if year_max == year:
                    if name not in players:
                        players.append(name)
                        players_team['current_year_list'][name] = link

        for p in pitchers:
            if 'class' not in p:
                name = p.find('td', {'data-stat': 'player'}).a.get_text()
                player_id = p.find('td', {'data-stat': 'player'})['data-append-csv']
                link = p.find('td', {'data-stat': 'player'}).a['href']
                year_max = p.find('td', {'data-stat': 'year_max'}).get_text()
                year_max = int(year_max)
                players_team['complete_list'].append(player_id)
                if year_max == year:
                    if name not in players:
                        players.append(name)
                        players_team['current_year_list'][name] = link


        for p in players:
            r = session.get(base_url + players_team['current_year_list'][p])
            bsObj = BeautifulSoup(r.text, PARSER)
            team = bsObj.find('div', {'id': 'info'}).find_all('p')[3].a.get_text()
            players_team['current_year_list'][p] = team

        return players_team
