from typing import Dict, List
from .senset import Senset


class Dictnet:
    def __init__(self, senses: List[Dict[str, str]], def_embeds):
        self._def_embeds = def_embeds
        self._pos_to_sensets, self._headword_to_sensets, self._id_to_sensets = self._load_sensets(
            senses)

    def _load_sensets(self, senses):
        pos_to_sensets = {}
        headword_to_sensets = {}
        id_to_sensets = {}
        for sense in senses:
            if sense['id'] not in self._def_embeds:
                continue
            headword = sense['headword']
            pos = sense['pos']
            if pos not in pos_to_sensets:
                pos_to_sensets[pos] = []
            if headword not in headword_to_sensets:
                headword_to_sensets[headword] = []
            senset = Senset(sense, self)
            pos_to_sensets[pos].append(senset)
            headword_to_sensets[headword].append(senset)
            id_to_sensets[senset.id] = senset
        return (pos_to_sensets, headword_to_sensets, id_to_sensets)

    def keys(self, pos=None) -> List[str]:
        if pos is None:
            return list(set(senset.key for sensets in self._pos_to_sensets.values()
                            for senset in sensets))
        elif pos not in self._pos_to_sensets:
            raise KeyError(
                f'{pos} is not in the pos tags: {list(self._pos_to_sensets.keys())}')
        else:
            return list(set(senset.key for senset in self._pos_to_sensets[pos]))

    def headwords(self, pos=None) -> List[str]:
        if pos is None:
            return list(set(senset.headword for sensets in self._pos_to_sensets.values()
                            for senset in sensets))
        elif pos not in self._pos_to_sensets:
            raise KeyError(
                f'{pos} is not in the pos tags: {list(self._pos_to_sensets.keys())}')
        else:
            return list(set(senset.headword for senset in self._pos_to_sensets[pos]))

    def all_sensets(self, pos=None):
        if pos is None:
            return [senset for sensets in self._pos_to_sensets.values()
                    for senset in sensets]
        elif pos not in self._pos_to_sensets:
            raise KeyError(
                f'{pos} is not in the pos tags: {list(self._pos_to_sensets.keys())}')
        else:
            return [senset for senset in self._pos_to_sensets[pos]]

    def sensets(self, headword, pos=None):
        if headword not in self._headword_to_sensets:
            raise KeyError(f'{headword} is not in the sensets')
        sensets = self._headword_to_sensets[headword]
        if pos is None:
            return sensets
        elif pos not in self._pos_to_sensets:
            raise KeyError(
                f'{pos} is not in the pos tags: {list(self._pos_to_sensets.keys())}')
        else:
            return [senset for senset in sensets
                    if senset.pos == pos]

    def senset(self, senset_id):
        if senset_id not in self._def_embeds:
            raise KeyError(f'{senset_id} is not in the sensets')
        return self._id_to_sensets[senset_id]

    def find_similar_sensets_by_id(self, senset_id, pos=None, top=10):
        if senset_id not in self._def_embeds:
            raise KeyError(f'{senset_id} is not in the sensets')
        if pos is None:
            return [self.senset(_id) for _id, _ in self._def_embeds.most_similar(senset_id, topn=top)]
        elif pos not in self._pos_to_sensets:
            raise KeyError(
                f'{pos} is not in the pos tags: {list(self._pos_to_sensets.keys())}')
        else:
            sensets = []
            candidates = self._def_embeds.most_similar(
                senset_id, topn=len(self._def_embeds.vocab))
            for _id, _ in candidates:
                if len(sensets) >= top:
                    break
                senset = self.senset(_id)
                if senset.pos == pos:
                    sensets.append(senset)
            return sensets
