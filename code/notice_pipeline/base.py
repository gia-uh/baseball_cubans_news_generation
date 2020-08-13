import abc
from importlib import import_module
from configparser import ConfigParser
from typing import Dict, Any, List, Union
import json
import os
try:
    MODULE = os.path.dirname(os.path.realpath(__file__))
except:
    MODULE = ""

class Scrapper(metaclass=abc.ABCMeta):
    __slots__ = tuple(['_data', '_is_scrap_data'])
    def __init__(self):
        self._data = None
        self._is_scrap_data = False

    @abc.abstractmethod
    def _scrap(self)->Dict[str, Any]:
        raise NotImplementedError

    def scrap(self)->Dict[str, Any]:
        self._data = self._scrap()
        self._is_scrap_data = True
        return self._data

    @property
    def data(self)->Dict[str, Any]:
        if self._is_scrap_data is True:
            return self._data
        return self.scrap()

class ScrapperGames(Scrapper, metaclass=abc.ABCMeta):
    __slots__ = ()

    # @abc.abstractmethod
    # def __call__(self, country_results):
    #     """
    #     This class is call  with the result of the previous stage in the pipeline
    #     """
    #     raise NotImplementedError

    @property
    def allGamesDetails(self):
        if self._is_scrap_data is False:
            self.scrap()
        return self._data['all_games_details']

    @property
    def gameDayData(self):
        if self._is_scrap_data is False:
            self.scrap()
        return self._data['game_day_data']

class Outstandings(metaclass=abc.ABCMeta):
    __slots__ = ()
    @abc.abstractmethod
    def get_sorted_outstandings(self, players_details: Dict[str, Any])->Union[dict, list]:
        raise NotImplementedError

class News(metaclass=abc.ABCMeta):
    __slots__ = ('_player_details', '_sorted_for_outstandings', '_games_details',
                 '_players_teams', '_text', '_templates')
    def __init__(self, player_details, sorted_for_outstandings, games_details, players_teams):
        self._player_details = player_details
        self._sorted_for_outstandings = sorted_for_outstandings
        self._games_details = games_details
        self._players_teams = players_teams
        self._text = None

    @abc.abstractmethod
    def _get_text(self)->Dict[str, Any]:
        raise NotImplementedError

    def get_text(self)->Dict[str, Any]:
        self._text = self._get_text()
        return self._text

    @property
    def text(self)->Dict[str, Any]:
        if self._text is not None:
            return self._text
        return self.get_text()

class Configuration(metaclass=abc.ABCMeta):
    __slots__ = ('_config', '_country', '_scraping', '_clasification', '_generation')
    def __init__(self, config_file='./config.init'):
        self._config = ConfigParser()
        self._config.read(config_file)
        self._country = None
        self._scraping = None
        self._clasification = None
        self._generation = None

    def _instanciate_country(self):
        scraping_players_module = self._config.get('country', 'module')
        scraping_players_class = self._config.get('country', 'class')
        scraping_players_country = self._config.get('country', 'country')
        module = import_module(scraping_players_module)
        class_ = getattr(module, scraping_players_class)
        c = class_(scraping_players_country)
        return c

    def _instanciate_scraping(self, country):
        scraping_module = self._config.get('scraping', 'module')
        scraping_class = self._config.get('scraping', 'class')
        module = import_module(scraping_module)
        class_ = getattr(module, scraping_class)
        if self._config.get('scraping','receiveCountry') == 'True':
            c = class_(country)
        else:
            c = class_()
        return c

    def _instanciate_clasification(self):
        clasification_module = self._config.get('clasification', 'module')
        clasification_class = self._config.get('clasification', 'class')
        module = import_module(clasification_module)
        class_ = getattr(module, clasification_class)
        c = class_()
        return c

    def _instanciate_generation(self, player_details, sorted_for_outstandings, games_details, players_teams):
        gen_module = self._config.get('generation', 'module')
        gen_class = self._config.get('generation', 'class')
        module = import_module(gen_module)
        class_ = getattr(module, gen_class)
        c = class_(player_details, sorted_for_outstandings, games_details, players_teams)
        return c

    @abc.abstractmethod
    def _after_run(self, *args, **kwargs):
        """
        The result of the last stage of the pipeline is passed
        as part of **kwargs in the key "pipeline_result"
        """
        raise NotImplementedError

    def _before_run(self, *args, **kwargs):
        """
        This method is called before the run method of the class execute his content
        This method must return True or False
        if return True the then content of run is executed
        otherway isn't
        """
        return True

    def run(self, *args, **kwargs):
        if not self._before_run(*args, **kwargs):
            return
        if self._country is None:
            self._country = self._instanciate_country()
            assert issubclass(type(self._country), Scrapper)

        players = self._country.data

        if self._scraping is None:
            self._scraping = self._instanciate_scraping(players)
            assert issubclass(type(self._scraping), ScrapperGames)

        if self._clasification is None:
            self._clasification = self._instanciate_clasification()
            assert issubclass(type(self._clasification), Outstandings)

        sfo = self._clasification.get_sorted_outstandings(self._scraping.gameDayData)

        if self._generation is None:
            self._generation = self._instanciate_generation(
                self._scraping.gameDayData,
                sfo,
                self._scraping.allGamesDetails,
                players,
            )
            assert issubclass(type(self._generation), News)
        result = self._generation.text

        kwargs['pipeline_result'] = result
        return self._after_run(*args, **kwargs)
