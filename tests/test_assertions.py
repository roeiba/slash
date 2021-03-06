from .utils import (
    TestCase,
    CustomException,
    )
from contextlib import contextmanager
from slash import should
from slash.exceptions import TestFailed

class AssertionsTest(TestCase):
    def test_assert_equals(self):
        with checking(should.equal, should.not_equal):
            good(1, 1)
            bad(1, 2)
    def test_assert_isinstance(self):
        with checking(should.be_a, should.not_be_a):
            good(1, int)
            good("a", str)
            good({}, dict)
            bad(1, 1)
            bad(1, str)
            bad(None, str)
    def test_is_none(self):
        with checking(should.be_none, should.not_be_none):
            good(None)
            bad("None")
    def test_is(self):
        obj = object()
        with checking(should.be, should.not_be):
            good(obj, obj)
            good(self, self)
            bad(obj, object())
            bad({}, {})
    def test_truth(self):
        with checking(should.be_true, should.be_false):
            good(True)
            good("hello")
            bad(False)
            bad("")
            bad({})
    def test_in(self):
        with checking(should.be_in, should.not_be_in):
            good(1, [1, 2, 3])
            good("e", "hello")
            bad(1, [])
            bad("e", "fdfd")
        with checking(should.contain, should.not_contain):
            good([1, 2, 3], 1)
            good("hello", "e")
            bad("fdfdfd", "e")
    def test_raises_exception(self):
        thrown = CustomException()
        with should.raise_exception(CustomException) as caught:
            raise thrown
        self.assertIs(caught.exception, thrown)
        try:
            with should.raise_exception(CustomException):
                raise OtherException()
        except OtherException:
            pass
        else:
            self.fail("should.raise_exception allowed a different type of exception to be raised")
        try:
            with should.raise_exception(CustomException):
                pass
        except TestFailed as e:
            self.assertIn(" not raised", str(e))
        else:
            self.fail("should.raise_exception allowed success")

## boilerplate

class OtherException(BaseException):
    pass

_MESSAGE = "SOME MESSAGE HERE"


def good(*args):
    _test_assertion(args, positive=True)

def bad(*args):
    _test_assertion(args, positive=False)

def _test_assertion(args, positive):
    positive_assertion = _current_positive_assertion
    negative_assertion = _current_negative_assertion
    if not positive:
        positive_assertion, negative_assertion = negative_assertion, positive_assertion
    positive_assertion(*args)
    positive_assertion(*(args+(_MESSAGE,)))
    for msg in (None, _MESSAGE):
        try:
            negative_assertion(*(args + (msg,)))
        except TestFailed as e:
            if msg is not None:
                assert msg in str(e)
        else:
            assert False, "Assertion did not fail"


_current_positive_assertion = None
_current_negative_assertion = None

@contextmanager
def checking(assertion, negative_assertion):
    global _current_positive_assertion
    global _current_negative_assertion
    assert _current_positive_assertion is None
    _current_positive_assertion = assertion
    _current_negative_assertion = negative_assertion
    try:
        yield
    finally:
        _current_positive_assertion = None
        _current_negative_assertion = None
