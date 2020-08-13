import abc

class Entity(metaclass=abc.ABCMeta):
    def __init__(self, player_name, player_dict, templates):
        self._player_name = player_name
        self._player_dict = player_dict
        self._templates = templates

    @property
    def text(self):
        return self.get_text()

    @abc.abstractmethod
    def get_text(self):
        raise NotImplementedError

class Highlights(metaclass=abc.ABCMeta):
    def __init__(self, player_name, player_dict, templates):
        self._player_dict = player_dict
        self._player_name = player_name
        self._templates = templates

class Stats(Entity, metaclass=abc.ABCMeta):
    def __init__(self, player_name, player_dict, templates, play_dict):
        super().__init__(player_name, player_dict, templates)
        self._play_dict = play_dict

class Action(Entity, metaclass=abc.ABCMeta):
    def __init__(self, player_name, player_dict, templates, condition='action'):
        super().__init__(player_name, player_dict, templates)
        self._condition = condition

class EntityCont(Entity, metaclass=abc.ABCMeta):
    def __init__(self, player_name, player_dict):
        super().__init__(player_name, player_dict)
        self._cont = 0

    @property
    def cont(self):
        return self._cont

    @cont.setter
    def cont(self, cont):
        assert isinstance(cont, int) or isinstance(cont, float)
        self._cont=cont
