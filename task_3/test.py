import contextlib
import io
import time

import pytest

# stdout работы файла с кодом студента (все его print()) в виде одной строки
output = io.StringIO()
with contextlib.redirect_stdout(output):
    import precode

# stdout работы файла с кодом автора (все его print()) в виде одной строки
author_output = io.StringIO()
with contextlib.redirect_stdout(author_output):
    import author

# переменная, в которой в виде строки хранится весь код студента.
with open("precode.py", encoding="utf-8") as task:
    user_code = task.readlines()

# переменная, в которой в виде строки хранится весь код автора.
with open("author.py", encoding="utf-8") as task:
    author_code = task.readlines()


class MsgError:

    def __init__(self, method_name, *args, **kwargs):
        self.result = getattr(self, method_name)(*args, **kwargs)

    def add_def(self, def_name):
        return f"Проверьте наличие функции `{def_name}()`"

    def dont_cahge_def(self, def_name):
        return f"Кажется вы изменили функцию `{def_name}()`"


@pytest.fixture
def msg_err():
    def _msg_err(msg_name, *args, **kwargs):
        msg = MsgError(msg_name, *args, **kwargs)
        return msg.result
    return _msg_err


def time_check(func):
    def wrapper(*args):
        start_time = time.time()
        func(*args)
        execution_time = round(time.time() - start_time, 1)
        return execution_time
    return wrapper


def foo(num):
    time.sleep(1)
    return num*2


class TestTask:

    def test_have_def(self, msg_err):
        try:
            precode.time_check
        except AttributeError:
            assert False, msg_err("add_def", "time_check")
        try:
            precode.cache_args
        except AttributeError:
            assert False, msg_err("add_def", "cache_args")
        try:
            precode.long_heavy
        except AttributeError:
            assert False, msg_err("add_def", "long_heavy")

    # def test_time_check(self, msg_err):
    #     us_tm_ch = io.StringIO()
    #     with contextlib.redirect_stdout(us_tm_ch):
    #         importlib.reload(precode)
    #         precode.time_check(foo)(2)

    #     au_tm_ch = io.StringIO()
    #     with contextlib.redirect_stdout(au_tm_ch):
    #         importlib.reload(author)
    #         author.time_check(foo)(2)

    #     assert us_tm_ch.getvalue() == au_tm_ch.getvalue(), msg_err(
    #         "dont_cahge_def", "time_check"
    #     )

    def test_long_heavy(self, msg_err):
        assert precode.long_heavy(4) == author.long_heavy(4), msg_err(
            "dont_cahge_def", "long_heavy"
        )

    def test_cache_args(self):
        user_cache = precode.cache_args(foo)
        author_cache = author.cache_args(foo)
        for i in (1, 1, 2, 2, 2):
            assert time_check(user_cache)(i) == time_check(author_cache)(i), (
                "Фунуция `cache_args()` работает не верно"
            )

    def test_response_output(self):
        assert output.getvalue() == author_output.getvalue(), (
            "Error: Вы ошиблись в выводе на экран !")
