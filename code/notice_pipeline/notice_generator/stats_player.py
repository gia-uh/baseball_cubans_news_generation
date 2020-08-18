import random
from .base_class import Entity, Highlights
from .base_class import Action, EntityCont
from .utils import fill_template, number

# Entity
class Player_name(Entity):
    def get_text(self):
        spl = self._player_name.split()
        c = ''
        for i in spl[1:]:
            c += i + ' '
        return c

# Entity
class Position(Entity):
    def get_text(self):
        pos = self._player_dict['position'].split('-')[0]
        l_pos = self._templates['posicion'][pos]
        return random.choice(l_pos)

# Entity
class Team(Entity):
    def get_text(self):
        return self._player_dict['team']

# Entity
class Rival_Team(Entity):
    def get_text(self):
        return self._player_dict['rival_team']

# Entity
class Referring(Entity):
    def __init__(self, referring_list):
        super().__init__('', '', '')
        self._referring_list = referring_list

    def get_text(self):
        return random.choice(self._referring_list)

# NO
class Result(EntityCont):
    # win or lose
    def get_text(self):
        return str(self._cont)

###########################################
################ GENERIC ##################
###########################################

# Entity, Action
class Hits(Action):
    def get_text(self):
        cant = self._player_dict['H']

        num = number(cant)

        d = {'H': num}

        c = '0'
        if cant == 1:
            c = '1'
        elif cant > 1:
            c = '>1'

        pos = 'bateador'
        if self._player_dict['position'] == 'P':
            pos = 'lanzador'

        if self._condition == 'entity':
            return fill_template(random.choice(self._templates['estadisticas']['jugador']['hits']['entidad'][c]), d)
        return fill_template(random.choice(self._templates['estadisticas']['jugador']['hits']['accion'][pos][c]), d)

# Entity, Action
class Runs(Action):
    def get_text(self):
        cant = self._player_dict['R']
        er = 0
        if 'ER' in self._player_dict:
            er = self._player_dict['ER']

        num = number(cant)

        d = {'R': num}

        c = '0'
        if cant == 1:
            c = '1'
        elif cant > 1:
            c = '>1'

        pos = 'bateador'
        if self._player_dict['position'] == 'P':
            pos = 'lanzador'

        if self._condition == 'entity':
            return fill_template(random.choice(self._templates['estadisticas']['jugador']['carreras_anotadas']['entidad'][c]), d)

        if cant == 0:
            return fill_template(random.choice(self._templates['estadisticas']['jugador']['carreras_anotadas']['accion'][pos][c]), d)
        if pos == 'bateador':
            return fill_template(random.choice(self._templates['estadisticas']['jugador']['carreras_anotadas']['accion'][pos][c]), d)
        x = 'limpias'
        if er != cant:
            if er != 0:
                x = 'medio'
            else:
                x = 'sucias'
        return fill_template(random.choice(self._templates['estadisticas']['jugador']['carreras_anotadas']['accion'][pos][c][x]), d)

# Entity
class BB(Entity):
    def get_text(self):
        cant = self._player_dict['BB']

        num = number(cant)

        d = {"BB": num}

        c = '0'
        if cant == 1:
            c = '1'
        elif cant > 1:
            c = '>1'

        return fill_template(random.choice(self._templates['estadisticas']['jugador']['base_por_bolas']['entidad'][c]), d)


###########################################
################ HITTERS ##################
###########################################

# Complement
class AB(Entity):
    def get_text(self):
        cant = self._player_dict['AB']

        num = number(cant)

        d = {"AB": num}

        c = '0'
        if cant == 1:
            c = '1'
        elif cant > 1:
            c = '>1'

        return fill_template(random.choice(self._templates['estadisticas']['jugador']['turnos_al_bate']['complemento'][c]), d)

# Entity
class Doubles(Entity):
    def get_text(self):
        cant = self._player_dict['Double']
        num = number(cant)

        d = {"2B": num}

        c = '0'
        if cant == 1:
            c = '1'
        elif cant > 1:
            c = '>1'

        return fill_template(random.choice(self._templates['estadisticas']['jugador']['dobles']['entidad'][c]), d)

