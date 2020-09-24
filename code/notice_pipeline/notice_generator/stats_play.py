import random
from .base_class import Stats
from .utils import ordinal as uordinal
#from .utils import direction as udirection
from .utils import fill_template, number

# Complement
class Inning(Stats):
    def get_text(self):
        inning = self._play_dict['inning']
        i = inning[0]
        n = int(inning[1:])

        d = {
            'inning_m': uordinal[n][0],
            'inning_f': uordinal[n][1]
        }

        x = 'inicio'
        if i == 'b':
            x = 'fin'

        return fill_template(random.choice(self._templates['estadisticas']['jugada']['inning']['complemento'][x]), d)

# Complement
class Current_Score(Stats):
    def get_text(self):
        current_score = self._play_dict['current_score']
        current_rival_score = self._play_dict['current_rival_score']
        text = 'ganando'
        subject = self._player_dict['team']

        d = {
            "equipo": subject,
            "marcador_equipo": str(current_score),
            "marcador_equipo_rival": str(current_rival_score)
        }

        if current_score < current_rival_score:
            text = 'perdiendo'
        elif current_score == current_rival_score:
            text = 'empatando'

        return fill_template(random.choice(self._templates['estadisticas']['jugada']['marcador_actual']['complemento'][text]), d)

# Complement
class Outs(Stats):
    def get_text(self):
        outs = str(self._play_dict['outs'])
        return random.choice(self._templates['estadisticas']['jugada']['outs']['complemento'][outs])

# Complement
class ROB(Stats):
    def get_text(self):
        rob = self._play_dict['runners_on_bases_pbp']
        return random.choice(self._templates['estadisticas']['jugada']['corredores_en_base']['complemento'][rob])

# Reaction
class Runs_Play_Result(Stats):
    def get_text(self):
        runs_play_result = self._play_dict['runs_outs_result'].count('R')
        current_score = self._play_dict['current_score']
        current_rival_score = self._play_dict['current_rival_score']
        result_score = current_score
        result_rival_score = current_rival_score
        if self._player_dict['position'] == 'P':
            result_rival_score += runs_play_result
        else:
            result_score += runs_play_result
        team = self._player_dict['team']
        rival_team = self._player_dict['rival_team']
        # t = [team, 'su equipo']
        # rt = [rival_team, 'el equipo contrario']
        # fb = self._play_dict['play_desc']['on_bases']['1B']
        sb = self._play_dict['play_desc']['on_bases']['2B']
        tb = self._play_dict['play_desc']['on_bases']['3B']
        result_score = current_score + runs_play_result

        d = {
            "marcador_equipo": str(result_score),
            "marcador_equipo_rival": str(result_rival_score),
            "equipo": team,
            "equipo_rival": rival_team,
            "diferencia_carreras": str(result_score - current_rival_score)
        }

        if self._player_dict['position'] == 'P':
            result_rival_score = current_rival_score + runs_play_result

            if result_rival_score > current_score:
                return fill_template(random.choice(self._templates['estadisticas']['jugada']['carreras_en_jugada']['reaccion']['lanzador']['pierde']), d)

            if result_rival_score == current_score:
                return fill_template(random.choice(self._templates['estadisticas']['jugada']['carreras_en_jugada']['reaccion']['lanzador']['empata']), d)

            return fill_template(random.choice(self._templates['estadisticas']['jugada']['carreras_en_jugada']['reaccion']['lanzador']['gana']), d)

        if runs_play_result == 0:
            if sb and tb:
                return fill_template(random.choice(self._templates['estadisticas']['jugada']['carreras_en_jugada']['reaccion']['bateador']['0']['2_en_pos_anotadora']), d)
            if sb or tb:
                return fill_template(random.choice(self._templates['estadisticas']['jugada']['carreras_en_jugada']['reaccion']['bateador']['0']['1_en_pos_anotadora']), d)

            return fill_template(random.choice(self._templates['estadisticas']['jugada']['carreras_en_jugada']['reaccion']['bateador']['0']['otro']), d)

        if result_score < current_rival_score:
            return fill_template(random.choice(self._templates['estadisticas']['jugada']['carreras_en_jugada']['reaccion']['bateador']['>=1']['pierde']), d)

        if result_score == current_rival_score:
            return fill_template(random.choice(self._templates['estadisticas']['jugada']['carreras_en_jugada']['reaccion']['bateador']['>=1']['empata']), d)

        if current_score <= current_rival_score:
            return fill_template(random.choice(self._templates['estadisticas']['jugada']['carreras_en_jugada']['reaccion']['bateador']['>=1']['remonta']), d)

        return fill_template(random.choice(self._templates['estadisticas']['jugada']['carreras_en_jugada']['reaccion']['bateador']['>=1']['aumenta_ventaja']), d)

