from joelsutilities import jsonutils


def test_is_jsonable():
    class A:
        pass
    assert jsonutils.is_jsonable('hello') is True
    assert jsonutils.is_jsonable(A) is False
    assert jsonutils.is_jsonable(A()) is False
    assert jsonutils.is_jsonable(1) is True
    assert jsonutils.is_jsonable({'a': 1}) is True
    assert jsonutils.is_jsonable({'a': A}) is False