# Entity
class Triples(Entity):
    def get_text(self):
        cant = self._player_dict['Triple']
        num = number(cant)

        d = {"3B": num}

        c = '0'
        if cant == 1:
            c = '1'
        elif cant > 1:
            c = '>1'

        return fill_template(random.choice(self._templates['estadisticas']['jugador']['triples']['entidad'][c]), d)

# Entity
class Home_Runs(Entity):
    def get_text(self):
        cant = self._player_dict['HR']
        num = number(cant)

        d = {"HR": num}

        c = '0'
        if cant == 1:
            c = '1'
        elif cant > 1:
            c = '>1'

        return fill_template(random.choice(self._templates['estadisticas']['jugador']['jonrones']['entidad'][c]), d)

# Action, Entity
class RBI(Action):
    def get_text(self):
        cant = self._player_dict['RBI']

        num = number(cant)

        d = {"RBI": num}

        c = '0'
        if cant == 1:
            c = '1'
        elif cant > 1:
            c = '>1'

        condition = 'entidad'
        if self._condition != 'entity':
            condition = 'accion'

        return fill_template(random.choice(self._templates['estadisticas']['jugador']['carreras_impulsadas'][condition][c]), d)


###########################################
################ PITCHERS #################
###########################################

# Complement
class IP(Entity):
    def get_text(self):
        ip = self._player_dict['IP']

        d = {"IP": ip}

        c = '1'
        if ip != '1':
            c = 'not_1'

        return fill_template(random.choice(self._templates['estadisticas']['jugador']['entradas_lanzadas']['complemento'][c]), d)

# Action, Entity, NO
class ER(EntityCont):
    def get_text(self):
        return str(self._cont)

# Entity
class SO(Entity):
    def get_text(self):
        cant = self._player_dict['SO']
        num = number(cant)

        d = {"SO": num}

        c = '0'
        if cant == 1:
            c = '1'
        elif cant > 1:
            c = '>1'

        return fill_template(random.choice(self._templates['estadisticas']['jugador']['ponches']['entidad'][c]), d)

# Action
class Impact(Entity):
    def get_text(self):
        impact = self._player_dict['impact']

        g = ''

        if "W" in impact:
            g = 'W'
        elif 'L' in impact:
            g = 'L'
        elif "S" in impact:
            g = 'S'

        if g != '':
            return random.choice(self._templates['estadisticas']['jugador']['impacto']['accion'][g])
        return ''

# Action
class Batters_faced(Entity):
    def get_text(self):
        cant = self._player_dict['batters_faced']

        num = number(cant)

        d = {"bateadores_enfrentados": num}

        c = '0'
        if cant == 1:
            c = '1'
        elif cant > 1:
            c = '>1'

        return fill_template(random.choice(self._templates['estadisticas']['jugador']['bateadores_enfrentados']['accion'][c]), d)

###########################################
############### HIGHLIGHTS ################
###########################################

