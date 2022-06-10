import contextlib
import io
import time

# stdout работы файла с кодом студента (все его print()) в виде одной строки
output = io.StringIO()
with contextlib.redirect_stdout(output):
    import precode

# stdout работы файла с кодом автора (все его print()) в виде одной строки
author_output = io.StringIO()
with contextlib.redirect_stdout(author_output):
    import author


def time_check(func):
    def wrapper(*args):
        start_time = time.time()
        func(*args)
        execution_time = round(time.time() - start_time, 1)
        return execution_time
    return wrapper


class TestTask:

    def test_make_divider(self):
        author_div2 = author.make_divider_of(2)
        user_div2 = precode.make_divider_of(2)
        assert author_div2(10) == user_div2(10), (
            "Функция `make_divider()` работает не верно")

    def test_time_make_divider(self):
        author_div2 = author.make_divider_of(2)
        user_div2 = precode.make_divider_of(2)
        tm_au = time_check(author_div2)(10)
        tm_us = time_check(user_div2)(10)
        assert tm_au == tm_us, (
            "Функция `make_divider()` выполняется слишком долго"
        )

    def test_response_output(self):
            assert output.getvalue() == author_output.getvalue(), (
                "Error: Вы ошиблись в выводе на экран !")
