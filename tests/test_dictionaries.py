from joelsutilities import dictionaries


def test_dict_subset():
    def t(inner, outer):
        assert dictionaries.is_dict_subset(inner, outer)

    def f(inner, outer):
        assert not dictionaries.is_dict_subset(inner, outer)

    t(
        {'a': 1},
        {'a': 1, 'b': 2}
    )
    t(
        {},
        {'a': 1}
    )
    t(
        {},
        {}
    )
    f(
        {'a': {}},
        {}
    )
    f(
        {'a': {'b': 2}},
        {'a': {'b': 3}}
    )
    t(
        {'a': {'b': {'c': 1}}},
        {'a': {'b': {'c': 1, 'd': 2}}}
    )


def test_dict_update():
    x = {'a': 1, 'b': 2}
    dictionaries.dict_update({'b': {'c': 1}}, x)
    assert x == {'a': 1, 'b': {'c': 1}}
