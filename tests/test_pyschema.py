from joelsutilities import pyschema


def test_inheritance_args():
    def get_keys(c):
        return list(pyschema.get_inheritance_args(c).keys())

    class A:
        def __init__(self, a: int, b: str):
            pass
    assert get_keys(A) == ['a', 'b']

    class B(A):
        def __init__(self, c: int):
            super().__init__(1, '2')

    # *args and **kwargs not passed so shouldn't process parent classes
    assert get_keys(B) == ['c']

    class C(A):
        def __init__(self, d: int, **kwargs):
            super().__init__(**kwargs)

    # init args should be from defined class + parent classes
    assert get_keys(C) == ['d', 'a', 'b']

