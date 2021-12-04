import copy
from collections.abc import Mapping
from typing import Dict, Iterable

from .exceptions import DictException


# TODO - remove
def validate_config(cfg: Dict, cfg_spec: Dict):
    _cfg = copy.deepcopy(cfg)
    for k, spec in cfg_spec.items():
        exist = k in _cfg
        val = _cfg.pop(k, None)
        if not spec.get("optional"):
            if not exist:
                raise DictException(
                    f'expected key "{k}" in configuration dict as per config spec: "{cfg_spec}"'
                )
        if exist:
            # if 'type' in spec:
            if not isinstance(val, spec["type"]):
                raise DictException(
                    f'expected key "{k}" value to be type "{spec["type"]}", got "{type(val)}"'
                )
    if _cfg:
        raise DictException(f'configuration dictionary has unexpected values: "{_cfg}"')


def is_dict_subset(inner: dict, outer: dict):
    """
    recursively determine if key value pairs in `inner` are a subset of `outer`
    - `outer` keys must eclipse `inner`s
    - `outer` can have additional keys
    - `inner` values must match `outer`s
    """
    for k, v in inner.items():
        if k not in outer:
            return False
        elif all(hasattr(v, a) for a in ["items", "__getitem__", "__contains__"]):
            if not isinstance(outer[k], Iterable):
                return False
            elif not is_dict_subset(v, outer[k]):
                return False
        elif v != outer[k]:
            return False
    return True


def dict_update(updates: Mapping, base_dict: Mapping):
    """recursively update key value pairs of base_dict with updates"""

    for k, v in updates.items():

        if not isinstance(v, dict):
            # value is not dict
            base_dict[k] = v
            continue

        # value is dict
        if k not in base_dict:
            # value is dict & key not found in y
            base_dict[k] = v
            continue

        # value is dict & key found in y
        if isinstance(base_dict[k], Iterable):
            # value is dict & key found in y & value in y is iterable
            dict_update(v, base_dict[k])
            continue

        # value is dict & key found in y & value in y is not iterable
        base_dict[k] = v


def dict_sort(d: dict, key=lambda item: item[1]) -> Dict:
    """sort a dictionary items"""
    return {k: v for k, v in sorted(d.items(), key=key)}
