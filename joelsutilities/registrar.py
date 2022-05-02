from typing import Dict, Generic, TypeVar, ValuesView
from collections.abc import ItemsView

from .exceptions import RegistrarException

T = TypeVar("T")

class Registrar(Generic[T]):
    """
    Registrar dictionary wrapper of unique string to elements
    
    ``register_named`` and ``register_element`` provide wrapper functions, typically used as decorators to "register" a function or class
    
    Dictionary of elements can be accessed using ``registrar.get(...)``, ``registrar.values()`` and ``registrar.items()``
    
    Dictionary indexing functions are also available using ``... in registrar`` or ``registrar[...]``

    :param T Generic: generic type of object held in dictionary elements
    """
    def __init__(self):
        self._reg: Dict[str, T] = dict()

    def register_named(self, name: str):
        """
        register an element using a defined name, add to dictionary of elements            
        """

        def inner(obj):
            return self._reg_element(name=name, obj=obj)

        return inner

    def register_element(self, obj: T) -> T:
        """
        register an element using its `__name__` attribute, add to dictionary of elements
        """
        return self._reg_element(name=obj.__name__, obj=obj)

    def _reg_element(self, name: str, obj: T) -> T:
        if name in self._reg:
            raise RegistrarException(
                f'registering object "{obj.__name__}", but already exists!'
            )
        else:
            self._reg[name] = obj
            return obj

    def __getitem__(self, item) -> T:
        if item in self._reg:
            return self._reg[item]
        else:
            raise RegistrarException(f'object "{item}" not found in registrar')

    def __contains__(self, item):
        return item in self._reg

    def items(self) -> ItemsView[str, T]:
        return self._reg.items()

    def values(self) -> ValuesView[T]:
        return self._reg.values()

