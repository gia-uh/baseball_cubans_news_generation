import os
from .base import Outstandings
import joblib
import numpy as np

try:
    MODULE = os.path.dirname(os.path.realpath(__file__))
except:
    MODULE = ""

class Outstandings_LR(Outstandings):
    __slots__ = tuple(['_model'])
    def __init__(self):
        super().__init__()
        self._model = joblib.load(os.path.join(MODULE, 'classifier_lr_1.sav'))

    def get_sorted_outstandings(self, players_details):
        data = {}
        for player in players_details['hitters']:
            if len(players_details['hitters'][player]['plays']) == 0:
                continue
            data[player] = {}
            x = players_details['hitters'][player]['wpa_bat']
            y = players_details['hitters'][player]['leverage_index_avg']
            z = players_details['hitters'][player]['re24_bat']
            data[player]['stats'] = [float(x), float(y), float(z)]

        for player in players_details['pitchers']:
            if len(players_details['pitchers'][player]['plays']) == 0:
                continue
            data[player] = {}
            x = players_details['pitchers'][player]['wpa_def']
            y = players_details['pitchers'][player]['leverage_index_avg']
            z = players_details['pitchers'][player]['re24_def']
            data[player]['stats'] = [float(x), float(y), float(z)]

        coefs = self._model.coef_
        sorted_players = []
        for player in data:
            stats = data[player]['stats']
            stats_for_pred = np.array(stats)
            stats_for_pred = stats_for_pred.reshape(1, -1)
            outstanding = self._model.predict(stats_for_pred)
            coef = stats[0]*coefs[0][0] + stats[1]*coefs[0][1] + stats[2]*coefs[0][2]
            #data[player]['outstanding'] = outstanding[0]
            #data[player]['coef'] = coef
            sorted_players.append( (coef, player, outstanding[0]) )

        sorted_players.sort(reverse=True)
        #sorted_players.reverse()

        return sorted_players
