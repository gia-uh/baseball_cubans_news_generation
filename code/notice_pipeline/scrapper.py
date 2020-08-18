import json
from typing import Dict, List, Union
import requests
from bs4 import Comment
from bs4 import BeautifulSoup
from .base import ScrapperGames
import re

PARSER = 'lxml'
try:
    import lxml
except ImportError:
    PARSER = 'html.parser'




class Scrapper_BR(ScrapperGames):
    __slots__ = ('_players', '_ss', '_base_url')
    def __init__(self, players: List[str]):
        super().__init__()
        self._players = players['complete_list']
        self._ss = requests.Session()
        self._ss.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Safari/537.36'
        self._ss.headers['Accept-Encoding'] = 'gzip, deflate'
        self._base_url = 'https://www.baseball-reference.com'
        self._data = {}
        self._data['players_details'] = {}
        self._data['all_games_details'] = []
        self._data['top_players'] = []
        self._data['players_details']['hitters'] = {}
        self._data['players_details']['pitchers'] = {}

    # def __call__(self, country_results):
    #     if isinstance(country_results, dict):
    #         self._players = list(country_results.keys())
    #     self._players = country_results

    def _get_game_score(self, bsObj):

        game_details = {}

        scorebox = bsObj.find('div', {'class': 'scorebox'})

        names_teams = scorebox.findAll('strong')[:2]

        away = names_teams[0].a.get_text()
        home = names_teams[1].a.get_text()

        game_details[away] = {}
        game_details[home] = {}

        scores = scorebox.findAll('div', {'class': 'score'})

        game_details[away]['score'] = int(scores[0].get_text())
        game_details[home]['score'] = int(scores[1].get_text())

        divs = scorebox.findAll('div')

        game_details[away]['season_score'] = divs[5].get_text()
        game_details[home]['season_score'] = divs[12].get_text()

        scorebox_meta = bsObj.find('div', {'class': 'scorebox_meta'}).find_all('div')[2]

        stadium = scorebox_meta.get_text()
        stadium = stadium.replace('Venue: ', '')

        game_details['stadium'] = stadium

        game_details['uod'] = 1
        for game in self._data['all_games_details']:
            if away in game and home in game:
                game['uod'] = 2
                game_details['uod'] = 3
                break

        linescore = bsObj.find('div', {'class': 'linescore_wrap'}).tfoot.get_text().strip()
        if linescore=='':
            return

        wls = re.findall('(?:LP:|WP:|SV:).+?\(([0-9]+\-[0-9]+)',linescore)
        win = wls[0]
        lose = wls[1]
        sv = ''
        if len(wls) > 2:
            sv = wls[2]

        game_details['WP'] = win
        game_details['LP'] = lose
        if sv != '':
            game_details['SV'] = sv

        self._data['all_games_details'].append(game_details)

        return game_details

    def _get_hitters(self, name_team, game_bsObj, players_p, game_details):
        comments = game_bsObj.find_all(string=lambda text: isinstance(text, Comment))
        for i in comments:
            bs = BeautifulSoup(i, PARSER)
            players = bs.find('table', {'id': name_team + 'batting'})
            if players is not None:
                players = players.tbody.findAll('tr')
                break
        players_details = self._data['players_details']
        filter_players = set(self._players)
        for p in players:
            position = p.find('th')
            link = position.find('a')
            if link is None:
                continue
            name = link.get_text()
            name_and_pos = position.get_text().lstrip()
            pos = name_and_pos.replace(name, '').lstrip()
            if pos == 'P':
                continue
            name = link.get_text()
            if len(filter_players) > 0 and name not in filter_players:
                continue
            if game_details['uod'] == 2:
                name = name + '_1'
            if game_details['uod'] == 3:
                name = name + '_2'
            players_p[name] = 'batter'
            players_details['hitters'][name] = {}
            players_details['hitters'][name]['position'] = pos
            players_details['hitters'][name]['plays'] = []
            players_details['hitters'][name]['game_details'] = game_details
            stats = p.findAll('td')
            for s in stats:
                k = s['data-stat']
                v = s.get_text()
                players_details['hitters'][name][k] = v

    def _get_pitchers(self, name_team, game_bsObj, players_p, game_details):
        comments = game_bsObj.find_all(string=lambda text: isinstance(text, Comment))
        for i in comments:
            bs = BeautifulSoup(i, PARSER)
            players = bs.find('table', {'id': name_team + 'pitching'})
            if players is not None:
                players = players.tbody.findAll('tr')
                break
        players_details = self._data['players_details']
        filter_players = set(self._players)
        for p in players:
            position = p.find('th')
            link = position.find('a')
            if link is None:
                continue
            name_and_impact = position.get_text().lstrip()
            name = link.get_text()
            impact = name_and_impact.replace(name, '')
            if len(filter_players) > 0 and name not in filter_players:
                continue
            if game_details['uod'] == 2:
                name = name + '_1'
            if game_details['uod'] == 3:
                name = name + '_2'
            players_p[name] = 'pitcher'
            players_details['pitchers'][name] = {}
            players_details['pitchers'][name]['position'] = 'P'
            players_details['pitchers'][name]['impact'] = impact
            players_details['pitchers'][name]['plays'] = []
            players_details['pitchers'][name]['game_details'] = game_details
            stats = p.findAll('td')
            for s in stats:
                k = s['data-stat']
                v = s.get_text()
                players_details['pitchers'][name][k] = v

    def _get_plays(self, players, game_bsObj):
        comments = game_bsObj.find_all(string=lambda text: isinstance(text, Comment))
        for i in comments:
            bs = BeautifulSoup(i, PARSER)
            plays = bs.find('table', {'id': 'play_by_play'})
            if plays is not None:
                plays = plays.tbody.findAll('tr')
                break
        players_details = self._data['players_details']
        for p in plays:
            if not p.has_attr('id'):
                continue
            details = {}
            play_details = p.findAll('td')
            details['inning'] = p.find('th').get_text()
            for pd in play_details:
                details[pd['data-stat']] = pd.get_text()
            details['batter'] = details['batter'].replace('\xa0', ' ')
            details['pitcher'] = details['pitcher'].replace('\xa0', ' ')
            batter = details['batter']
            pitcher = details['pitcher']
            if batter in players and players[batter] == 'batter':
                players_details['hitters'][batter]['plays'].append( details.copy() )
            if pitcher in players and players[pitcher] == 'pitcher':
                players_details['pitchers'][pitcher]['plays'].append( details.copy() )
            if (batter + '_1') in players and players[(batter + '_1')] == 'batter':
                players_details['hitters'][(batter + '_1')]['plays'].append( details.copy() )
            if (pitcher + '_1') in players and players[(pitcher + '_1')] == 'pitcher':
                players_details['pitchers'][(pitcher + '_1')]['plays'].append( details.copy() )
            if (batter + '_2') in players and players[(batter + '_2')] == 'batter':
                players_details['hitters'][(batter + '_2')]['plays'].append( details.copy() )
            if (pitcher + '_2') in players and players[(pitcher + '_2')] == 'pitcher':
                players_details['pitchers'][(pitcher + '_2')]['plays'].append( details.copy() )

    def _get_play_description(self, play):
        if isinstance(play, dict):
            return play
        play_details = {}
        play_details['event'] = ''
        play_details['direction'] = ''
        direction_details = ''
        play_and_runnbases = play.split(';')
        event = play_and_runnbases[0]
        play_details['on_bases'] = {'1B': False, '2B': False, '3B': False}
        play_details['RBI'] = 0

        d = {
            'Single': '1B',
            'Double': '2B',
            'Triple': '3B',
            'Walk': '1B'
        }

        if 'Walk' in event:
            play_details['on_bases']['1B'] = True

        if 'Single to' in event or 'Double to' in event or 'Triple to' in event or 'Home Run' in event:
            event_splitted = event.split()
            if event_splitted[0] == 'Home':
                play_details['event'] = 'Home Run'
                play_details['RBI'] += 1
            else:
                play_details['on_bases'][d[event_splitted[0]]] = True
                play_details['event'] = event_splitted[0]
                direction_details = event_splitted[2]

        elif ':' in event:
            event_splitted = event.split(':')
            play_details['event'] = event_splitted[0]
            direction_details = event_splitted[1].lstrip().split('(')[0].split()[0].split('/')[0]


        elif 'Walk' in event or 'Strikeout' in event:
            cur = event.split()
            play_details['event'] = cur[0]

        else:
            play_details['event'] = 'DISCARD'

        for adv in play_and_runnbases[1:]:
            details = adv.split()
            if ' to ' in adv:
                play_details['on_bases'][details[2]] = True
            else:
                if 'No RBI' not in adv:
                    play_details['RBI'] += 1

        play_details['direction'] = direction_details

        return play_details

    def _get_team_and_rival(self, player, player_details):
        play_1 = player_details['plays'][0]
        top_or_bottom = play_1['inning'][0]
        batter = play_1['batter']
        pitcher = play_1['pitcher']
        teams = list(player_details['game_details'].keys())
        if batter in player and top_or_bottom == 't':
            return (teams[0], teams[1])
        elif pitcher in player and top_or_bottom == 'b':
            return (teams[0], teams[1])
        return (teams[1], teams[0])

    def _win_or_lose(self, player_details):
        teams = list(player_details['game_details'].keys())
        away_score = player_details['game_details'][teams[0]]['score']
        home_score = player_details['game_details'][teams[1]]['score']
        if teams[0] == player_details['team'] and away_score > home_score:
            return 'win'
        elif teams[1] == player_details['team'] and home_score > away_score:
            return 'win'
        return 'lose'

    def _get_current_score_team(self, player_details, play_dict):
        scores = play_dict['score_batting_team'].split('-')
        if player_details['position'] == 'P':
            return (int(scores[1]), int(scores[0]))
        return (int(scores[0]), int(scores[1]))

    def _get_runs_outs_result(self, play_dict):
        result = play_dict['runs_outs_result']
        return ( result.count('R'), result.count('O') )

    def _get_on_base_result(self, play_dict):
        x = play_dict['play_desc']['on_bases']['1B']
        y = play_dict['play_desc']['on_bases']['2B']
        z = play_dict['play_desc']['on_bases']['3B']
        return (x, y, z)

    def _get_real_wpa(self, player_details, play_dict):
        w = play_dict['win_probability_added'].replace('%', '')
        wpa = int(w)
        wl = self._win_or_lose(player_details)
        if wl == 'win':
            return wpa
        return -wpa

    def _get_extra_bases(self, player_details):
        double = 0
        triple = 0
        home_run = 0
        plays = player_details['plays']
        for p in plays:
            if p['play_desc']['event'] == 'Double':
                double += 1
            elif p['play_desc']['event'] == 'Triple':
                triple += 1
            elif p['play_desc']['event'] == 'Home Run':
                home_run += 1
        return (double, triple, home_run)

    def _convert_player(self, player, player_details):

        if not 'position' in player_details:
            player_details['position'] = 'P'

        if len(player_details['plays']) == 0:
            return

        player_details['team'], player_details['rival_team'] = self._get_team_and_rival(player, player_details)
        player_details['result'] = self._win_or_lose(player_details)

        score_team = int(player_details['game_details'][player_details['team']]['score'])
        player_details['game_details'][player_details['team']]['score'] = score_team
        score_rival_team = int(player_details['game_details'][player_details['rival_team']]['score'])
        player_details['game_details'][player_details['rival_team']]['score'] = score_rival_team

        plays = player_details['plays']
        for p in plays:
            p['current_score'], p['current_rival_score'] = self._get_current_score_team(player_details, p)
            p['outs'] = int(p['outs'])
            p['runs_play_result'], p['outs_play_result'] = self._get_runs_outs_result(p)
            p['wpa'] = self._get_real_wpa(player_details, p)
            p['on_base_result'] = self._get_on_base_result(p)

    def _convert_hitter(self, player, player_details):
        player_details['AB'] = int(player_details['AB'])
        player_details['H'] = int(player_details['H'])
        player_details['R'] = int(player_details['R'])
        player_details['RBI'] = int(player_details['RBI'])
        player_details['BB'] = int(player_details['BB'])
        player_details['SO'] = int(player_details['SO'])
        x, y, z = self._get_extra_bases(player_details)
        player_details['Double'], player_details['Triple'], player_details['HR'] = (x, y, z)

    def _convert_pitcher(self, player, player_details):
        player_details['IP'] = player_details['IP'].strip()
        player_details['H'] = int(player_details['H'])
        player_details['R'] = int(player_details['R'])
        player_details['ER'] = int(player_details['ER'])
        player_details['BB'] = int(player_details['BB'])
        player_details['SO'] = int(player_details['SO'])
        player_details['batters_faced'] = int(player_details['batters_faced'])

    def _scrap(self):
        session = self._ss
        base_url = self._base_url
        # get links games
        games_links = []
        r = session.get(base_url)
        #r = session.get(base_url + '/boxes/?month=8&day=10&year=2020')
        bsObj = BeautifulSoup(r.text, PARSER)
        scores = bsObj.find('div', {'id': 'scores'})
        #scores = bsObj.find('div', {'class': 'game_summaries'})
        games_refs = scores.findAll('td', {'class': 'right gamelink'})

        for l in games_refs:
            link = l.a['href']
            f_or_s = l.a.get_text()
            if 'Final' in f_or_s:
                games_links.append(l.a['href'])
                r = session.get(base_url+link)
                bsObj = BeautifulSoup(r.text, PARSER)
                self._get_game_score(bsObj)

        for i in range(len(games_links)):
            r = session.get(base_url+games_links[i])
            bsObj = BeautifulSoup(r.text, PARSER)
            game_details = self._data['all_games_details'][i]
            # get filter players
            away_team = list(game_details.keys())[0]
            home_team = list(game_details.keys())[1]
            away_team = away_team.replace('.', '').replace(' ', '')
            home_team = home_team.replace('.', '').replace(' ', '')
            players = {}
            #away team players
            self._get_hitters(away_team, bsObj, players, game_details)
            self._get_pitchers(away_team, bsObj, players, game_details)
            #home team players
            self._get_hitters(home_team, bsObj, players, game_details)
            self._get_pitchers(home_team, bsObj, players, game_details)
            self._get_plays(players, bsObj)

        players_details = self._data['players_details']

        for player in players_details['hitters']:
            for play in players_details['hitters'][player]['plays']:
                play_desc = self._get_play_description(play['play_desc'])
                play['play_desc'] = play_desc

        for player in players_details['pitchers']:
            for play in players_details['pitchers'][player]['plays']:
                play_desc = self._get_play_description(play['play_desc'])
                play['play_desc'] = play_desc

        hitters = list(players_details['hitters'].keys())
        pitchers = list(players_details['pitchers'].keys())

        for h in hitters:
            pd = players_details['hitters'][h]
            self._convert_player(h, pd)
            self._convert_hitter(h, pd)

        for p in pitchers:
            pd = players_details['pitchers'][p]
            self._convert_player(p, pd)
            self._convert_pitcher(p, pd)

        return {'all_games_details': self._data['all_games_details'],
                'game_day_data': players_details}
