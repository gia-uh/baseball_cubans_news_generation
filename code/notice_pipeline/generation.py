import os
import json
import random
from .base import News
from .notice_generator import Player, Play
from .notice_generator.stats_player import Highlights_Player
from .notice_generator.utils import get_yesterday_date as gyd, fill_template
from gensim.summarization import summarize
from .notice_generator.stats_player import Hits, Home_Runs, RBI, Runs

try:
    MODULE = os.path.dirname(os.path.realpath(__file__))
except:
    MODULE = ""

class New_Templates(News):
    __slots__ = ()
    def __init__(self, player_details, sorted_for_outstandings, games_details, players_teams):
        super().__init__(player_details, sorted_for_outstandings, games_details, players_teams)
        self._templates = json.load(open(os.path.join(MODULE,'templates.json')))

    def _get_first_paragraph(self):
        outstandings = self._sorted_for_outstandings
        games_details = self._games_details

        s = set()
        for _, p, _ in outstandings:
            name = p.replace('_2', '').replace('_1', '')
            s.add(name)

        date = gyd()
        text = ''

        d = {
            'fecha': date,
            'cant_jugadores': str(len(outstandings)),
            'cant_juegos': str(len(games_details))
        }

        if len(games_details) == 1:
            text = fill_template(random.choice(self._templates['noticia_juego']['primer_parrafo']\
            ['total_de_juegos']['1']), d)

        else:
            text = fill_template(random.choice(self._templates['noticia_juego']['primer_parrafo']\
            ['total_de_juegos']['>1']), d)

        text_2 = ''

        if len(outstandings) == 0:
            text_2 = fill_template(random.choice(self._templates['noticia_juego']['primer_parrafo']\
            ['total_de_cubanos']['0']), d)
        elif len(outstandings) == 1:
            text_2 = fill_template(random.choice(self._templates['noticia_juego']['primer_parrafo']\
            ['total_de_cubanos']['1']), d)
        else:
            text_2 = fill_template(random.choice(self._templates['noticia_juego']['primer_parrafo']\
            ['total_de_cubanos']['>1']), d)

        c = text_2[0]
        text_2 = c.upper() + text_2[1:]

        c = text[0]
        text = c.upper() + text[1:]

        return text + '. ' + text_2 + '.'

    @staticmethod
    def _sort_games(all_games):

        for i in all_games:
            i['checked'] = False

        all_games_sorted = []
        last = []

        for game in all_games:
            if game['checked']:
                continue
            if game['players']['home'] or game['players']['away']:
                #away = list(game.keys())[0]
                #home = list(game.keys())[1]
                if game['players']['home'] and game['players']['home'][0][1] == 1 and not game['checked']:
                    game['checked'] = True
                    all_games_sorted.append(game)
                    if game['uod'] == 2 or game['uod'] == 3:
                        index = 5 - game['uod']
                        for g in all_games:
                            x = (list(game.keys())[0], list(game.keys())[1])
                            y = (list(g.keys())[0], list(g.keys())[1])
                            if ((x[0] == y[0] and x[1] == y[1]) or (x[1] == y[0] and x[0] == y[1])) and g['uod'] == index and not g['checked']:
                                if g['players']['home'] or g['players']['away']:
                                    g['checked'] = True
                                    all_games_sorted.append(g)
                elif game['players']['away'] and game['players']['away'][0][1] == 1 and not game['checked']:
                    game['checked'] = True
                    all_games_sorted.append(game)
                    if game['uod'] == 2 or game['uod'] == 3:
                        index = 5 - game['uod']
                        for g in all_games:
                            x = (list(game.keys())[0], list(game.keys())[1])
                            y = (list(g.keys())[0], list(g.keys())[1])
                            if ((x[0] == y[0] and x[1] == y[1]) or (x[1] == y[0] and x[0] == y[1])) and g['uod'] == index and not g['checked']:
                                if g['players']['home'] or g['players']['away']:
                                    g['checked'] = True
                                    all_games_sorted.append(g)
                elif not game['checked']:
                    other_game_outstanding = False
                    if game['uod'] == 2 or game['uod'] == 3:
                        index = 5 - game['uod']
                        for g in all_games:
                            x = (list(game.keys())[0], list(game.keys())[1])
                            y = (list(g.keys())[0], list(g.keys())[1])
                            if ((x[0] == y[0] and x[1] == y[1]) or (x[1] == y[0] and x[0] == y[1])) and g['uod'] == index and not g['checked']:
                                if g['players']['home'] and g['players']['home'][0][1] == 1:
                                    other_game_outstanding = True
                                elif g['players']['away'] and g['players']['away'][0][1] == 1:
                                    other_game_outstanding = True
                    if not other_game_outstanding:
                        game['checked'] = True
                        last.append(game)

        all_games_sorted.extend(last)

        return all_games_sorted

    def _get_title(self):
        player_details = self._player_details
        outstandings = self._sorted_for_outstandings

        # parser = ConfigParser()
        # parser.read(os.path.join(MODULE, 'config.ini'))

        # country = parser.get('country', 'country')

        # if country != 'Cuba':
        #     pass

        # else:
        # TODO: cambiar las plantillas basado en la nacionalidad del jugador
        hitters = []
        pitchers = []

        prom_all = 0

        for coef, player, o in outstandings:
            prom_all += coef
            if player in player_details['hitters']:
                hitters.append((coef, player, o))
            else:
                pitchers.append((coef, player, o))

        prom_bat = 0
        prom_pit = 0

        for coef, _, _ in hitters:
            prom_bat += coef

        for coef, _, _ in pitchers:
            prom_pit += coef


        if len(hitters) > 0:
            prom_bat /= len(hitters)

        if len(pitchers) > 0:
            prom_pit /= len(pitchers)

        text = ''

        if len(outstandings) == 0:
            title = random.choice(self._templates['noticia_juego']['titulo']['sin_participacion_cubana'])
            return title


        elif outstandings[0][2] == 1:
            if len(outstandings) > 1 and outstandings[1][2] == 1:
                name_1 = outstandings[0][1]
                name_2 = outstandings[1][1]

                name_1 = name_1.replace('_1', '').replace('_2', '')
                name_2 = name_2.replace('_1', '').replace('_2', '')

                d = {
                    "jugador_1": name_1,
                    "jugador_2": name_2
                }

                text = fill_template(random.choice(self._templates['noticia_juego']['titulo']\
                ['participacion_cubana']['dos_destacados']), d)

            else:
                if outstandings[0] in hitters:
                    name = outstandings[0][1]

                    #p = Player(name, player_details['hitters'][name], self.templates)

                    
                    team = player_details['hitters'][name]['team']

                    hits = player_details['hitters'][name]['H']
                    hr = player_details['hitters'][name]['HR']
                    rbi = player_details['hitters'][name]['RBI']
                    r = player_details['hitters'][name]['R']

                    stats = [
                        (hits, 'con ' + Hits(name, player_details['hitters'][name], self._templates, 'entity').text),
                        (hr, 'con ' + Home_Runs(name, player_details['hitters'][name], self._templates).text),
                        (rbi, 'con ' + RBI(name, player_details['hitters'][name], self._templates, 'entity').text),
                        (r, 'con ' + Runs(name, player_details['hitters'][name], self._templates, 'entity').text)
                    ]

                    stats.sort()
                    stats.reverse()

                    stat_comp = stats[0][1]

                    name = name.replace('_1', '').replace('_2', '')

                    d = {
                        "jugador": name,
                        "estadistica_comp": stat_comp,
                        "equipo": team
                    }

                    if prom_bat > 1.25:
                        text = fill_template(random.choice(self._templates['noticia_juego']['titulo']\
                        ['participacion_cubana']['un_destacado']['bateador']['buen_resultado']), d)

                    elif prom_bat < 0.5:
                        text = fill_template(random.choice(self._templates['noticia_juego']['titulo']\
                        ['participacion_cubana']['un_destacado']['bateador']['mal_resultado']), d)
                    else:
                        text = fill_template(random.choice(self._templates['noticia_juego']['titulo']\
                        ['participacion_cubana']['un_destacado']['bateador']['resultado_medio']), d)
                else:
                    name = outstandings[0][1]
                    team = player_details['pitchers'][name]['team']
                    team_rival = player_details['pitchers'][name]['rival_team']

                    name = name.replace('_1', '').replace('_2', '')

                    d = {
                        "jugador": name,
                        "equipo": team,
                        "equipo_rival": team_rival
                    }

                    if prom_pit > 1.25:
                        text = fill_template(random.choice(self._templates['noticia_juego']['titulo']\
                        ['participacion_cubana']['un_destacado']['lanzador']['buen_resultado']), d)

                    elif prom_pit < 0.5:
                        text = fill_template(random.choice(self._templates['noticia_juego']['titulo']\
                        ['participacion_cubana']['un_destacado']['lanzador']['mal_resultado']), d)
                    else:
                        text = fill_template(random.choice(self._templates['noticia_juego']['titulo']\
                        ['participacion_cubana']['un_destacado']['lanzador']['resultado_medio']), d)

        else:
            if prom_all > 1.00:
                text = random.choice(self._templates['noticia_juego']['titulo']\
                ['participacion_cubana']['sin_destacados']['buen_resultado'])
            else:
                text = random.choice(self._templates['noticia_juego']['titulo']\
                ['participacion_cubana']['sin_destacados']['resultado_medio'])

        c = text[0]
        text = text[1:]
        text = c.upper() + text

        return text

    @staticmethod
    def _get_list_players_text(players):
        text = players[0]
        for i in range(1, len(players)):
            if i == len(players) - 1:
                text += ' y ' + players[i]
            else:
                text += ', ' + players[i]

        return text

    def _get_game_summary(self, game):

        uod = game['uod']

        away_team = list(game.keys())[0]
        home_team = list(game.keys())[1]

        stadium = game['stadium']

        winner_team = ''
        loser_team = ''

        winner_score = ''
        loser_score = ''

        if game[away_team]['score'] > game[home_team]['score']:
            winner_team = away_team
            loser_team = home_team
            winner_score = str(game[away_team]['score'])
            loser_score = str(game[home_team]['score'])
        else:
            winner_team = home_team
            loser_team = away_team
            winner_score = str(game[home_team]['score'])
            loser_score = str(game[away_team]['score'])

        o = []
        all_players = []
        winner_team_players = []
        loser_team_players = []

        for p, oo in game['players']['home']:
            if oo == 1:
                o.append(p.player_name)
            else:
                all_players.append(p.player_name)
                if p.dict_classes['team'].text == winner_team:
                    winner_team_players.append(p)
                else:
                    loser_team_players.append(p)

        for p, oo in game['players']['away']:
            if oo == 1:
                o.append(p.player_name)
            else:
                all_players.append(p.player_name)
                if p.dict_classes['team'].text == winner_team:
                    winner_team_players.append(p)
                else:
                    loser_team_players.append(p)

        outstanding_template = ''
        _get_list_players_text = self._get_list_players_text

        d = {
            "equipo_ganador": winner_team,
            "equipo_perdedor": loser_team,
            "carreras_ganador": winner_score,
            "carreras_perdedor": loser_score,
            "estadio": stadium
        }

        if len(o) > 1:
            d = {
                'destacados': _get_list_players_text(o)
            }
            outstanding_template = fill_template(random.choice(self._templates['noticia_juego']\
            ['resumen_juego']['varios_destacados']), d)
        elif len(o) == 1:
            d = {
                'destacado': o[0]
            }
            outstanding_template = fill_template(random.choice(self._templates['noticia_juego']\
            ['resumen_juego']['un_destacado']), d)

        d = {
            "equipo_ganador": winner_team,
            "equipo_perdedor": loser_team,
            "carreras_ganador": winner_score,
            "carreras_perdedor": loser_score,
            "estadio": stadium,
            "destacados_accion": outstanding_template,
            "jugadores": _get_list_players_text(all_players),
            "jugador": all_players[0]
        }

        initial_sentence = ''

        if uod == 1:
            if o:
                if len(all_players) > 1:
                    initial_sentence = fill_template(random.choice(self._templates['noticia_juego']\
                    ['resumen_juego']['juego_unico']['con_destacados']['varios_jugadores']), d)
                else:
                    initial_sentence = fill_template(random.choice(self._templates['noticia_juego']\
                    ['resumen_juego']['juego_unico']['con_destacados']['solo_un_jugador']), d)
            else:
                if len(all_players) > 1:
                    initial_sentence = fill_template(random.choice(self._templates['noticia_juego']\
                    ['resumen_juego']['juego_unico']['sin_destacados']['varios_jugadores']), d)
                else:
                    initial_sentence = fill_template(random.choice(self._templates['noticia_juego']\
                    ['resumen_juego']['juego_unico']['sin_destacados']['solo_un_jugador']), d)
        elif uod == 2:
            if o:
                if len(all_players) > 1:
                    initial_sentence = fill_template(random.choice(self._templates['noticia_juego']\
                    ['resumen_juego']['primero_del_doble']['con_destacados']['varios_jugadores']), d)
                else:
                    initial_sentence = fill_template(random.choice(self._templates['noticia_juego']\
                    ['resumen_juego']['primero_del_doble']['con_destacados']['solo_un_jugador']), d)
            else:
                if len(all_players) > 1:
                    initial_sentence = fill_template(random.choice(self._templates['noticia_juego']\
                    ['resumen_juego']['primero_del_doble']['sin_destacados']['varios_jugadores']), d)
                else:
                    initial_sentence = fill_template(random.choice(self._templates['noticia_juego']\
                    ['resumen_juego']['primero_del_doble']['sin_destacados']['solo_un_jugador']), d)
        else:
            if o:
                initial_sentence = fill_template(random.choice(self._templates['noticia_juego']\
                ['resumen_juego']['segundo_del_doble']['con_destacados']), d)
            else:
                initial_sentence = fill_template(random.choice(self._templates['noticia_juego']\
                ['resumen_juego']['segundo_del_doble']['sin_destacados']), d)

        mr_winner = []
        mr_loser = []
        mr_all = []

        for p in winner_team_players:
            text = p.get_general_player_stats()
            mr_winner.append(text)
            mr_all.append(text)

        for p in loser_team_players:
            text = p.get_general_player_stats()
            mr_loser.append(text)
            mr_all.append(text)

        rest_of_paragraph = ''

        if winner_team_players:
            rest_of_paragraph += fill_template(random.choice(self._templates['noticia_juego']\
            ['resumen_juego']['resto_del_parrafo']['jugadores_equipo_ganador']), d)
            rest_of_paragraph += ' '
            cont = 0
            for mw in mr_winner:
                if cont > 0:
                    c = mw[0]
                    mw = c.upper() + mw[1:]
                rest_of_paragraph += mw + '. '
                cont += 1


        if loser_team_players:
            rest_of_paragraph_2 = fill_template(random.choice(self._templates['noticia_juego']\
            ['resumen_juego']['resto_del_parrafo']['jugadores_equipo_perdedor']), d)
            c = rest_of_paragraph_2[0]
            rest_of_paragraph_2 = c.upper() + rest_of_paragraph_2[1:]
            rest_of_paragraph += rest_of_paragraph_2
            rest_of_paragraph += ' '
            cont = 0
            for mw in mr_loser:
                if cont > 0:
                    c = mw[0]
                    mw = c.upper() + mw[1:]
                rest_of_paragraph += mw + '. '
                cont += 1

        c = initial_sentence[0]
        initial_sentence = c.upper() + initial_sentence[1:]

        c = rest_of_paragraph[0]
        rest_of_paragraph = c.upper() + rest_of_paragraph[1:]

        return initial_sentence + '. ' + rest_of_paragraph

    def _generate_game(self, game):
        paragraphs = []
        outstandings = []
        have_not_outstandings = False
        for p, o in game['players']['home']:
            if o == 1:
                outstandings.append(p)
            else:
                have_not_outstandings = True
        for p, o in game['players']['away']:
            if o == 1:
                outstandings.append(p)
            else:
                have_not_outstandings = True

        for i in range(len(outstandings)):
            paragraphs.append(outstandings[i].get_report(i))

        if have_not_outstandings:
            paragraphs.append(self._get_game_summary(game))

        return paragraphs

    def _get_game_without_cubans(self, game):
        uod = game['uod']

        away_team = list(game.keys())[0]
        home_team = list(game.keys())[1]

        #stadium = game['stadium']

        winner_team = ''
        loser_team = ''

        winner_score = ''
        loser_score = ''

        if game[away_team]['score'] > game[home_team]['score']:
            winner_team = away_team
            loser_team = home_team
            winner_score = str(game[away_team]['score'])
            loser_score = str(game[home_team]['score'])
        else:
            winner_team = home_team
            loser_team = away_team
            winner_score = str(game[home_team]['score'])
            loser_score = str(game[away_team]['score'])

        winner_pitcher = game['WP']
        loser_pitcher = game['LP']
        saver_pitcher = ''
        if 'SV' in game:
            saver_pitcher = game['SV']

        player_team = ''
        if not game['players']['home']:
            player_team = away_team
        elif not game['players']['away']:
            player_team = home_team

        all_players = []
        for p in game['players']['home']:
            all_players.append(p)
        for p in game['players']['away']:
            all_players.append(p)

        _get_list_players_text = self._get_list_players_text

        d = {
            "equipo_ganador": winner_team,
            "equipo_perdedor": loser_team,
            "carreras_ganador": winner_score,
            "carreras_perdedor": loser_score,
            "equipo": player_team,
            "jugadores": _get_list_players_text(all_players),
            "jugador": all_players[0]
        }

        text = ''

        if uod == 1:
            if player_team != '':
                if len(all_players) > 1:
                    text = fill_template(random.choice(self._templates['noticia_juego']\
                    ['resumen_juego_sin_cubanos']['juego_unico']['un_solo_equipo']\
                    ['varios_jugadores']), d)
                else:
                    text = fill_template(random.choice(self._templates['noticia_juego']\
                    ['resumen_juego_sin_cubanos']['juego_unico']['un_solo_equipo']\
                    ['un_solo_jugador']), d)
            else:
                text = fill_template(random.choice(self._templates['noticia_juego']\
                ['resumen_juego_sin_cubanos']['juego_unico']['varios_equipos']), d)
        elif uod == 2:
            if player_team != '':
                if len(all_players) > 1:
                    text = fill_template(random.choice(self._templates['noticia_juego']\
                    ['resumen_juego_sin_cubanos']['primero_del_doble']['un_solo_equipo']\
                    ['varios_jugadores']), d)
                else:
                    text = fill_template(random.choice(self._templates['noticia_juego']\
                    ['resumen_juego_sin_cubanos']['primero_del_doble']['un_solo_equipo']\
                    ['un_solo_jugadores']), d)
            else:
                text = fill_template(random.choice(self._templates['noticia_juego']\
                ['resumen_juego_sin_cubanos']['primero_del_doble']['varios_equipos']), d)
        else:
            if player_team != '':
                if len(all_players) > 1:
                    text = fill_template(random.choice(self._templates['noticia_juego']\
                    ['resumen_juego_sin_cubanos']['segundo_del_doble']['un_solo_equipo']\
                    ['varios_jugadores']), d)
                else:
                    text = fill_template(random.choice(self._templates['noticia_juego']\
                    ['resumen_juego_sin_cubanos']['segundo_del_doble']['un_solo_equipo']\
                    ['un_solo_jugadores']), d)
            else:
                text = fill_template(random.choice(self._templates['noticia_juego']\
                ['resumen_juego_sin_cubanos']['segundo_del_doble']['varios_equipos']), d)

        text_2 = ''
        if saver_pitcher != '':
            text_2 = fill_template(random.choice(self._templates['noticia_juego']\
            ['resumen_juego_sin_cubanos']['detalles_del_juego']['con_salvamento']), d)
        else:
            text_2 = fill_template(random.choice(self._templates['noticia_juego']\
            ['resumen_juego_sin_cubanos']['detalles_del_juego']['sin_salvamento']), d)

        c = text[0]
        text = c.upper() + text[1:]

        c = text_2[0]
        text_2 = c.upper() + text_2[1:]

        return text + '. ' + text_2

    def _get_text(self):
        player_details = self._player_details
        games_details = self._games_details
        players_teams = self._players_teams['current_year_list']

        paragraphs = []

        t = self._get_first_paragraph()
        paragraphs.append(t)

        #outstandings = []
        all_players = []

        for _, player, o in self._sorted_for_outstandings:
            if player in player_details['pitchers']:
                p = Player(player, player_details['pitchers'][player], self._templates)
            else:
                p = Player(player, player_details['hitters'][player], self._templates)
            all_players.append((player, o, p))

        all_games = []

        for game in games_details:
            game['players'] = {}
            game['players']['home'] = []
            game['players']['away'] = []
            k = list(game.keys())
            for player, o, p in all_players:
                if p.player_dict['team'] == k[0]:
                    if game['uod'] == 1 or (game['uod'] == 2 and p.first_game) or \
                    (game['uod'] == 3 and p.second_game):
                        game['players']['away'].append((p, o))
                elif p.player_dict['team'] == k[1]:
                    if game['uod'] == 1 or (game['uod'] == 2 and p.first_game) or \
                    (game['uod'] == 3 and p.second_game):
                        game['players']['home'].append((p, o))
            all_games.append(game)

        all_games = self._sort_games(all_games)

        title = self._get_title()

        for g in all_games:
            ps = self._generate_game(g)
            paragraphs.extend(ps)

        cont = 0

        if not all_players:
            for game in games_details:
                game['players'] = {}
                game['players']['home'] = []
                game['players']['away'] = []
                away = list(game.keys())[0]
                home = list(game.keys())[1]
                for p in players_teams:
                    team = players_teams[p]
                    if team == away:
                        game['players']['away'].append(p)
                    elif team == home:
                        game['players']['home'].append(p)
                if game['players']['home'] or game['players']['away']:
                    cont += 1
                    ps = self._get_game_without_cubans(game)
                    paragraphs.append(ps)

        if not cont and not all_players:
            t = random.choice(self._templates['noticia_juego']['sin_participacion_cubana'])
            c = t[0]
            t = c.upper() + t[1:]
            paragraphs.append(t + '.')

        complete_new = ''

        for p in paragraphs:
            complete_new += p + '\n\n'

        summary = summarize(complete_new, word_count=80)

        return {
            'title': title,
            'paragraphs': paragraphs,
            'summary': summary,
        }
