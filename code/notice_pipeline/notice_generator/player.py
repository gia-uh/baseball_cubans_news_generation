# this imports are ugly but necessary
from .stats_play import *
from .stats_player import *
import random

class Player:
    def __init__(self, player_name, player_dict, templates):
        self.templates = templates
        self.dict_classes = {}
        self.player_dict = player_dict
        self.player_name = player_name
        self.first_game = False
        self.second_game = False
        self.init_classes()

    def init_classes(self):

        if '_1' in self.player_name:
            self.first_game = True
            self.player_name = self.player_name.replace('_1', '')

        if '_2' in self.player_name:
            self.second_game = True
            self.player_name = self.player_name.replace('_2', '')

        self.dict_classes['player_name'] = Player_name(self.player_name, self.player_dict, self.templates)
        self.dict_classes['position'] = Position(self.player_name, self.player_dict, self.templates)
        self.dict_classes['team'] = Team(self.player_name, self.player_dict, self.templates)
        self.dict_classes['rival_team'] = Rival_Team(self.player_name, self.player_dict, self.templates)
        self.dict_classes['H'] = Hits(self.player_name, self.player_dict, self.templates, 'Entity')

        self.dict_classes['plays'] = []

        for play in self.player_dict['plays']:
            self.dict_classes['plays'].append(Play(self.player_name, self.player_dict, play, self.templates))

    def _last_name(self):
        n = self.player_name.split()
        text = ''
        for i in n[1:]:
            text += i + ' '
        return text.rstrip()

    def rbi_on_play(self, play):
        return self.player_dict['position'] != 'P' and play.play_dict['play_desc']['RBI'] > 0

    def _rbi_and_runs(self):
        r = self.player_dict['R']
        rbi = self.player_dict['RBI']

        r_text = self.dict_classes['runs']['entity'].text
        rbi_text = self.dict_classes['RBI']['entity'].text

        if r > 0 and rbi > 0:
            return r_text + ' y ' + rbi_text
        elif r > 0:
            return r_text
        else:
            return rbi_text

    def get_general_player_stats(self):

        text = ''
        last_name = self._last_name()
        self.dict_classes['hits'] = {}
        self.dict_classes['runs'] = {}

        self.dict_classes['hits']['entity'] = Hits(self.player_name, self.player_dict, self.templates, 'entity')
        self.dict_classes['hits']['action'] = Hits(self.player_name, self.player_dict, self.templates)
        self.dict_classes['runs']['entity'] = Runs(self.player_name, self.player_dict, self.templates, 'entity')
        self.dict_classes['runs']['action'] = Runs(self.player_name, self.player_dict, self.templates)
        self.dict_classes['BB'] = BB(self.player_name, self.player_dict, self.templates)

        if self.player_dict['position'] != 'P':

            self.dict_classes['RBI'] = {}

            self.dict_classes['AB'] = AB(self.player_name, self.player_dict, self.templates)
            self.dict_classes['Double'] = Doubles(self.player_name, self.player_dict, self.templates)
            self.dict_classes['Triple'] = Triples(self.player_name, self.player_dict, self.templates)
            self.dict_classes['HR'] = Home_Runs(self.player_name, self.player_dict, self.templates)
            self.dict_classes['RBI']['entity'] = RBI(self.player_name, self.player_dict, self.templates, 'entity')
            self.dict_classes['RBI']['action'] = RBI(self.player_name, self.player_dict, self.templates)

            # complement = self.dict_classes['AB'].text
            ads = []
            if self.player_dict['HR'] > 0:
                ads.append(self.dict_classes['HR'])
            if self.player_dict['Triple'] > 0:
                ads.append(self.dict_classes['Triple'])
            if self.player_dict['Double'] > 0:
                ads.append(self.dict_classes['Double'])

            #ads.append(self.dict_classes['BB'])

            r = self.player_dict['R']
            rbi = self.player_dict['RBI']

            rbi_and_runs = self._rbi_and_runs()

            #text = ll[0].text + ', con ' + ll[1].text
            text_1 = ''

            if len(ads) == 1:
                text_1 += ads[0].text
            elif ads:
                text_1 += ads[0].text
                for i in range(1, len(ads)):
                    if i == len(ads) - 1:
                        text_1 += ' y ' + ads[i].text
                    else:
                        text_1 += ', ' + ads[i].text

            d = {
                "nombre": last_name,
                "hits_accion": self.dict_classes['hits']['action'].text,
                "AB_comp": self.dict_classes['AB'].text,
                "extrabases_entidad": text_1,
                "extrabases_accion": "conectó " + text_1,
                "RBI_R_entidad": rbi_and_runs
            }

            if r > 0 or rbi > 0:
                if ads:
                    text = fill_template(random.choice(self.templates['noticia_jugador']\
                    ['estadisticas_generales_jugador']['bateador']['anotadas_o_impulsadas']\
                    ['extrabases']), d)
                else:
                    text = fill_template(random.choice(self.templates['noticia_jugador']\
                    ['estadisticas_generales_jugador']['bateador']['anotadas_o_impulsadas']\
                    ['sin_extrabases']), d)
            else:
                if ads:
                    text = fill_template(random.choice(self.templates['noticia_jugador']\
                    ['estadisticas_generales_jugador']['bateador']['sin_anotadas_ni_impulsadas']\
                    ['extrabases']), d)
                else:
                    text = fill_template(random.choice(self.templates['noticia_jugador']\
                    ['estadisticas_generales_jugador']['bateador']['sin_anotadas_ni_impulsadas']\
                    ['sin_extrabases']), d)

        else:
            self.dict_classes['impact'] = Impact(self.player_name, self.player_dict, self.templates)
            self.dict_classes['IP'] = IP(self.player_name, self.player_dict, self.templates)
            self.dict_classes['SO'] = SO(self.player_name, self.player_dict, self.templates)
            self.dict_classes['batters_faced'] = Batters_faced(self.player_name, self.player_dict, self.templates)

            d = {
                "IP_comp": self.dict_classes['IP'].text,
                "nombre": last_name,
                "bateadores_enfrentados_accion": self.dict_classes['batters_faced'].text,
                "R_accion": self.dict_classes['runs']['action'].text,
                "hits_accion": self.dict_classes['hits']['action'].text,
                "SO_entidad": self.dict_classes['SO'].text,
                "BB_entidad": self.dict_classes['BB'].text,
                "impacto_accion": self.dict_classes['impact'].text
            }

            if self.dict_classes['impact'].text != '':
                text = fill_template(random.choice(self.templates['noticia_jugador']\
                    ['estadisticas_generales_jugador']['lanzador']['con_impacto_en_juego']), d)
            else:
                text = fill_template(random.choice(self.templates['noticia_jugador']\
                    ['estadisticas_generales_jugador']['lanzador']['sin_impacto_en_juego']), d)

        return text

    def get_initial_sentence(self, i):
        text = ''

        wl = self.player_dict['result']

        score_team = self.player_dict['game_details'][self.player_dict['team']]['score']
        score_rival_team = self.player_dict['game_details'][self.player_dict['rival_team']]['score']
        season_rival_score = \
        self.player_dict['game_details'][self.player_dict['rival_team']]['season_score']
        season_score = self.player_dict['game_details'][self.player_dict['team']]['season_score']

        d = {
            "nombre": self.player_name,
            "equipo": self.player_dict['team'] + ' (' + season_score + ')',
            "carreras_equipo": str(score_team),
            "equipo_rival": self.player_dict['rival_team'] + ' (' + season_rival_score + ')',
            "carreras_equipo_rival": str(score_rival_team)
        }

        if wl == 'win':
            if self.first_game:
                text = fill_template(random.choice(self.templates['noticia_jugador']['oracion_inicial']\
                ['victoria']['primero_del_doble']), d)
            elif self.second_game:
                text = fill_template(random.choice(self.templates['noticia_jugador']['oracion_inicial']\
                ['victoria']['segundo_del_doble']), d)
            else:
                text = fill_template(random.choice(self.templates['noticia_jugador']['oracion_inicial']\
                ['victoria']['juego_unico']), d)

        else:
            if self.first_game:
                text = fill_template(random.choice(self.templates['noticia_jugador']['oracion_inicial']\
                ['derrota']['primero_del_doble']), d)
            elif self.second_game:
                text = fill_template(random.choice(self.templates['noticia_jugador']['oracion_inicial']\
                ['derrota']['segundo_del_doble']), d)
            else:
                text = fill_template(random.choice(self.templates['noticia_jugador']['oracion_inicial']\
                ['derrota']['juego_unico']), d)

        if i > 0:
            text = fill_template(random.choice(self.templates['noticia_jugador']['oracion_inicial']\
                ['segundo_destacado_del_juego']), d)

        c = text[0]
        c = c.upper()
        text = text[1:]
        text = c + text

        text += '. '

        return text

    def get_report(self, i):
        self.dict_classes['plays'].sort()

        plays = self.dict_classes['plays']
        text = ''

        ic = self.get_initial_sentence(i)

        ps = []

        ps.append(ic)

        plays.sort()
        plays.reverse()

        for p in plays:
            if (p.wpa >= 5 or self.rbi_on_play(p)) and p.play_dict['play_desc']['event'] != 'DISCARD':
                ps.append(p.get_text_play())

        gp = self.get_general_player_stats()

        fc = gp[0]
        gp = gp[1:]
        fc = fc.upper()
        gp = fc + gp

        if self.player_dict['position'] != 'P':
            fc = gp[0].lower()

            '''
            gp = gp[1:]
            gp = fc + gp

            gp = 'En el juego ' + gp
            '''
        gp += '. '

        ps.insert(2, gp)

        for p in ps:
            text += p

        text = text.replace(' de el ', ' del ')
        text = text.replace(' a el ', ' al ')
        text = text.replace('  ', ' ')
        text = text.replace(' ,', ',')

        return text

    def get_minority_report(self):
        text = ''

        text2 = 'en '

        if self.player_dict['result'] == 'win':
            text2 += 'la victoria de '
        else:
            text2 += 'la derrota de '

        team = self.player_dict['team']
        score_team = self.player_dict['game_details'][team]['score']
        season_team = self.player_dict['game_details'][team]['season_score']

        rival_team = self.player_dict['rival_team']
        score_rival_team = self.player_dict['game_details'][rival_team]['score']
        season_rival_team = self.player_dict['game_details'][rival_team]['season_score']

        text2 += team + ' (' + season_team + ') ' + str(score_team) + '-' + str(score_rival_team) + \
        ' contra ' + rival_team + ' (' + season_rival_team + '). '

        general_stats = self.get_general_player_stats()

        fc = general_stats[0].lower()

        general_stats = general_stats[1:]
        general_stats = fc + general_stats

        text = self.player_name + ' ' + general_stats[:-2] + ', ' + text2

        if self.first_game:
            text = text[:-2] + ', en el primero de dos encuentros disputados. '

        if self.second_game:
            text = text[:-2] + ', en el segundo de dos encuentros disputados. '

        return text