# Reaction
class Out_Play_Results(Stats):
    def get_text(self):
        current_outs = self._play_dict['outs']
        outs_play = self._play_dict['runs_outs_result'].count('O')
        outs_results = current_outs + outs_play

        l = []

        if outs_results == 2:
            return random.choice(self._templates['estadisticas']['jugada']['outs_en_jugada']['reaccion']['2'])

        elif outs_results == 3:
            return random.choice(self._templates['estadisticas']['jugada']['outs_en_jugada']['reaccion']['3'])

        if len(l) == 0:
            return ''

# NO
class Current_Batter(Stats):
    def __init__(self, player_name, player_dict, play_dict):
        super().__init__(player_name, player_dict, play_dict)

# Complement
class Current_Pitcher(Stats):
    def get_text(self):
        current_pitcher = self._play_dict['pitcher']

        d = {
            'lanzador': current_pitcher
        }

        return fill_template(random.choice(self._templates['estadisticas']['jugada']['lanzador_actual']['complemento']), d)

# NO
class WPA(Stats):
    def __init__(self, player_name, player_dict, play_dict):
        super().__init__(player_name, player_dict, play_dict)

# Action, present always
class Event(Stats):
    def get_text(self):
        event = self._play_dict['play_desc']['event']

        batter = self._play_dict['batter']

        d = {
            'bateador': batter
        }

        if event == 'Single':
            return random.choice(self._templates['estadisticas']['jugada']['evento']['accion']['sencillo'])

        elif event == 'Double':
            return random.choice(self._templates['estadisticas']['jugada']['evento']['accion']['doble'])

        elif event == 'Triple':
            return random.choice(self._templates['estadisticas']['jugada']['evento']['accion']['triple'])

        elif event == 'Home Run':
            return random.choice(self._templates['estadisticas']['jugada']['evento']['accion']['home_run'])

        elif event == 'Walk':
            return random.choice(self._templates['estadisticas']['jugada']['evento']['accion']['base_por_bolas'])

        elif event == 'Groundout':
            if self._player_dict['position'] != 'P':
                return random.choice(self._templates['estadisticas']['jugada']['evento']['accion']['rolling_out']['bateador'])
            else:
                return fill_template(random.choice(self._templates['estadisticas']['jugada']['evento']['accion']['rolling_out']['lanzador']), d)

        elif 'Double Play' in event:
            return fill_template(random.choice(self._templates['estadisticas']['jugada']['evento']['accion']['doble_play']), d)

        elif event == 'Strikeout':
            return fill_template(random.choice(self._templates['estadisticas']['jugada']['evento']['accion']['ponche']), d)

        elif 'Flyball' in event and self._player_dict['position'] == 'P':
            return fill_template(random.choice(self._templates['estadisticas']['jugada']['evento']['accion']['flyball']), d)

        elif 'Sacrifice' in event and self._player_dict['position'] != 'P':
            return random.choice(self._templates['estadisticas']['jugada']['evento']['accion']['sacrificio'])

        elif event == 'Lineout' and self._player_dict['position'] == 'P':
            return fill_template(random.choice(self._templates['estadisticas']['jugada']['evento']['accion']['linea_out']['lanzador']), d)

        elif event == 'Lineout' and self._player_dict['position'] != 'P':
            return fill_template(random.choice(self._templates['estadisticas']['jugada']['evento']['accion']['linea_out']['bateador']), d)

        elif event == 'Popfly':
            return fill_template(random.choice(self._templates['estadisticas']['jugada']['evento']['accion']['popfly']), d)

# Complement (only after Event)
class Direction(Stats):
    def get_text(self):
        if self._play_dict['play_desc']['direction'] == '':
            return ''
        direction = self._play_dict['play_desc']['direction'].split('-')[0]
        if direction in self._templates['direccion']:
            direction = random.choice(self._templates['direccion'][direction])
        else:
            return ''

        d = {
            'direccion': direction
        }

        return fill_template(random.choice(self._templates['estadisticas']['jugada']['direccion']['complemento']), d)

# Reaction,
# TODO: no se si sea necesario todavia
class On_Base_Result(Stats):
    def __init__(self, player_name, player_dict, play_dict):
        super().__init__(player_name, player_dict, play_dict)

# Action, Reaction (only batter)
class RBI_Result(Stats):
    def __init__(self, player_name, player_dict, play_dict, templates, act_or_react):
        super().__init__(player_name, player_dict, play_dict, templates)
        self._act_or_react = act_or_react

    def get_text(self):
        cant = self._play_dict['play_desc']['RBI']
        num = number(cant)

        d = {'RBI': num}

        c = '0'
        if cant == 1:
            c = '1'
        elif cant > 1:
            c = '>1'
        else:
            return ''

        if self._act_or_react == 'action':
            return fill_template(random.choice(self._templates['estadisticas']['jugada']['impulsadas_en_jugada']['accion'][c]), d)

        else:
            return fill_template(random.choice(self._templates['estadisticas']['jugada']['impulsadas_en_jugada']['reaccion'][c]), d)
