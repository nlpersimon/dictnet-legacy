from typing import TYPE_CHECKING, Dict
from copy import deepcopy

if TYPE_CHECKING:
    from .dictnet import Dictnet


class Senset:
    def __init__(self, sense: Dict[str, str], dictnet: "Dictnet" = None):
        self._id = sense['id']
        self._key = sense['key']
        self._headword = sense['headword']
        self._pos = sense['pos']
        self._guideword = sense['guideword']
        self._en_def = sense['en_def']
        self._ch_def = sense['ch_def']
        self._level = sense['level']
        self._gcs = sense['gcs']
        self._examples = sense['examples']
        self._dictnet = dictnet

    @property
    def id(self):
        return self._id

    @property
    def key(self):
        return self._key

    @property
    def headword(self):
        return self._headword

    @property
    def pos(self):
        return self._pos

    @property
    def guideword(self):
        return self._guideword

    @property
    def en_def(self):
        return self._en_def

    @property
    def en_def(self):
        return self._en_def

    @property
    def ch_def(self):
        return self._ch_def

    @property
    def gcs(self):
        return self._gcs

    @property
    def examples(self):
        return deepcopy(self._examples)

    def __repr__(self) -> str:
        return f"Senset('{self.id}')"

    def similar_sensets(self, pos=None, top=10):
        return self._dictnet.find_similar_sensets_by_id(self.id, pos, top)