class Highlights_Player(Highlights):
    def __init__(self, player_name, player_dict):
        super().__init__(player_name, player_dict, '')

    def get_dict_of_texts(self):
        name = self._player_name.replace('_1', '')
        name = name.replace('_2', '')
        templates_stats = {}

        if self._player_dict['position'] == 'P':
            ip = self._player_dict['IP']
            h = self._player_dict['H']
            impact = self._player_dict['impact']
            r = self._player_dict['R']
            k = self._player_dict['SO']
            bb = self._player_dict['BB']

            if ip >= '6.0' and r <= 3:
                l = []
                ss = ['apertura', 'salida']
                l.append(name + ' tuvo  ' + random.choice(ss) +' de calidad')
                l.append(name + ' también tuvo '+ random.choice(ss) +' de calidad')
                l.append('otra '+ random.choice(ss) +' de calidad para ' + name)
                templates_stats['SC'] = l

            if impact == 'W':
                l = []

                f = [
                    ' se apuntó la victoria de su equipo',
                    ' ganó el juego',
                ]
                f1 = [
                    'victoria para ',
                    'juego ganado para '
                ]
                ff = [
                    name + random.choice(f),
                    random.choice + name
                ]

                s = ' también ganó el juego para su equipo'

                x = random.choice(ff)

                l.append(x)
                l.append(s)
                templates_stats['W'] = l

            if impact == 'SV':
                l = []

                f = [
                    ' se apuntó el salvamento para su equipo',
                    ' salvó el juego',
                ]
                f1 = [
                    'juego salvado para ',
                    'salvamento para '
                ]
                ff = [
                    name + random.choice(f),
                    random.choice + name
                ]

                s = ' también salvó el juego para su equipo'

                x = random.choice(ff)

                l.append(x)
                l.append(s)
                templates_stats['SV'] = l

            if r <= 3:
                l = []
                zero = [
                    name + ' no permitió ninguna anotación',
                    name + ' no recibió carreras'
                ]
                c = ['carrera', 'carreras']
                a = ['anotación', 'anotaciones']

                i = 1
                if r == 1:
                    i = 0

                l.append(name + ' permitió solamente ' + str(r) + ' ' + c[i])
                l.append(name + ' recibió solo ' + str(r) + ' ' + a[i])

                templates_stats['R'] = l

            if k >= 5:
                l = []

                l.append(name + ' ponchó a ' + str(k) + ' bateadores')
                l.append(name + ' propinó ' + str(k) + ' ponches')
                l.append('juego de ' + str(k) + ' ponches para ' + name)

                templates_stats['K'] = l

            if IP >= '9.0' and h == 0:
                l = []

                l.append(name + 'propinó no hit no run al rival')
                l.append('no hit no run también para ' + name)

                templates_stats['NHNR'] = l

        else:
            ab = self._player_dict['AB']
            h = self._player_dict['H']
            r = self._player_dict['R']
            rbi = self._player_dict['RBI']
            hr = self._player_dict['HR']
            double = self._player_dict['Double']
            triple = self._player_dict['Triple']

            if ab == h and h > 2:
                l = []

                l.append('juego perfecto para ' + name)
                l.append(name + ' tampoco falló al bate')

                templates_stats['PG'] = l

            if hr > 0:
                l = []

                if hr == 1:
                    l.append(name + ' pegó jonrón')
                    l.append('otro cuadrangular de ' + name)
                    l.append(name + ' también disparó jonrón')

                else:
                    l.append(name + ' pegó ' + str(hr) + ' jonrones')
                    l.append(' otros ' + str(hr) + ' jonrones de ' + name)
                    l.append(name + ' también pegó ' + str(hr) + ' jonrones')

                templates_stats['HR'] = l

            if rbi > 0:
                l = []

                a = ['carrera', 'carreras']
                b = ['anotación', 'anotaciones']

                i = 1
                if rbi == 1:
                    i = 0

                l.append(name + ' impulsó ' + str(rbi) + ' ' + a[i])
                l.append(name + ' también empujó ' + str(rbi) + ' ' + b[i])

                templates_stats['RBI'] = l

            if r > 0:
                l = []

                a = ['carrera', 'carreras']
                b = ['vez', 'veces']

                i = 1
                if r == 1:
                    i = 0

                l.append(name + ' anotó ' + str(r) + ' ' + a[i])
                l.append(name + ' también pisó ' + str(r) + b[i] + ' el home')

                templates_stats['R'] = l

            if h > 1:
                l = []

                l.append('multihits de ' + name)
                l.append(name + 'pegó ' + str(h) + ' hits')
                l.append('juego de ' + str(h) + ' indiscutibles para ' + name)

                templates_stats['H'] = l

            if double + triple + hr > 1:
                l = []

                eb = double + triple + hr

                l.append(name + ' disparó ' + str(eb) + ' extrabases')
                l.append('juego de ' + str(h) + ' extrabases para ' + name)

                templates_stats['EB'] = l

        return templates_stats
