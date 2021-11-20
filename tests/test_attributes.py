from joelsutilities import attributes


def test_dgetattr():
    class A:
        class B:
            class C:
                D = 1

    assert attributes.dgetattr(A, 'B.C.D') == 1
    assert attributes.dgetattr(dict(a=dict(b=dict(c=1))), 'a.b.c', is_dict=True) == 1


def test_dgetattr_name():
    assert attributes.dattr_name('A.B.C.D') == 'D'
    assert attributes.dattr_name('A') == 'A'


def test_object_members():
    class TestClass:
        a = 1
        b = 2
        _c = 3

        def d(self):
            pass

    assert attributes.object_members(TestClass()) == ['a', 'b']