class Play:
    def __init__(self, player_name, player_dict, play_dict, templates):
        #super().__init__(player_name, player_dict)
        self.templates = templates
        self.player_name = player_name
        self.player_dict = player_dict
        self.play_dict = play_dict
        self.wpa = play_dict['wpa']
        self.dict_classes = {}
        self.init_classes()
        self.init_c()

    def __lt__(self, play):
        return self.wpa < play.wpa

    def init_c(self):
        self.dict_classes['player_name'] = Player_name(self.player_name, self.player_dict, self.templates)
        self.dict_classes['position'] = Position(self.player_name, self.player_dict, self.templates)
        self.dict_classes['team'] = Team(self.player_name, self.player_dict, self.templates)
        self.dict_classes['rival_team'] = Rival_Team(self.player_name, self.player_dict, self.templates)
        self.dict_classes['referring'] = Referring([self.dict_classes['player_name'].text, \
        self.dict_classes['position'].text, 'el cubano'])

    def init_classes(self):
        self.dict_classes['play_desc'] = {}
        self.dict_classes['inning'] = Inning(self.player_name, self.player_dict, self.templates, self.play_dict)
        self.dict_classes['current_score'] = \
        Current_Score(self.player_name, self.player_dict, self.templates, self.play_dict)
        self.dict_classes['outs'] = Outs(self.player_name, self.player_dict, self.templates, self.play_dict)
        self.dict_classes['rob'] = ROB(self.player_name, self.player_dict, self.templates, self.play_dict)
        self.dict_classes['pitcher'] = \
        Current_Pitcher(self.player_name, self.player_dict, self.templates, self.play_dict)
        self.dict_classes['play_desc']['direction'] = \
        Direction(self.player_name, self.player_dict, self.templates, self.play_dict)
        self.dict_classes['play_desc']['event'] = \
        Event(self.player_name, self.player_dict, self.templates, self.play_dict)
        self.dict_classes['play_desc']['RBI'] = {}
        self.dict_classes['play_desc']['RBI']['action'] = \
        RBI_Result(self.player_name, self.player_dict, self.templates, self.play_dict, 'action')
        self.dict_classes['play_desc']['RBI']['reaction'] = \
        RBI_Result(self.player_name, self.player_dict,  self.templates, self.play_dict, 'reaction')
        self.dict_classes['outs_play_result'] = \
        Out_Play_Results(self.player_name, self.player_dict, self.templates, self.play_dict)
        self.dict_classes['score_result'] = \
        Runs_Play_Result(self.player_name, self.player_dict, self.templates, self.play_dict)

    def get_text_play(self):
        if self.player_dict['position'] != 'P':

            entity = self.dict_classes['referring'].text

            inning = self.dict_classes['inning'].text
            rob = self.dict_classes['rob'].text

            complements = [
                self.dict_classes['current_score'].text,
                self.dict_classes['outs'].text,
                self.dict_classes['pitcher'].text,
            ]

            comp = [rob, random.choice(complements)]

            action = self.dict_classes['play_desc']['event'].text

            reaction = [
                self.dict_classes['score_result'].text,
                self.dict_classes['play_desc']['RBI']['reaction'].text
            ]

            while '' in reaction:
                reaction.remove('')

            comp_after_event = self.dict_classes['play_desc']['direction'].text

        else:
            entity = self.dict_classes['referring'].text

            inning = self.dict_classes['inning'].text

            #current_score = self.dict_classes['current_score'].text
            #outs = self.dict_classes['outs'].text
            rob = self.dict_classes['rob'].text

            complements = [
                self.dict_classes['current_score'].text,
                self.dict_classes['outs'].text,
            ]

            comp = [rob, random.choice(complements)]

            action = self.dict_classes['play_desc']['event'].text

            reaction = [
                self.dict_classes['score_result'].text,
                self.dict_classes['outs_play_result'].text
            ]

            while '' in reaction:
                reaction.remove('')

            comp_after_event = self.dict_classes['play_desc']['direction'].text

        d = {
            "jugador": entity,
            "comp_1": comp[0],
            "comp_2": comp[1],
            "inning": inning,
            "accion": action,
            "direccion": comp_after_event,
            "reaccion": random.choice(reaction)
        }

        text = fill_template(random.choice(self.templates['noticia_jugador']['texto_jugada']), d)

        return_text = text

        fc = return_text[0].upper()

        return_text = return_text[1:]
        return_text = fc + return_text + '. '

        return return_text
